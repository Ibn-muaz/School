/**
 * Sanga Portal — Main JavaScript
 * Sidebar toggle (desktop collapse + mobile drawer), dark mode,
 * notification bell, dropdown, toast system, swipe-to-close
 */

(function () {
  'use strict';

  const isMobile  = () => window.innerWidth <= 768;
  const isTablet  = () => window.innerWidth > 768 && window.innerWidth <= 1024;

  // ── Theme ──────────────────────────────────────────────────
  const html      = document.documentElement;
  const THEME_KEY = 'sanga_theme';

  function applyTheme(theme) {
    html.setAttribute('data-theme', theme);
    const moonIcon = document.getElementById('theme-icon-moon');
    const sunIcon  = document.getElementById('theme-icon-sun');
    const ddIcon   = document.getElementById('dd-theme-icon');
    const ddLabel  = document.getElementById('dd-theme-label');

    if (theme === 'dark') {
      if (moonIcon) moonIcon.style.display = 'none';
      if (sunIcon)  sunIcon.style.display  = 'block';
      if (ddLabel)  ddLabel.textContent = 'Light Mode';
      if (ddIcon)   ddIcon.setAttribute('data-lucide', 'sun');
    } else {
      if (moonIcon) moonIcon.style.display = 'block';
      if (sunIcon)  sunIcon.style.display  = 'none';
      if (ddLabel)  ddLabel.textContent = 'Dark Mode';
      if (ddIcon)   ddIcon.setAttribute('data-lucide', 'moon');
    }
    if (typeof lucide !== 'undefined') lucide.createIcons();
  }

  function toggleTheme() {
    const current = html.getAttribute('data-theme') || 'light';
    const next    = current === 'dark' ? 'light' : 'dark';
    localStorage.setItem(THEME_KEY, next);
    applyTheme(next);
    fetch('/profile/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: `theme_preference=${next}&_theme_only=1`,
    }).catch(() => {});
  }

  const savedTheme = localStorage.getItem(THEME_KEY) || html.getAttribute('data-theme') || 'light';
  applyTheme(savedTheme);

  document.getElementById('theme-toggle-btn')?.addEventListener('click', toggleTheme);
  document.getElementById('dropdown-theme-btn')?.addEventListener('click', toggleTheme);


  // ── Sidebar ─────────────────────────────────────────────────
  const sidebar     = document.getElementById('sidebar');
  const overlay     = document.getElementById('sidebar-overlay');
  const toggleBtn   = document.getElementById('sidebar-toggle-btn');
  const hamburgerBtn= document.getElementById('mobile-menu-btn');
  const SIDEBAR_KEY = 'sanga_sidebar_collapsed';

  // ── Desktop / Tablet collapse ──
  function setCollapsed(collapsed) {
    sidebar?.classList.toggle('collapsed', collapsed);
    // update toggle icon direction
    const icon = toggleBtn?.querySelector('i[data-lucide]');
    if (icon) {
      icon.setAttribute('data-lucide', collapsed ? 'panel-left-open' : 'panel-left-close');
      if (typeof lucide !== 'undefined') lucide.createIcons();
    }
  }

  // Restore on desktop load
  if (!isMobile()) {
    const wasCollapsed = localStorage.getItem(SIDEBAR_KEY) === 'true';
    setCollapsed(wasCollapsed);
  }

  toggleBtn?.addEventListener('click', () => {
    if (isMobile()) return; // on mobile the toggle closes the drawer instead
    const collapsed = !sidebar.classList.contains('collapsed');
    setCollapsed(collapsed);
    localStorage.setItem(SIDEBAR_KEY, collapsed);
  });


  // ── Mobile drawer open / close ──
  function openDrawer() {
    sidebar?.classList.add('mobile-open');
    overlay?.classList.add('active');
    document.body.style.overflow = 'hidden'; // prevent scroll behind drawer
  }

  function closeDrawer() {
    sidebar?.classList.remove('mobile-open');
    overlay?.classList.remove('active');
    document.body.style.overflow = '';
  }

  hamburgerBtn?.addEventListener('click', openDrawer);
  overlay?.addEventListener('click', closeDrawer);

  // X close button (mobile)
  document.getElementById('sidebar-close-btn')?.addEventListener('click', closeDrawer);


  // Close on sidebar collapse button (mobile)
  toggleBtn?.addEventListener('click', () => {
    if (isMobile()) closeDrawer();
  });

  // Close drawer when a nav link is clicked on mobile
  sidebar?.querySelectorAll('.nav-item[href]').forEach(link => {
    link.addEventListener('click', () => {
      if (isMobile()) closeDrawer();
    });
  });

  // ── Swipe-to-close (touch support) ──
  let touchStartX = 0;
  let touchStartY = 0;

  document.addEventListener('touchstart', (e) => {
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
  }, { passive: true });

  document.addEventListener('touchend', (e) => {
    if (!isMobile()) return;
    const dx = e.changedTouches[0].clientX - touchStartX;
    const dy = e.changedTouches[0].clientY - touchStartY;
    // Swipe left ≥60px and mostly horizontal → close drawer
    if (dx < -60 && Math.abs(dy) < 60 && sidebar?.classList.contains('mobile-open')) {
      closeDrawer();
    }
    // Swipe right ≥60px from left edge → open drawer
    if (dx > 60 && Math.abs(dy) < 60 && touchStartX < 30 && !sidebar?.classList.contains('mobile-open')) {
      openDrawer();
    }
  }, { passive: true });

  // ── Tablet: expand on hover (icon-only mode) ──
  if (isTablet()) {
    sidebar?.addEventListener('mouseenter', () => {
      sidebar.classList.add('mobile-open');
    });
    sidebar?.addEventListener('mouseleave', () => {
      sidebar.classList.remove('mobile-open');
    });
  }

  // Re-run tablet detection on resize
  window.addEventListener('resize', () => {
    if (!isMobile()) {
      closeDrawer(); // ensure overlay cleared on resize to desktop
    }
  });


  // ── Dropdowns ──────────────────────────────────────────────
  function initDropdown(btnId, menuId) {
    const btn  = document.getElementById(btnId);
    const menu = document.getElementById(menuId);
    if (!btn || !menu) return;

    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = menu.classList.contains('open');
      document.querySelectorAll('.dropdown-menu.open, .notif-dropdown.open')
              .forEach(el => el.classList.remove('open'));
      if (!isOpen) menu.classList.add('open');
    });
  }

  initDropdown('profile-btn', 'profile-dropdown');
  initDropdown('notif-btn',   'notif-dropdown');

  document.addEventListener('click', () => {
    document.querySelectorAll('.dropdown-menu.open, .notif-dropdown.open')
            .forEach(el => el.classList.remove('open'));
  });


  // ── Toast Notification System ──────────────────────────────
  window.showToast = function (title, message = '', type = 'info', duration = 4000) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const icons  = { info: 'ℹ️', success: '✅', warning: '⚠️', error: '❌' };
    const toast  = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
      <span class="toast-icon">${icons[type] || icons.info}</span>
      <div class="toast-body">
        <div class="toast-title">${title}</div>
        ${message ? `<div class="toast-message">${message}</div>` : ''}
      </div>
      <button onclick="this.closest('.toast').remove()"
              style="background:none;border:none;cursor:pointer;padding:0;color:var(--text-muted);font-size:18px;line-height:1;margin-left:8px;">&times;</button>
    `;
    container.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('removing');
      toast.addEventListener('animationend', () => toast.remove());
    }, duration);
  };

  // Auto-dismiss flash messages after 5s
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 400ms';
      alert.style.opacity    = '0';
      setTimeout(() => alert.remove(), 400);
    }, 5000);
  });


  // ── CSRF Cookie Helper ──────────────────────────────────────
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      for (const cookie of document.cookie.split(';')) {
        const c = cookie.trim();
        if (c.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(c.slice(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }


  // ── Active nav link highlight ──────────────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-item[href]').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // Re-init lucide icons
  if (typeof lucide !== 'undefined') lucide.createIcons();

})();
