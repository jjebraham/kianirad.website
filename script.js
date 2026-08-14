/* KIANIRAD Web Design & Development — shared site script */

document.addEventListener('DOMContentLoaded', function () {
  /* --- Mobile navigation toggle --- */
  var toggle = document.querySelector('.nav-toggle');
  var navList = document.querySelector('.site-nav ul');
  if (toggle && navList) {
    toggle.addEventListener('click', function () {
      navList.classList.toggle('open');
    });
  }

  /* --- Current year in footer --- */
  var yearEl = document.getElementById('year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  /* --- AJAX forms (FormSubmit) ---
     Submits without leaving the page and shows "Thanks for submitting!" */
  document.querySelectorAll('form.ajax-form').forEach(function (form) {
    form.addEventListener('submit', function (event) {
      event.preventDefault();

      var status = form.querySelector('.form-status');
      var button = form.querySelector('.btn-submit');
      if (button) {
        button.disabled = true;
        button.textContent = 'Sending...';
      }
      if (status) {
        status.textContent = '';
      }

      fetch(form.action, {
        method: 'POST',
        headers: { Accept: 'application/json' },
        body: new FormData(form)
      })
        .then(function (res) {
          if (!res.ok) {
            throw new Error('Request failed');
          }
          if (status) {
            status.textContent = 'Thanks for submitting!';
          }
          form.reset();
        })
        .catch(function () {
          if (status) {
            status.style.color = '#b00020';
            status.textContent = 'Something went wrong. Please email kianirad2020@gmail.com directly.';
          }
        })
        .finally(function () {
          if (button) {
            button.disabled = false;
            button.textContent = button.dataset.label || button.textContent.replace('Sending...', 'Submit');
          }
        });
    });

    // remember original button label
    var btn = form.querySelector('.btn-submit');
    if (btn) {
      btn.dataset.label = btn.textContent;
    }
  });
});
