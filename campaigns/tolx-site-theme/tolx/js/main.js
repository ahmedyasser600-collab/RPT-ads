// ============================================
// TOLX. — Main JavaScript
// ============================================

// Progressive enhancement gate: mark that JS is running so the CSS will
// hide .fade-in elements for the scroll animation. If this line never runs
// (JS blocked/errored), .fade-in stays visible by default — no blank sections.
document.documentElement.classList.add('js');

// Scroll fade-in observer
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

// Safety net: if anything is still hidden a few seconds after load (observer
// missed it, element taller than viewport, mobile throttling), reveal it.
window.addEventListener('load', () => {
  setTimeout(() => {
    document.querySelectorAll('.fade-in:not(.visible)').forEach(el => {
      const r = el.getBoundingClientRect();
      // Reveal anything at or above the current fold that never triggered.
      if (r.top < window.innerHeight) el.classList.add('visible');
    });
  }, 1200);
});

// Word flip width calculation
function setFlipWidth() {
  document.querySelectorAll('.flip-wrapper').forEach(wrapper => {
    const sizer = wrapper.querySelector('.flip-sizer');
    const words = wrapper.querySelectorAll('.flip-word');
    if (!sizer) return;
    let maxW = sizer.offsetWidth;
    words.forEach(w => {
      w.style.position = 'absolute';
      w.style.visibility = 'hidden';
      w.style.display = 'inline';
      w.style.opacity = '1';
      const wW = w.offsetWidth;
      if (wW > maxW) maxW = wW;
      w.style.position = '';
      w.style.visibility = '';
      w.style.display = '';
      w.style.opacity = '';
    });
    wrapper.style.width = maxW + 'px';
  });
}

// The hidden .flip-sizer already reserves the width in CSS; the measurement only
// refines it, so run it after load instead of during first render (it forces layout).
if (document.querySelector('.flip-wrapper')) {
  window.addEventListener('load', () => requestAnimationFrame(setFlipWidth));
  window.addEventListener('resize', setFlipWidth);
}

// Mobile menu toggle
const mobileToggle = document.querySelector('.nav-mobile-toggle');
const mobileMenu = document.querySelector('.nav-mobile');

if (mobileToggle && mobileMenu) {
  const setMenuState = (open) => {
    mobileMenu.classList.toggle('open', open);
    mobileToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.classList.toggle('menu-open', open);
    const spans = mobileToggle.querySelectorAll('span');
    if (open) {
      spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
      spans[1].style.opacity = '0';
      spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
    } else {
      spans[0].style.transform = '';
      spans[1].style.opacity = '';
      spans[2].style.transform = '';
    }
  };

  mobileToggle.addEventListener('click', () => {
    setMenuState(!mobileMenu.classList.contains('open'));
  });

  // Close menu when a link inside it is tapped
  mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => setMenuState(false));
  });

  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && mobileMenu.classList.contains('open')) {
      setMenuState(false);
    }
  });
}

// Nav scroll state
const navEl = document.querySelector('.nav');
if (navEl) {
  let ticking = false;
  const updateNav = () => {
    if (window.scrollY > 24) {
      navEl.classList.add('scrolled');
    } else {
      navEl.classList.remove('scrolled');
    }
    ticking = false;
  };
  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(updateNav);
      ticking = true;
    }
  }, { passive: true });
  updateNav();
}

// Pause the hero's looping effects while it is off screen (saves battery/CPU)
const heroEl = document.querySelector('.hero');
if (heroEl && 'IntersectionObserver' in window) {
  new IntersectionObserver((entries) => {
    entries.forEach(entry => heroEl.classList.toggle('fx-paused', !entry.isIntersecting));
  }).observe(heroEl);
}

// Scroll progress hairline
const progressEl = document.querySelector('.scroll-progress');
if (progressEl) {
  let pTick = false;
  const updateProgress = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    progressEl.style.setProperty('--p', max > 0 ? Math.min(1, window.scrollY / max) : 0);
    pTick = false;
  };
  window.addEventListener('scroll', () => {
    if (!pTick) { window.requestAnimationFrame(updateProgress); pTick = true; }
  }, { passive: true });
  updateProgress();
}

// Card spotlight + HUD corners: mark card components and track the pointer
// (fine pointers only, so touch devices don't get a stuck highlight).
const fxSelector = '.card, .diag-card, .sol-card, .op-block, .value-card, .step-card, .module-card, .blog-card, .pricing-card';
document.querySelectorAll(fxSelector).forEach(el => el.classList.add('fx-card'));
if (window.matchMedia('(pointer: fine)').matches) {
  document.addEventListener('pointermove', (e) => {
    const card = e.target.closest('.fx-card');
    if (!card) return;
    const r = card.getBoundingClientRect();
    card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    card.style.setProperty('--my', (e.clientY - r.top) + 'px');
  }, { passive: true });
}

// Consent manager / analytics adapter must explicitly enable this bridge.
window.tolxMeasure = function (event) {
  if (!['enquiry_saved', 'assessment_saved', 'whatsapp_click', 'phone_click'].includes(event)) return;
  if (window.TOLX_ANALYTICS_CONSENT !== true || typeof window.TOLX_ANALYTICS_SEND !== 'function') return;
  window.TOLX_ANALYTICS_SEND(event, {source: 'tolx_theme'});
};
document.addEventListener('click', function (e) {
  var a = e.target.closest('a[href]'); if (!a) return;
  if (/^https:\/\/wa.me\//.test(a.href)) window.tolxMeasure('whatsapp_click');
  else if (/^tel:/.test(a.getAttribute('href'))) window.tolxMeasure('phone_click');
});
