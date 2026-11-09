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
const revealEls = document.querySelectorAll('.section-head, .card, .steps li, .gallery a, .about > *, .contact > *');
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
  }), { threshold: 0.12 });
  revealEls.forEach(el => { el.classList.add('reveal'); io.observe(el); });
}

// Galerie-Lightbox
document.querySelectorAll('.gallery a').forEach(link => link.addEventListener('click', e => {
  e.preventDefault();
  const box = document.createElement('div');
  box.className = 'lightbox';
  box.innerHTML = `<img src="${link.getAttribute('href')}" alt="${link.querySelector('img').alt}">`;
  box.addEventListener('click', () => box.remove());
  document.addEventListener('keydown', function esc(ev) { if (ev.key === 'Escape') { box.remove(); document.removeEventListener('keydown', esc); } });
  document.body.appendChild(box);
}));

// Kontaktformular (sendet an kontakt.php, ohne Seitenwechsel)
const form = document.querySelector('.contact-form');
if (form) {
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const status = form.querySelector('.form-status');
    const btn = form.querySelector('button[type=submit]');
    btn.disabled = true;
    status.textContent = 'Wird gesendet …';
    try {
      const res = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } });
      const data = await res.json();
      status.textContent = data.message;
      if (data.ok) form.reset();
    } catch {
      status.textContent = 'Senden fehlgeschlagen. Bitte rufen Sie uns an oder schreiben Sie eine E-Mail.';
    }
    btn.disabled = false;
  });
}

// Jahr im Footer
const y = document.getElementById('year');
if (y) y.textContent = new Date().getFullYear();
