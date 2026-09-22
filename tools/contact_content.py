"""Verified Contact content; no shared-builder imports or side effects."""
from html import escape
from pathlib import Path
import re
from simple_content import simplify_content

ROOT = Path(__file__).resolve().parents[1]


def build_contact(button, link):
    """Return the Contact main content for the shared Royal page shell."""
    return '''<article class="contact-content">
<section class="wrap contact-heading" aria-labelledby="contact-title">
  <span class="eyebrow red">Contact / Royal Karate Sports</span>
  <h1 id="contact-title">Your first step.<br>Let’s make it clear.</h1>
  <p>Find our training centres, explore your options and prepare the questions you want to ask.</p>
  <a class="contact-jump" href="#contact-enquiry">Prepare an enquiry <span aria-hidden="true">↓</span></a>
</section>
<div class="wrap contact-layout">
  <section class="contact-information" aria-labelledby="contact-centres-title">
    <span class="eyebrow red">Regular karate training</span>
    <h2 id="contact-centres-title">Two centres.<br>Training for everyone.</h2>
    <p class="contact-free">Karate training is completely free.</p>
    <p>No paid classes. No training fees. Akash Kishor Shinde provides free regular karate training at these Mumbai centres.</p>
    <dl class="contact-centres">
      <div><dt>Ganesh Vidyamandir School</dt><dd>Dharavi, Mumbai</dd></div>
      <div><dt>Pratiksha Nagar</dt><dd>Mumbai</dd></div>
    </dl>
    <p class="contact-timing">Exact class timings and meeting instructions are not yet published. Please confirm these before planning a visit.</p>
    <section class="contact-channels" aria-labelledby="contact-channels-title">
      <h3 id="contact-channels-title">Direct contact</h3>
      <p>Reach Shree Aakash shinde using the details supplied for this website.</p>
      <dl>
        <div><dt>Contact</dt><dd>Shree Aakash shinde</dd></div>
        <div><dt>Phone</dt><dd><a href="tel:+918898329666">8898329666</a></dd></div>
        <div><dt>Email</dt><dd><a href="mailto:always4u.06@gmail.com">always4u.06@gmail.com</a></dd></div>
      </dl>
      <p>The form on this page still prepares a local file only. It does not send a message. Use phone or email to reach the academy.</p>
    </section>
    <figure class="contact-person"><img src="assets/akash-kishor-shinde.webp" alt="Akash Kishor Shinde in karate uniform, in the portrait supplied by the owner" width="720" height="960" loading="lazy" decoding="async"><figcaption><span class="eyebrow">The person behind the practice</span><h3>Akash Kishor Shinde</h3><p>Karate trainer &amp; social worker.</p>''' + link('About Akash Shinde', 'about-akash-shinde.html') + '''</figcaption></figure>
  </section>
  <section class="contact-enquiry" id="contact-enquiry" aria-labelledby="contact-form-title">
    <span class="eyebrow red">Your enquiry / Local draft only</span>
    <h2 id="contact-form-title">Prepare an enquiry</h2>
    <p class="contact-form-intro">Write it here. Review it. Keep a copy.</p>
    <div class="contact-preview-note" id="contact-preview-note"><strong>Preview — not connected</strong><p>Nothing is sent to Royal. This does not book a class, register for a camp or reserve a place.</p></div>
    <form id="contact-form" autocomplete="off" aria-describedby="contact-preview-note contact-privacy">
      <fieldset id="contact-fields" disabled>
        <legend class="contact-sr-only">Enquiry details</legend>
        <p class="contact-required-note">Fields marked * are required. For a child, a parent or guardian should complete the draft.</p>
        <div class="contact-field"><label for="contact-topic">What would you like to ask about? *</label><select id="contact-topic" name="topic" required><option value="">Choose an enquiry type</option><option value="regular-classes">Regular classes</option><option value="summer-camp">Summer camp</option><option value="winter-camp">Winter camp</option><option value="school-seminar">School seminar</option><option value="community-seminar">College, workplace or community seminar</option><option value="other">Other enquiry</option></select></div>
        <p class="contact-topic-note" id="contact-topic-note">Choose a topic. Availability and arrangements still need confirmation.</p>
        <div class="contact-field"><label for="contact-centre">Preferred regular training centre <span>(optional)</span></label><select id="contact-centre" name="centre"><option value="not-sure">Not sure / not applicable</option><option value="dharavi">Ganesh Vidyamandir School, Dharavi</option><option value="pratiksha-nagar">Pratiksha Nagar, Mumbai</option></select><p>These are regular training centres, not confirmed camp venues.</p></div>
        <div class="contact-field-row"><div class="contact-field"><label for="contact-name">Your name *</label><input id="contact-name" name="name" type="text" maxlength="100" pattern=".*\\S.*" required></div><div class="contact-field"><label for="contact-email">Your email <span>(optional)</span></label><input id="contact-email" name="email" type="email" maxlength="180" inputmode="email" spellcheck="false"></div></div>
        <div class="contact-field"><label for="contact-message">Your question *</label><textarea id="contact-message" name="message" rows="5" maxlength="2000" required aria-describedby="contact-message-hint"></textarea><p id="contact-message-hint">Ask about timings, starting out or suitability. Do not include a child’s full name, address, medical details or other sensitive information.</p></div>
        <p id="contact-privacy" class="contact-privacy">Your entries stay in this page while it is open. No submission or browser storage is used. Only the file you choose to download is saved; it contains your entries, so keep or delete it securely.</p>
        <button id="contact-review-button" class="button black contact-primary" type="submit" disabled>Review my draft <span aria-hidden="true">→</span></button>
      </fieldset>
      <noscript><p class="contact-noscript">JavaScript is off. The draft form is disabled to protect your details. You can still read the centre information and prepare your questions separately. Nothing will be sent.</p></noscript>
    </form>
    <p id="contact-status" class="contact-status" role="status" aria-live="polite"></p>
    <section id="contact-review" class="contact-review" aria-labelledby="contact-review-title" hidden>
      <span class="eyebrow red">UNSENT / Review before downloading</span><h3 id="contact-review-title" tabindex="-1">Your enquiry draft</h3>
      <p>Check your details below. You can edit them before saving a copy. No message has been sent.</p>
      <pre id="contact-draft" tabindex="0" role="region" aria-label="Unsent enquiry draft text"></pre>
      <div class="contact-review-actions"><button id="contact-download" class="button black" type="button" disabled>Download .txt draft <span aria-hidden="true">↓</span></button><button id="contact-edit" class="contact-edit" type="button">Edit details</button></div>
    </section>
  </section>
</div>
<section class="wrap contact-next" aria-labelledby="contact-next-title"><div><span class="eyebrow red">Before you make plans</span><h2 id="contact-next-title">A little clarity<br>goes a long way.</h2></div><div class="contact-answers">
<details><summary>When are the summer and winter camps?</summary><p>Camps take place twice a year, in summer and winter. Enrollments open one month before each season. Exact dates, venue and participation details for the next camp are not yet announced. Regular karate training is free; camp-specific arrangements need confirmation.</p>''' + link('Explore camps & activities', 'events.html') + '''</details>
<details><summary>Can a school or community group enquire?</summary><p>Yes, you can prepare a seminar enquiry. School, college, workplace and community sessions are proposed offerings, not confirmed events. Topics, suitability, instructor, venue and availability need the academy’s approval.</p>''' + link('About seminar enquiries', 'seminars.html') + '''</details>
<details><summary>What happens after I download my draft?</summary><p>The text file stays on your device. Nothing is submitted from this form, and no reply or booking is triggered. You can also call 8898329666 or email always4u.06@gmail.com.</p></details>
</div></section>
</article><script src="contact.js" defer></script>'''


def render_local():
    """Rebuild through the canonical pipeline, including the shared redesign."""
    import runpy
    runpy.run_path(str(ROOT / 'tools/build.py'), run_name='__main__')


if __name__ == '__main__':
    render_local()
