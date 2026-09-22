"""Contact refresh contract and real-browser regression tests.
Run: python tools/test_contact_refresh.py
"""
from pathlib import Path
import importlib.util
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def contact_body():
    source = ROOT / 'tools/contact_content.py'
    if not source.exists():
        return (ROOT / 'contact.html').read_text(encoding='utf-8')
    spec = importlib.util.spec_from_file_location('contact_content', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_contact(lambda text, url, *args: f'<a href="{url}">{text}</a>',
                                lambda text, url: f'<a href="{url}">{text}</a>')


class ContactContentTests(unittest.TestCase):
    def test_local_renderer_preserves_shell_and_is_idempotent(self):
        import subprocess
        import sys
        target = ROOT / 'contact.html'
        before = target.read_text(encoding='utf-8')
        for _ in range(2):
            run = subprocess.run([sys.executable, str(ROOT / 'tools/contact_content.py')], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
        after = target.read_text(encoding='utf-8')
        for tag in ['header', 'footer']:
            pattern = f'<{tag}\\b.*?</{tag}>'
            self.assertEqual(re.search(pattern, before, re.S)[0], re.search(pattern, after, re.S)[0])
        self.assertEqual(before, after)
        self.assertEqual(after.count('href="royal.css"'), 1)
        self.assertEqual(after.count('src="contact.js"'), 1)
        self.assertIn('<body class="royal-design r-page contact-refresh">', after)

    def test_grounded_contact_has_safe_local_draft_form(self):
        body = contact_body()
        for text in ['Prepare an enquiry', 'Akash Kishor Shinde',
                     'Ganesh Vidyamandir School', 'Dharavi', 'Pratiksha Nagar',
                     'completely free', 'one month before', 'not connected',
                     'Summer camp', 'Winter camp', 'School seminar',
                     'Phone', 'Exact class timings', 'UNSENT']:
            self.assertIn(text, body)
        self.assertRegex(body, r'<form[^>]+id="contact-form"')
        self.assertRegex(body, r'<button[^>]+id="contact-review-button"[^>]+disabled')
        self.assertIn('<script src="contact.js" defer></script>', body)
        self.assertNotIn('novalidate', body)
        self.assertNotIn('assets/704', body)

    def test_supplied_phone_email_and_public_pages(self):
        body = contact_body()
        self.assertIn('Shree Aakash shinde', body)
        self.assertIn('tel:+918898329666', body)
        self.assertIn('8898329666', body)
        self.assertIn('mailto:always4u.06@gmail.com', body)
        self.assertNotIn('instagram.com', body)
        self.assertNotIn('facebook.com', body)
        self.assertNotIn('justdial.com', body)
        self.assertNotIn('Not yet supplied', body)
        self.assertNotIn('phone and email are not yet supplied', body)


class ContactBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import functools
        import http.server
        import threading
        from playwright.sync_api import sync_playwright
        class QuietHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *args):
                pass
        cls.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}/contact.html'
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch()
        cls.artifacts = ROOT / 'verification'
        cls.artifacts.mkdir(exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        self.context = self.browser.new_context(viewport={'width': 1440, 'height': 1000}, accept_downloads=True, reduced_motion='reduce')
        self.page = self.context.new_page()
        self.errors = []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))
        self.page.goto(self.url)

    def tearDown(self):
        self.assertEqual(self.errors, [])
        self.context.close()

    def complete_form(self):
        self.page.select_option('#contact-topic', 'regular-classes')
        self.page.select_option('#contact-centre', 'dharavi')
        self.page.fill('#contact-name', 'Contact QA')
        self.page.fill('#contact-email', 'contact-qa@example.test')
        self.page.fill('#contact-message', 'Which class timings are available?')

    def test_keyboard_can_read_the_full_scrollable_draft(self):
        page = self.page
        page.set_viewport_size({'width': 390, 'height': 844})
        self.complete_form()
        page.locator('#contact-review-button').click()
        self.assertEqual(page.locator('#contact-draft').get_attribute('tabindex'), '0')
        page.keyboard.press('Tab')
        self.assertEqual(page.evaluate('document.activeElement.id'), 'contact-draft')
        page.keyboard.press('End')
        page.wait_for_function("document.querySelector('#contact-draft').scrollTop > 0")
        self.assertGreater(page.locator('#contact-draft').evaluate('(node) => node.scrollTop'), 0)
        page.add_script_tag(path=str(ROOT / 'tools/axe.min.js'))
        result = page.evaluate("async () => await axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21aa']}})")
        self.assertEqual(result['violations'], [])

    def test_no_javascript_or_failed_script_cannot_submit(self):
        for mode in ['no-javascript', 'blocked-contact-script']:
            context = self.browser.new_context(java_script_enabled=mode != 'no-javascript', viewport={'width': 390, 'height': 844})
            if mode == 'blocked-contact-script':
                context.route('**/contact.js', lambda route: route.abort())
            page = context.new_page()
            page.goto(self.url)
            self.assertTrue(page.locator('#contact-review-button').is_disabled())
            self.assertTrue(page.locator('#contact-name').is_disabled())
            self.assertTrue(page.locator('#contact-download').is_disabled())
            self.assertTrue(page.locator('#contact-review').is_hidden())
            self.assertIn('not connected', page.locator('main').inner_text())
            page.keyboard.press('Enter')
            self.assertEqual(page.url, self.url)
            if mode == 'no-javascript':
                self.assertTrue(page.locator('.contact-noscript').is_visible())
                page.locator('.contact-noscript').scroll_into_view_if_needed()
                page.screenshot(path=str(self.artifacts / 'contact-nojs-390.png'))
            context.close()

    def test_accessibility_keyboard_mobile_review_and_offline(self):
        import json
        page = self.page
        page.add_script_tag(path=str(ROOT / 'tools/axe.min.js'))
        results = []
        for width in [1440, 390]:
            page.set_viewport_size({'width': width, 'height': 844})
            result = page.evaluate("async () => await axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21aa']}})")
            results.append({'width': width, 'violations': result['violations'], 'passes': len(result['passes']), 'incomplete': result['incomplete']})
            self.assertEqual(result['violations'], [], f'Accessibility violations at {width}px')
        (self.artifacts / 'contact-accessibility.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
        page.goto(self.url)
        page.keyboard.press('Tab')
        self.assertEqual(page.locator(':focus').inner_text(), 'Skip to content')
        page.keyboard.press('Enter')
        page.locator('#contact-topic').focus()
        page.select_option('#contact-topic', 'winter-camp')
        page.keyboard.press('Tab')
        self.assertEqual(page.evaluate('document.activeElement.id'), 'contact-centre')
        self.complete_form()
        page.fill('#contact-message', '<script>window.BAD = true</script> Plain text question.')
        page.locator('#contact-review-button').focus()
        page.keyboard.press('Enter')
        self.assertTrue(page.locator('#contact-review').is_visible())
        self.assertIsNone(page.evaluate('window.BAD'))
        self.assertEqual(page.locator('#contact-draft script').count(), 0)
        page.fill('#contact-message', 'Which class timings are available for a beginner?')
        page.locator('#contact-review-button').click()
        self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), 390)
        page.locator('#contact-review').scroll_into_view_if_needed()
        page.evaluate('document.fonts.ready')
        page.evaluate('new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))')
        page.screenshot(path=str(self.artifacts / 'contact-review-390.png'))
        page.set_viewport_size({'width': 1440, 'height': 1000})
        page.locator('#contact-review').scroll_into_view_if_needed()
        page.evaluate('new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))')
        page.screenshot(path=str(self.artifacts / 'contact-review-1440.png'))
        page.goto((ROOT / 'contact.html').as_uri())
        self.complete_form()
        page.locator('#contact-review-button').click()
        self.assertTrue(page.locator('#contact-review').is_visible())
        with page.expect_download() as download_info:
            page.locator('#contact-download').click()
        self.assertIsNone(download_info.value.failure())
        page.reload()
        self.assertEqual(page.locator('#contact-name').input_value(), '')
        self.assertTrue(page.locator('#contact-review').is_hidden())

    def test_topic_context_and_allowlisted_links(self):
        page = self.page
        page.goto(self.url + '?enquiry=summer-camp#contact-enquiry')
        self.assertEqual(page.locator('#contact-topic').input_value(), 'summer-camp')
        self.assertIn('one month before', page.locator('#contact-topic-note').inner_text())
        expected = {'regular-classes': 'completely free', 'summer-camp': 'not yet announced',
                    'winter-camp': 'not yet announced', 'school-seminar': 'proposed',
                    'community-seminar': 'proposed', 'other': 'confirmation'}
        for value, text in expected.items():
            page.select_option('#contact-topic', value)
            self.assertIn(text, page.locator('#contact-topic-note').inner_text())
        page.goto(self.url + '?enquiry=unverified-topic')
        self.assertEqual(page.locator('#contact-topic').input_value(), '')

    def test_responsive_layout_and_shared_navigation(self):
        page = self.page
        for width in [1440, 768, 390, 320]:
            page.set_viewport_size({'width': width, 'height': 1000 if width > 760 else 844})
            self.assertTrue(page.locator('.mobile-trial').is_hidden(), 'Contact must not show the unrelated fixed booking shortcut')
            self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), width)
            for field in page.locator('#contact-form input, #contact-form select, #contact-form textarea, #contact-review-button').all():
                box = field.bounding_box()
                self.assertGreaterEqual(box['height'], 44)
                self.assertGreaterEqual(box['x'], 0)
                self.assertLessEqual(box['x'] + box['width'], width)
            if width in [1440, 390]:
                page.evaluate("document.querySelectorAll('main img').forEach(i => i.loading = 'eager')")
                page.evaluate("Promise.all([...document.querySelectorAll('main img')].map(i => i.decode()))")
                page.evaluate('document.fonts.ready')
                page.evaluate('window.scrollTo(0,0)')
                page.screenshot(path=str(self.artifacts / f'contact-{width}.png'), full_page=True)
                page.screenshot(path=str(self.artifacts / f'contact-top-{width}.png'))
                page.locator('#contact-enquiry').scroll_into_view_if_needed()
                page.screenshot(path=str(self.artifacts / f'contact-form-{width}.png'))
        page.set_viewport_size({'width': 390, 'height': 844})
        page.locator('.menu-toggle').click()
        self.assertTrue(page.locator('#mobile-menu').evaluate('(dialog) => dialog.open'))
        page.locator('#mobile-menu summary').filter(has_text='Programmes').click()
        self.assertTrue(page.locator('#mobile-menu a[href="kids-batches.html"]').is_visible())
        page.keyboard.press('Escape')
        self.assertFalse(page.locator('#mobile-menu').evaluate('(dialog) => dialog.open'))
        self.assertEqual(page.evaluate('document.activeElement.className'), 'menu-toggle')
        page.set_viewport_size({'width': 1440, 'height': 1000})
        page.locator('.desktop-nav summary').filter(has_text='Trending').click()
        self.assertTrue(page.locator('.desktop-nav a[href="events.html"]').is_visible())
        page.keyboard.press('Escape')
        self.assertFalse(page.locator('.desktop-nav a[href="events.html"]').is_visible())
        self.assertEqual(page.locator('footer a[href="contact.html"]').get_attribute('aria-current'), 'page')

    def test_native_validation_rejects_whitespace_and_invalid_email(self):
        page = self.page
        self.complete_form()
        page.fill('#contact-message', '   \n   ')
        page.locator('#contact-review-button').click()
        self.assertTrue(page.locator('#contact-review').is_hidden(), 'Whitespace is not an enquiry')
        self.assertFalse(page.locator('#contact-message').evaluate('(field) => field.checkValidity()'))
        page.fill('#contact-message', 'When can a beginner start?')
        page.fill('#contact-name', '   ')
        page.locator('#contact-review-button').click()
        self.assertTrue(page.locator('#contact-review').is_hidden())
        page.fill('#contact-name', 'Contact QA')
        page.fill('#contact-email', 'not-an-email')
        page.locator('#contact-review-button').click()
        self.assertTrue(page.locator('#contact-review').is_hidden())
        self.assertTrue(page.locator('#contact-email').evaluate('(field) => field.validity.typeMismatch'))
        page.fill('#contact-email', '')
        page.locator('#contact-review-button').click()
        self.assertTrue(page.locator('#contact-review').is_visible())
        self.assertIn('Email: Not provided', page.locator('#contact-draft').inner_text())

    def test_review_download_and_edit_never_send(self):
        page = self.page
        self.assertTrue(page.locator('#contact-review-button').is_enabled(), 'JavaScript must enable the safe local form')
        requests = []
        page.on('request', lambda request: requests.append((request.method, request.url)))
        page.locator('#contact-review-button').click()
        self.assertTrue(page.locator('#contact-review').is_hidden())
        self.complete_form()
        page.locator('#contact-review-button').click()
        self.assertTrue(page.locator('#contact-review').is_visible())
        draft = page.locator('#contact-draft').inner_text()
        for text in ['UNSENT', 'Contact QA', 'Regular classes', 'Ganesh Vidyamandir School', 'Which class timings', 'No class', 'not sent']:
            self.assertIn(text, draft)
        self.assertEqual(page.evaluate('document.activeElement.id'), 'contact-review-title')
        with page.expect_download() as download_info:
            page.locator('#contact-download').click()
        download = download_info.value
        self.assertEqual(download.suggested_filename, 'royal-karate-enquiry-UNSENT.txt')
        path = self.artifacts / 'contact-draft-test.txt'
        download.save_as(path)
        self.assertEqual(path.read_text(encoding='utf-8'), draft)
        page.locator('#contact-edit').click()
        self.assertTrue(page.locator('#contact-review').is_hidden())
        self.assertTrue(page.locator('#contact-download').is_disabled())
        self.assertEqual(page.locator('#contact-draft').inner_text(), '')
        page.fill('#contact-message', 'Updated question about starting karate.')
        page.locator('#contact-review-button').click()
        self.assertIn('Updated question', page.locator('#contact-draft').inner_text())
        page.fill('#contact-name', 'Contact QA revised')
        self.assertTrue(page.locator('#contact-review').is_hidden())
        self.assertTrue(page.locator('#contact-download').is_disabled())
        self.assertNotIn('?', page.url)
        self.assertEqual(requests, [], 'Enquiry actions must not make any network requests')
        self.assertEqual(page.evaluate('localStorage.length + sessionStorage.length'), 0)
        self.assertIn('8898329666', draft)
        self.assertIn('always4u.06@gmail.com', draft)
        self.assertNotIn('have not yet been supplied', draft)


if __name__ == '__main__':
    import json
    import sys
    result = unittest.main(verbosity=2, exit=False).result
    report = {'tests_run': result.testsRun,
              'failures': [{'test': str(test), 'traceback': trace} for test, trace in result.failures],
              'errors': [{'test': str(test), 'traceback': trace} for test, trace in result.errors],
              'successful': result.wasSuccessful(),
              'browser': 'Playwright Chromium',
              'viewports': [1440, 768, 390, 320],
              'modes': ['HTTP', 'file://', 'no JavaScript', 'contact.js blocked'],
              'test_data': 'Synthetic Contact QA / example.test only'}
    (ROOT / 'verification').mkdir(exist_ok=True)
    (ROOT / 'verification/contact-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    sys.exit(0 if result.wasSuccessful() else 1)
