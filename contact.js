(() => {
  'use strict';
  const form = document.querySelector('#contact-form');
  if (!form) return;
  const fields = document.querySelector('#contact-fields');
  const reviewButton = document.querySelector('#contact-review-button');
  const review = document.querySelector('#contact-review');
  const output = document.querySelector('#contact-draft');
  const downloadButton = document.querySelector('#contact-download');
  const editButton = document.querySelector('#contact-edit');
  const status = document.querySelector('#contact-status');
  const name = document.querySelector('#contact-name');
  const topic = document.querySelector('#contact-topic');
  const centre = document.querySelector('#contact-centre');
  const email = document.querySelector('#contact-email');
  const message = document.querySelector('#contact-message');
  let prepared = '';

  function draftText() {
    return [
      'ROYAL KARATE SPORTS — UNSENT ENQUIRY DRAFT',
      'This draft is not sent. No class is booked, no camp registration is made and no place is reserved.',
      '',
      `Enquiry: ${topic.selectedOptions[0].textContent}`,
      `Preferred regular training centre: ${centre.selectedOptions[0].textContent}`,
      `Name: ${name.value.trim()}`,
      `Email: ${email.value.trim() || 'Not provided'}`,
      '', 'Question:', message.value.trim(), '',
      'Regular karate training is completely free. No paid classes or training fees.',
      'Class timings, meeting instructions and availability require confirmation.',
      'Camps: summer and winter; enrollments open one month before each season. Exact dates, venue and participation arrangements are not yet announced.',
      'Seminars are proposed offerings and require academy approval.',
      'Contact the academy directly: 8898329666 or always4u.06@gmail.com. This file is not sent automatically.',
      'This local file contains your entries. Keep or delete it securely.', ''
    ].join('\n');
  }

  function invalidate() {
    const hadDraft = Boolean(prepared);
    prepared = '';
    output.textContent = '';
    review.hidden = true;
    downloadButton.disabled = true;
    status.textContent = hadDraft ? 'Draft cleared. Review your updated details before downloading.' : '';
  }

  function validateWhitespace() {
    for (const field of [name, message]) {
      field.setCustomValidity(field.value && !field.value.trim() ? 'Please enter more than spaces.' : '');
    }
  }

  form.addEventListener('input', () => { validateWhitespace(); invalidate(); });
  form.addEventListener('change', () => { validateWhitespace(); invalidate(); });
  form.addEventListener('submit', event => {
    event.preventDefault();
    validateWhitespace();
    if (!form.reportValidity()) return;
    prepared = draftText();
    output.textContent = prepared;
    review.hidden = false;
    downloadButton.disabled = false;
    status.textContent = 'Draft ready to review. Nothing has been sent.';
    document.querySelector('#contact-review-title').focus();
  });

  editButton.addEventListener('click', () => {
    invalidate();
    name.focus();
  });

  downloadButton.addEventListener('click', () => {
    if (!prepared || draftText() !== prepared || !form.checkValidity()) {
      invalidate();
      status.textContent = 'Review your current details before downloading.';
      return;
    }
    const url = URL.createObjectURL(new Blob([prepared], {type: 'text/plain;charset=utf-8'}));
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = 'royal-karate-enquiry-UNSENT.txt';
    document.body.append(anchor);
    anchor.click();
    anchor.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    status.textContent = 'Draft download requested. Nothing has been sent or booked.';
  });

  const topicNotes = {
    'regular-classes': 'Regular karate training is completely free. Exact class timings and meeting instructions need confirmation.',
    'summer-camp': 'Summer camp enrollments open one month before the season. Exact dates, venue and participation details are not yet announced.',
    'winter-camp': 'Winter camp enrollments open one month before the season. Exact dates, venue and participation details are not yet announced.',
    'school-seminar': 'School seminars are proposed offerings. Topics, suitability, venue, instructor and availability need academy approval.',
    'community-seminar': 'College, workplace and community seminars are proposed offerings. Format, suitability and availability need academy approval.',
    'other': 'Share your question. Availability and arrangements still need confirmation.'
  };
  const topicNote = document.querySelector('#contact-topic-note');
  topic.setAttribute('aria-describedby', 'contact-topic-note');
  topicNote.setAttribute('aria-live', 'polite');
  function updateTopicNote() {
    topicNote.textContent = topicNotes[topic.value] || 'Choose a topic. Availability and arrangements still need confirmation.';
  }
  const requestedTopic = new URLSearchParams(location.search).get('enquiry');
  if (Object.hasOwn(topicNotes, requestedTopic || '')) topic.value = requestedTopic;
  topic.addEventListener('change', updateTopicNote);
  updateTopicNote();

  fields.disabled = false;
  reviewButton.disabled = false;
})();
