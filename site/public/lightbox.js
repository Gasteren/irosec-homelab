(function () {
  function initLightbox() {
    var images = document.querySelectorAll('.sl-markdown-content img');
    images.forEach(function (img) {
      if (img.dataset.lightboxBound) return;
      img.dataset.lightboxBound = 'true';
      img.classList.add('lightbox-trigger');
      img.addEventListener('click', function () {
        openLightbox(img.src, img.alt);
      });
    });
  }

  function openLightbox(src, alt) {
    var overlay = document.createElement('div');
    overlay.className = 'lightbox-overlay';

    var img = document.createElement('img');
    img.src = src;
    img.alt = alt || '';
    overlay.appendChild(img);

    function close() {
      overlay.remove();
      document.removeEventListener('keydown', onKey);
    }
    function onKey(e) {
      if (e.key === 'Escape') close();
    }

    overlay.addEventListener('click', close);
    document.addEventListener('keydown', onKey);
    document.body.appendChild(overlay);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLightbox);
  } else {
    initLightbox();
  }
})();
