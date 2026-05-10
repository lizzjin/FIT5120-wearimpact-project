<template>
  <nav class="navbar" :class="{ 'is-dark': isDarkRoute }" ref="navRef">
    <router-link to="/" class="logo">
      <span class="logo-mark">Wear</span><span class="logo-tail">Impact</span>
    </router-link>

    <!-- Desktop nav links -->
    <div class="nav-links">
      <router-link
        v-for="link in navLinks"
        :key="link.to"
        :to="link.to"
        class="nav-link"
      >
        {{ link.label }}
      </router-link>
    </div>

    <!-- Mobile hamburger button -->
    <button
      class="hamburger"
      :class="{ open: mobileOpen }"
      @click="mobileOpen = !mobileOpen"
      :aria-expanded="mobileOpen"
      aria-label="Toggle navigation menu"
    >
      <span class="hamburger-line"></span>
      <span class="hamburger-line"></span>
      <span class="hamburger-line"></span>
    </button>

    <!-- Mobile overlay menu -->
    <Transition name="mobile-menu">
      <div v-if="mobileOpen" class="mobile-overlay" @click.self="mobileOpen = false">
        <div class="mobile-panel">
          <router-link
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="mobile-link"
            @click="mobileOpen = false"
          >
            {{ link.label }}
          </router-link>
        </div>
      </div>
    </Transition>
  </nav>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const mobileOpen = ref(false)
const route = useRoute()
const navRef = ref(null)

// Knowledge Hub no longer uses the dark glass theme — it now shares the
// unified cream canvas with the rest of the site, so the navbar stays light.
const isDarkRoute = computed(() => false)

// Close mobile menu on route change
watch(() => route.path, () => { mobileOpen.value = false })

const navLinks = [
  { to: '/', label: 'Home' },
  { to: '/eco-shop', label: 'Act' },
  { to: '/knowledge', label: 'Discovery' },
  { to: '/brand-search', label: 'Evaluate' },
  { to: '/wardrobe', label: 'My Wardrobe' },
]
</script>

<style scoped>
/* ── Navbar bar ────────────────────────────────────────────────────────── */
.navbar {
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 32px;
  background: rgba(250, 247, 242, 0.88);
  backdrop-filter: blur(16px) saturate(1.6);
  -webkit-backdrop-filter: blur(16px) saturate(1.6);
  border-bottom: 1px solid var(--color-border);
  transition: box-shadow var(--transition-base);
}

/* ── Logo ──────────────────────────────────────────────────────────────── */
.logo {
  font-size: 22px;
  font-weight: 900;
  letter-spacing: -0.3px;
  text-decoration: none;
  transition: opacity var(--transition-base);
  display: inline-flex;
  line-height: 1;
}
.logo:hover { opacity: 0.85; }

.logo-mark { color: var(--color-primary-text); }
.logo-tail { color: var(--color-text); }

/* ── Desktop links ─────────────────────────────────────────────────────── */
.nav-links {
  display: flex;
  gap: 4px;
  align-items: center;
}

.nav-link {
  font-weight: 600;
  font-size: 15px;
  color: var(--color-text-muted);
  text-decoration: none;
  padding: 8px 16px;
  border-radius: var(--radius-pill);
  position: relative;
  transition: color var(--transition-base), background-color var(--transition-base), transform var(--transition-base);
}

/* Green-tinted nav hover */
.nav-link:hover {
  color: var(--color-text);
  background-color: rgba(211, 242, 192, 0.4);
}

/* Active: lime pill */
.nav-link.router-link-active {
  color: var(--color-primary-text);
  font-weight: 700;
  background-color: var(--color-primary);
}

.nav-link.router-link-active:hover {
  background-color: var(--color-primary);
  transform: scale(1.05);
}

/* ── Hamburger (hidden on desktop) ─────────────────────────────────────── */
.hamburger {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 36px;
  height: 36px;
  padding: 6px;
  border: none;
  background: transparent;
  cursor: pointer;
  border-radius: 8px;
  transition: background var(--transition-base);
}

.hamburger:hover { background: var(--color-surface-alt); }

.hamburger-line {
  display: block;
  width: 100%;
  height: 2px;
  background: var(--color-text);
  border-radius: 2px;
  transition: transform 300ms ease, opacity 200ms ease;
  transform-origin: center;
}

.hamburger.open .hamburger-line:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}
.hamburger.open .hamburger-line:nth-child(2) {
  opacity: 0;
}
.hamburger.open .hamburger-line:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

/* ── Mobile overlay (hidden on desktop) ────────────────────────────────── */
.mobile-overlay {
  display: none;
}

/* ── Mobile menu transition ────────────────────────────────────────────── */
.mobile-menu-enter-active { transition: opacity 250ms ease; }
.mobile-menu-leave-active { transition: opacity 200ms ease; }
.mobile-menu-enter-from,
.mobile-menu-leave-to { opacity: 0; }

.mobile-menu-enter-active .mobile-panel {
  animation: slideDown 280ms cubic-bezier(0.22, 1, 0.36, 1);
}
.mobile-menu-leave-active .mobile-panel {
  animation: slideUp 200ms ease forwards;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-12px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes slideUp {
  from { opacity: 1; transform: translateY(0); }
  to   { opacity: 0; transform: translateY(-12px); }
}

/* ── Dark variant (active on /knowledge route) ─────────────────────────── */
.navbar.is-dark {
  background: rgba(10, 14, 26, 0.6);
  border-bottom-color: rgba(255, 255, 255, 0.08);
}

.navbar.is-dark .logo .logo-mark {
  color: var(--color-kh-accent);
}

.navbar.is-dark .logo .logo-tail {
  color: var(--color-kh-text);
}

.navbar.is-dark .nav-link {
  color: rgba(255, 255, 255, 0.62);
}

.navbar.is-dark .nav-link:hover {
  color: var(--color-kh-text);
  background-color: rgba(255, 255, 255, 0.06);
}

.navbar.is-dark .nav-link.router-link-active {
  color: var(--color-primary-text);
  background-color: var(--color-kh-accent);
}

.navbar.is-dark .hamburger:hover {
  background: rgba(255, 255, 255, 0.06);
}

.navbar.is-dark .hamburger-line {
  background: var(--color-kh-text);
}

/* ── Responsive ────────────────────────────────────────────────────────── */
@media (max-width: 768px) {
  .navbar {
    padding: 12px 20px;
  }

  .nav-links { display: none; }
  .hamburger { display: flex; }

  .mobile-overlay {
    display: block;
    position: fixed;
    inset: 0;
    top: 57px; /* navbar height */
    z-index: 49;
    background: rgba(10, 18, 32, 0.3);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
  }

  .mobile-panel {
    background: var(--color-surface);
    border-bottom: 1px solid var(--color-border);
    box-shadow: 0 12px 32px rgba(14, 15, 12, 0.12);
    padding: 8px 16px 16px;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .mobile-link {
    display: block;
    padding: 14px 16px;
    font-size: 16px;
    font-weight: 500;
    color: var(--color-text-muted);
    text-decoration: none;
    border-radius: 12px;
    transition: color var(--transition-base), background var(--transition-base);
  }

  .mobile-link:hover,
  .mobile-link:active {
    color: var(--color-text);
    background: var(--color-surface-alt);
  }

  .mobile-link.router-link-active {
    color: var(--color-primary-text);
    font-weight: 700;
    background: var(--color-primary);
  }
}
</style>
