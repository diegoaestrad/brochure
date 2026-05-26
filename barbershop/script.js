const navbar = document.querySelector('.navbar');
const menuToggle = document.querySelector('.menu-toggle');
const navMenu = document.querySelector('#nav-menu');
const navMenuLinks = document.querySelectorAll('#nav-menu a');
const yearElement = document.querySelector('#year');
const form = document.querySelector('#contact-form');
const feedback = document.querySelector('#form-feedback');

const updateNavbarState = () => {
  if (!navbar) return;
  const shouldBeScrolled = window.scrollY > 24;
  navbar.classList.toggle('scrolled', shouldBeScrolled);
};

const closeMobileMenu = () => {
  if (!menuToggle || !navMenu) return;
  menuToggle.setAttribute('aria-expanded', 'false');
  navMenu.classList.remove('open');
};

if (menuToggle && navMenu) {
  menuToggle.addEventListener('click', () => {
    const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
    menuToggle.setAttribute('aria-expanded', String(!isExpanded));
    navMenu.classList.toggle('open', !isExpanded);
  });

  navMenuLinks.forEach((link) => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 760) {
        closeMobileMenu();
      }
    });
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 760) {
      closeMobileMenu();
    }
  });
}

window.addEventListener('scroll', updateNavbarState, { passive: true });
updateNavbarState();

if (yearElement) {
  yearElement.textContent = new Date().getFullYear();
}

const setFeedback = (message, type) => {
  if (!feedback) return;
  feedback.textContent = message;
  feedback.classList.remove('error', 'success');
  if (type) {
    feedback.classList.add(type);
  }
};

const validateEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
const validatePhone = (phone) => /^\+?[0-9\s\-()]{7,20}$/.test(phone);

if (form) {
  form.addEventListener('submit', (event) => {
    event.preventDefault();

    const nameInput = form.querySelector('#name');
    const emailInput = form.querySelector('#email');
    const phoneInput = form.querySelector('#phone');
    const messageInput = form.querySelector('#message');

    if (!nameInput || !emailInput || !phoneInput || !messageInput) return;

    [nameInput, emailInput, phoneInput, messageInput].forEach((field) =>
      field.classList.remove('invalid')
    );

    const name = nameInput.value.trim();
    const email = emailInput.value.trim();
    const phone = phoneInput.value.trim();
    const message = messageInput.value.trim();

    const errors = [];

    if (name.length < 2) {
      errors.push({ field: nameInput, message: 'Please enter your full name.' });
    }

    if (!validateEmail(email)) {
      errors.push({ field: emailInput, message: 'Please provide a valid email address.' });
    }

    if (phone.length > 0 && !validatePhone(phone)) {
      errors.push({ field: phoneInput, message: 'Please enter a valid phone number.' });
    }

    if (message.length < 10) {
      errors.push({
        field: messageInput,
        message: 'Please include at least 10 characters in your message.',
      });
    }

    if (errors.length > 0) {
      errors.forEach((error) => error.field.classList.add('invalid'));
      errors[0].field.focus();
      setFeedback(errors[0].message, 'error');
      return;
    }

    setFeedback('Thanks! Your inquiry has been sent. We will respond shortly.', 'success');
    form.reset();
  });
}
