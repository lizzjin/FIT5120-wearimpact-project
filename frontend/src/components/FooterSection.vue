<template>
  <footer class="footer" ref="footerRef">
    <div class="footer-grid">
      <div class="footer-brand">
        <h2>
          <span class="logo-mark">Wear</span><span class="logo-tail">Impact</span>
        </h2>
        <p>
          Helping Australians make more informed, sustainable fashion choices — one purchase at a time.
        </p>
      </div>

      <div>
        <h4>Tools</h4>
        <ul>
          <li><router-link to="/wardrobe">My Wardrobe</router-link></li>
          <li><router-link to="/knowledge">Knowledge Hub</router-link></li>
          <li><router-link to="/brand-search">Brand Search</router-link></li>
          <li><router-link to="/eco-shop">Eco-Shop Navigator</router-link></li>
        </ul>
      </div>

    </div>

    <div class="footer-bottom">
      <p>&copy; 2026 WearImpact. All rights reserved.</p>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue'
import { useStagger } from '../motion/useStagger'

const footerRef = ref(null)
// Stagger the brand block + each tools column when the footer enters view.
useStagger(footerRef, { selector: '.footer-grid > *', stagger: 0.12, y: 28, delay: 0.05 })
</script>

<style scoped>
.footer {
  background: var(--color-dark-bg);
  color: white;
  padding: 64px 48px 28px;
  border-radius: 40px 40px 0 0;
  margin-top: 56px;
}

.footer-grid {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 48px;
  margin-bottom: 32px;
}

.footer h2 {
  font-size: 28px;
  font-weight: 900;
  letter-spacing: -0.01em;
  margin-bottom: 16px;
}

.logo-mark { color: var(--color-primary); }
.logo-tail { color: white; }

.footer h4 {
  color: white;
  margin-bottom: 16px;
  font-size: 15px;
  font-weight: 700;
}

.footer-brand p {
  color: rgba(246, 240, 230, 0.7);
  font-weight: 500;
  line-height: 1.5;
  max-width: 420px;
  font-size: 15px;
}

.footer ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer ul li {
  margin-bottom: 8px;
}

.footer a {
  color: rgba(246, 240, 230, 0.7);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color var(--transition-base);
}

.footer a:hover {
  color: var(--color-primary);
}

.footer-bottom {
  border-top: 1px solid rgba(246, 240, 230, 0.12);
  padding-top: 20px;
  text-align: center;
}

.footer-bottom p {
  font-size: 13px;
  font-weight: 500;
  color: rgba(246, 240, 230, 0.55);
  margin: 0;
}

@media (max-width: 768px) {
  .footer {
    padding: 40px 24px 20px;
  }
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 28px;
  }
}
</style>
