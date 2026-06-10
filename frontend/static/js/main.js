/* =========================================================
   MENTORLINK — main.js
   Projet universitaire IFRI-UAC — 2026
   Uniquement des utilitaires côté client.
   La navigation est gérée par Django ({% url %}).
   ========================================================= */

"use strict";

/* ── 1. Afficher / masquer un mot de passe ───────────────── */
function togglePwd(fieldId, btn) {
  const field = document.getElementById(fieldId);
  if (!field) return;
  const icon = btn.querySelector('i');
  if (field.type === 'password') {
    field.type    = 'text';
    if (icon) icon.className = 'bi bi-eye-slash';
  } else {
    field.type    = 'password';
    if (icon) icon.className = 'bi bi-eye';
  }
}

/* ── 2. Sidebar mobile (toggle) ──────────────────────────── */
document.addEventListener('DOMContentLoaded', function () {

  // Bouton hamburger → ouvrir/fermer la sidebar sur mobile
  const toggleBtn = document.getElementById('sidebarToggle');
  const sidebar   = document.querySelector('.ml-sidebar');
  const overlay   = document.getElementById('sidebarOverlay');

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', function () {
      sidebar.classList.toggle('open');
      if (overlay) overlay.classList.toggle('d-none');
    });
  }
  if (overlay) {
    overlay.addEventListener('click', function () {
      if (sidebar) sidebar.classList.remove('open');
      overlay.classList.add('d-none');
    });
  }

  /* ── 3. Auto-dismiss des alertes Django après 5s ────────── */
  document.querySelectorAll('.alert.fade.show').forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  /* ── 4. Scroll automatique vers le bas dans le chat ─────── */
  const chatBody = document.getElementById('chatBody');
  if (chatBody) {
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  /* ── 5. Filtrage en direct des conversations (message.html) */
  const searchConv = document.getElementById('searchConv');
  if (searchConv) {
    searchConv.addEventListener('input', function () {
      const q = this.value.toLowerCase();
      document.querySelectorAll('#convList a').forEach(function (item) {
        const name    = item.querySelector('h6')?.textContent.toLowerCase() || '';
        const preview = item.querySelector('p')?.textContent.toLowerCase()  || '';
        item.style.display = (name.includes(q) || preview.includes(q)) ? '' : 'none';
      });
    });
  }

  /* ── 6. Grille de disponibilités cliquable (profil / modif) */
  document.querySelectorAll('.avail-cell[data-toggle="avail"]').forEach(function (cell) {
    cell.addEventListener('click', function () {
      this.classList.toggle('selected');
      const input = this.querySelector('input[type="checkbox"]');
      if (input) input.checked = !input.checked;
    });
  });

  /* ── 7. Confirmation avant déconnexion ───────────────────── */
  document.querySelectorAll('[data-confirm-logout]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      if (!confirm('Voulez-vous vous déconnecter ?')) {
        e.preventDefault();
      }
    });
  });

  /* ── 8. Limite de caractères sur les textarea ────────────── */
  document.querySelectorAll('textarea[maxlength]').forEach(function (ta) {
    const max     = parseInt(ta.getAttribute('maxlength'), 10);
    const counter = document.createElement('small');
    counter.className = 'text-muted-soft d-block text-end mt-1';
    counter.textContent = '0 / ' + max;
    ta.after(counter);
    ta.addEventListener('input', function () {
      counter.textContent = this.value.length + ' / ' + max;
    });
  });

  /* ── 9. Activer Bootstrap tooltips ──────────────────────── */
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

});
