(function () {
  var STORAGE_PREFIX = 'bsides:notes:read:';

  function setActiveNav() {
    var page = document.body.getAttribute('data-page');
    if (!page) return;
    var link = document.querySelector('a[data-nav="' + page + '"]');
    if (link) {
      link.style.color = 'var(--b-ink)';
      link.style.borderBottom = '1.5px solid var(--b-olive)';
      link.style.paddingBottom = '2px';
    }
  }

  function markListReadStates() {
    var rows = document.querySelectorAll('[data-note-step]');
    rows.forEach(function (row) {
      var step = row.getAttribute('data-note-step');
      var read = localStorage.getItem(STORAGE_PREFIX + step) === '1';
      var badge = row.querySelector('[data-read-badge]');
      if (badge) badge.style.display = read ? 'inline-flex' : 'none';
      if (read) row.setAttribute('data-read', '1');
    });
  }

  function trackCurrentStep() {
    var current = document.body.getAttribute('data-current-step');
    if (!current) return;
    var key = STORAGE_PREFIX + current;
    if (localStorage.getItem(key) === '1') return;

    var marked = false;
    function mark() {
      if (marked) return;
      marked = true;
      localStorage.setItem(key, '1');
    }
    function onScroll() {
      var h = document.documentElement;
      var scrolled = (h.scrollTop + h.clientHeight) / h.scrollHeight;
      if (scrolled >= 0.8) mark();
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    setTimeout(mark, 30000); // 30초 체류
  }

  function init() {
    setActiveNav();
    markListReadStates();
    trackCurrentStep();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
