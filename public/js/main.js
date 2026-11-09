// Header-Hintergrund beim Scrollen
const header = document.querySelector('.site-header');
const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 40);
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// Mobile Navigation
const toggle = document.querySelector('.nav-toggle');
const nav = document.getElementById('main-nav');
if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
  });
  nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    nav.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
  }));
}

// Einblend-Animation
const revealEls = document.querySelectorAll('.section-head, .tile, .steps li, .slideshow, .phone-mockup, .contact-btn');
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
  }), { threshold: 0.12 });
  revealEls.forEach(el => { el.classList.add('reveal'); io.observe(el); });
}

// Galerie: Slideshow mit Autoplay, Pfeilen, Vorschaubildern, Wischen und Vollbild
const show = document.querySelector('.slideshow');
if (show) {
  const slides = [...show.querySelectorAll('.slide')];
  const thumbs = [...show.querySelectorAll('.ss-thumb')];
  const backdrop = show.querySelector('.ss-backdrop');
  const counter = show.querySelector('.ss-counter');
  const bar = show.querySelector('.ss-progress span');
  const playBtn = show.querySelector('.ss-play');
  const stage = show.querySelector('.ss-stage');
  const interval = parseInt(show.dataset.interval, 10) || 5000;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const total = slides.length;
  let index = 0, timer = null, userPaused = reduced, hoverPaused = false, inView = false;

  const wrap = i => (i + total) % total;
  const src = i => slides[i].querySelector('a').getAttribute('href');
  const alt = i => slides[i].querySelector('img').alt;

  function render() {
    slides.forEach((s, i) => {
      s.classList.toggle('is-active', i === index);
      // Nachbarbilder vorladen, alle anderen bleiben ungeladen (schnelle Seite)
      s.classList.toggle('is-near', i === wrap(index + 1) || i === wrap(index - 1));
      s.setAttribute('aria-hidden', i === index ? 'false' : 'true');
      s.querySelector('a').tabIndex = i === index ? 0 : -1;
    });
    thumbs.forEach((t, i) => t.setAttribute('aria-current', i === index ? 'true' : 'false'));
    const t = thumbs[index];
    if (t) {
      const row = t.parentElement;
      row.scrollTo({ left: t.offsetLeft - row.clientWidth / 2 + t.clientWidth / 2, behavior: reduced ? 'auto' : 'smooth' });
    }
    backdrop.style.backgroundImage = `url("${src(index)}")`;
    counter.innerHTML = `<b>${index + 1}</b> / ${total}`;
  }

  function startBar() {
    bar.classList.remove('run');
    bar.style.transitionDuration = '0ms';
    bar.style.width = '0';
    void bar.offsetWidth; // Neustart der Animation erzwingen
    if (!running()) return;
    bar.style.transitionDuration = interval + 'ms';
    bar.classList.add('run');
    bar.style.width = '';
  }

  const running = () => !userPaused && !hoverPaused && inView && !document.hidden;

  function schedule() {
    clearTimeout(timer);
    startBar();
    if (running()) timer = setTimeout(() => go(index + 1), interval);
  }

  function go(i) { index = wrap(i); render(); schedule(); }

  function setPaused(p) {
    userPaused = p;
    show.classList.toggle('paused', p);
    playBtn.setAttribute('aria-label', p ? 'Slideshow starten' : 'Slideshow pausieren');
    show.querySelector('.slides').setAttribute('aria-live', p ? 'polite' : 'off');
    schedule();
  }

  show.querySelector('.ss-prev').addEventListener('click', () => go(index - 1));
  show.querySelector('.ss-next').addEventListener('click', () => go(index + 1));
  thumbs.forEach((t, i) => t.addEventListener('click', () => go(i)));
  playBtn.addEventListener('click', () => setPaused(!userPaused));

  // Pause bei Maus über dem Bild oder Tastatur-Fokus
  stage.addEventListener('mouseenter', () => { hoverPaused = true; schedule(); });
  stage.addEventListener('mouseleave', () => { hoverPaused = false; schedule(); });
  show.addEventListener('focusin', () => { hoverPaused = true; schedule(); });
  show.addEventListener('focusout', e => { if (!show.contains(e.relatedTarget)) { hoverPaused = false; schedule(); } });

  // Tastatur: Pfeiltasten
  show.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft') { e.preventDefault(); go(index - 1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); go(index + 1); }
  });

  // Wischen auf dem Handy
  const swipe = (el, onLeft, onRight) => {
    let x0 = null, y0 = 0;
    el.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
    el.addEventListener('touchend', e => {
      if (x0 === null) return;
      const dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
      if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) (dx < 0 ? onLeft : onRight)();
      x0 = null;
    }, { passive: true });
  };
  swipe(stage, () => go(index + 1), () => go(index - 1));

  // Nur abspielen, wenn die Galerie sichtbar ist und der Tab aktiv
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([e]) => { inView = e.isIntersecting; schedule(); }, { threshold: 0.35 }).observe(stage);
  } else { inView = true; }
  document.addEventListener('visibilitychange', schedule);

  // Vollbild (Lightbox) mit Blättern
  slides.forEach((s, i) => s.querySelector('a').addEventListener('click', e => {
    e.preventDefault();
    openLightbox(i);
  }));

  function openLightbox(start) {
    let li = start;
    const last = document.activeElement;
    const box = document.createElement('div');
    box.className = 'lightbox';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'Bild in Vollansicht');
    box.innerHTML = `
      <img src="" alt="">
      <button type="button" class="ss-btn ss-prev" aria-label="Vorheriges Bild"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>
      <button type="button" class="ss-btn ss-next" aria-label="Nächstes Bild"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>
      <button type="button" class="ss-btn lb-close" aria-label="Schliessen"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
      <p class="lb-caption"></p>`;
    const img = box.querySelector('img');
    const cap = box.querySelector('.lb-caption');
    const show_ = i => {
      li = wrap(i);
      img.src = src(li); img.alt = alt(li);
      img.style.animation = 'none'; void img.offsetWidth; img.style.animation = '';
      cap.textContent = `${alt(li)} · ${li + 1} / ${total}`;
      new Image().src = src(wrap(li + 1)); // nächstes Bild vorladen
    };
    const close = () => {
      box.remove();
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = '';
      go(li); // Slideshow springt zum zuletzt angesehenen Bild
      if (last) last.focus({ preventScroll: true });
    };
    const onKey = ev => {
      if (ev.key === 'Escape') close();
      if (ev.key === 'ArrowLeft') show_(li - 1);
      if (ev.key === 'ArrowRight') show_(li + 1);
    };
    box.querySelector('.ss-prev').addEventListener('click', ev => { ev.stopPropagation(); show_(li - 1); });
    box.querySelector('.ss-next').addEventListener('click', ev => { ev.stopPropagation(); show_(li + 1); });
    box.querySelector('.lb-close').addEventListener('click', close);
    box.addEventListener('click', ev => { if (ev.target === box) close(); });
    swipe(box, () => show_(li + 1), () => show_(li - 1));
    document.addEventListener('keydown', onKey);
    document.body.style.overflow = 'hidden';
    document.body.appendChild(box);
    show_(li);
    box.querySelector('.lb-close').focus();
  }

  if (reduced) setPaused(true);
  render();
  schedule();
}

// Jahr im Footer
const y = document.getElementById('year');
if (y) y.textContent = new Date().getFullYear();

