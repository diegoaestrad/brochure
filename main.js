const nav = document.querySelector('.site-nav');
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');
const stickyCta = document.querySelector('.sticky-cta');
const portfolioGrid = document.getElementById('portfolio-grid');
const filterChips = document.querySelectorAll('.filter-chip');
const contactForm = document.getElementById('quote-form');
const formFeedback = document.getElementById('form-feedback');

const unsplash = (id, w = 640) =>
  `https://images.unsplash.com/${id}?auto=format&fit=crop&w=${w}&q=80`;

// Nav scroll
const onScroll = () => {
  if (nav) nav.classList.toggle('scrolled', window.scrollY > 20);
  if (stickyCta) {
    const show = window.scrollY > 500;
    stickyCta.classList.toggle('visible', show);
    document.body.classList.toggle('has-sticky-cta', show);
  }
};
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// Mobile menu
if (menuToggle && navLinks) {
  menuToggle.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    menuToggle.setAttribute('aria-expanded', String(open));
  });
  navLinks.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      menuToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// Reveal on scroll
const revealEls = document.querySelectorAll('.reveal');
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
);
revealEls.forEach((el) => revealObserver.observe(el));

const renderPortfolioCard = (d) => `
      <article class="portfolio-card reveal" data-category="${d.category}">
        <a href="${d.slug}/index.html" target="_blank" rel="noopener">
          <div class="portfolio-thumb">
            <img src="${unsplash(d.hero)}" alt="${d.name} demo preview" loading="lazy" width="640" height="400" />
          </div>
          <div class="portfolio-body">
            <div class="portfolio-meta"><span>${d.emoji}</span><span>${d.category}</span></div>
            <h3>${d.name}</h3>
            <p>${d.tagline}</p>
            <span class="btn btn-ghost">View live demo →</span>
          </div>
        </a>
      </article>`;

const loadPortfolio = async () => {
  if (!portfolioGrid) return;

  let demos = window.PORTFOLIO_DEMOS;

  if (!demos || !demos.length) {
    try {
      const res = await fetch('catalog.json');
      if (res.ok) {
        const data = await res.json();
        demos = data.demos;
      }
    } catch {
      /* file:// or offline — embedded data required */
    }
  }

  if (!demos || !demos.length) {
    portfolioGrid.innerHTML =
      '<p style="color:var(--muted);text-align:center;grid-column:1/-1">Portfolio data missing. Ensure portfolio-data.js is loaded.</p>';
    return;
  }

  portfolioGrid.innerHTML = demos.map(renderPortfolioCard).join('');
  portfolioGrid.querySelectorAll('.reveal').forEach((el) => revealObserver.observe(el));
};

loadPortfolio();

// Portfolio filters
filterChips.forEach((chip) => {
  chip.addEventListener('click', () => {
    filterChips.forEach((c) => {
      c.classList.remove('active');
      c.setAttribute('aria-pressed', 'false');
    });
    chip.classList.add('active');
    chip.setAttribute('aria-pressed', 'true');
    const filter = chip.dataset.filter;
    document.querySelectorAll('.portfolio-card').forEach((card) => {
      const match = filter === 'all' || card.dataset.category === filter;
      card.classList.toggle('hidden', !match);
    });
  });
});

// Quote buttons → contact + prefill service
document.querySelectorAll('[data-quote]').forEach((btn) => {
  btn.addEventListener('click', () => {
    const service = btn.getAttribute('data-quote');
    const select = document.getElementById('service');
    const message = document.getElementById('message');
    if (select && service) select.value = service;
    if (message && !message.value) {
      message.value = `Hi, I'm interested in: ${service}. Please send a quote.`;
    }
    document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' });
  });
});

// Contact form
if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = contactForm.querySelector('#name')?.value?.trim();
    const email = contactForm.querySelector('#email')?.value?.trim();
    if (!name || !email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      if (formFeedback) {
        formFeedback.textContent = 'Please enter a valid name and email.';
        formFeedback.className = 'form-feedback error';
      }
      return;
    }
    if (formFeedback) {
      formFeedback.textContent = 'Thank you! Your request was received. We will reply shortly.';
      formFeedback.className = 'form-feedback success';
    }
    contactForm.reset();
  });
}
