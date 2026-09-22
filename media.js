'use strict';
(() => {
  const viewer = document.querySelector('#press-viewer');
  if (!viewer) return;
  const figures = [...document.querySelectorAll('.press-grid figure')];
  const filters = [...document.querySelectorAll('[data-media-filter]')];
  const scan = viewer.querySelector('#press-viewer-image');
  const stage = viewer.querySelector('.press-image-stage');
  const zoom = viewer.querySelector('[data-press-zoom]');
  const previous = viewer.querySelector('[data-press-prev]');
  const next = viewer.querySelector('[data-press-next]');
  const position = viewer.querySelector('#press-position');
  let opener, sequence = [], index = 0;
  function resetZoom() {
    stage.classList.remove('is-zoomed');
    zoom.setAttribute('aria-pressed', 'false');
    zoom.textContent = 'Zoom in';
    stage.scrollTop = stage.scrollLeft = 0;
  }
  function showItem(newIndex) {
    index = newIndex;
    const link = sequence[index];
    resetZoom();
    scan.src = link.getAttribute('href');
    scan.alt = link.querySelector('img').alt;
    viewer.querySelector('#press-viewer-title').textContent = link.dataset.title;
    viewer.querySelector('#press-original').href = link.getAttribute('href');
    previous.disabled = index === 0;
    next.disabled = index === sequence.length - 1;
    position.textContent = `Document ${index + 1} of ${sequence.length}`;
  }
  filters.forEach(button => button.addEventListener('click', () => {
    filters.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    let count = 0;
    figures.forEach(figure => {
      figure.hidden = button.dataset.mediaFilter !== 'all' && figure.dataset.mediaCategory !== button.dataset.mediaFilter;
      if (!figure.hidden) count++;
    });
    document.querySelector('#press-count').textContent = `${count} archive item${count === 1 ? '' : 's'}`;
  }));
  document.querySelectorAll('[data-press-open]').forEach(link => link.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    opener = link;
    sequence = figures.filter(f => !f.hidden).map(f => f.querySelector('[data-press-open]'));
    let target = sequence.findIndex(a => a.getAttribute('href') === link.getAttribute('href'));
    if (target < 0) { sequence = [link]; target = 0; }
    showItem(target);
    viewer.showModal();
    document.body.classList.add('locked');
    viewer.querySelector('[data-press-close]').focus();
  }));
  previous.addEventListener('click', () => { if (index > 0) showItem(index - 1); });
  next.addEventListener('click', () => { if (index < sequence.length - 1) showItem(index + 1); });
  zoom.addEventListener('click', () => {
    const active = stage.classList.toggle('is-zoomed');
    zoom.setAttribute('aria-pressed', String(active));
    zoom.textContent = active ? 'Fit to screen' : 'Zoom in';
    stage.scrollTop = stage.scrollLeft = 0;
  });
  viewer.querySelector('[data-press-close]').addEventListener('click', () => viewer.close());
  viewer.addEventListener('close', () => {
    document.body.classList.remove('locked');
    resetZoom();
    opener?.focus({preventScroll: true});
  });
  viewer.addEventListener('keydown', event => {
    if (event.key === 'ArrowRight' && index < sequence.length - 1) {
      event.preventDefault(); showItem(index + 1);
    }
    if (event.key === 'ArrowLeft' && index > 0) {
      event.preventDefault(); showItem(index - 1);
    }
  });
  scan.addEventListener('error', () => { position.textContent = 'This scan could not load. Try opening the original image.'; });
})();
