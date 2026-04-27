<template>
  <section class="hero">
    <div class="hero-text">
      <p class="eyebrow">FOR SUSTAINABLE FASHION IN AUSTRALIA</p>
      <h1>Your guide to shopping fashion sustainably</h1>
      <p class="subtitle">
        WearImpact shows you where to find second-hand shops near you,
        how transparent your favourite brands really are, and why
        sustainable fashion choices matter.
      </p>

      <div class="hero-buttons">
        <router-link to="/eco-shop" class="primary-btn">Find Eco-Shops Near Me</router-link>
        <router-link to="/brand-search" class="secondary-btn">Check a Brand's Score</router-link>
      </div>

      <p class="trust-line">Free to use · No account needed · Based on Australian locations</p>
    </div>

    <div class="hero-image">
      <img
        src="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=900&q=80"
        alt="Person browsing clothes in a second-hand op-shop"
      />
    </div>
  </section>
</template>

<style scoped>
.hero {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 48px;
  align-items: center;
  background: var(--color-primary-light);
  border-radius: var(--radius-card-lg);
  padding: 64px 56px;
  margin-bottom: 20px;
}

.eyebrow {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-primary-text);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 16px;
}

.hero-text h1 {
  font-size: 96px;
  line-height: 0.85;
  letter-spacing: -0.02em;
  font-weight: 900;
  color: var(--color-text);
  margin-bottom: 28px;
  max-width: 520px;
}

.subtitle {
  font-size: 20px;
  font-weight: 500;
  line-height: 1.5;
  color: var(--color-text-muted);
  max-width: 560px;
  margin-bottom: 32px;
}

.hero-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 18px;
}

.primary-btn,
.secondary-btn {
  padding: 12px 22px;
  border-radius: var(--radius-pill);
  font-weight: 700;
  display: inline-block;
  text-decoration: none;
  font-size: 16px;
  transition: transform var(--transition-base);
}

.primary-btn {
  background: var(--color-primary);
  color: var(--color-primary-text);
}

.primary-btn:hover {
  transform: scale(1.05);
}

.primary-btn:active {
  transform: scale(0.95);
}

.secondary-btn {
  background: rgba(22, 51, 0, 0.08);
  color: var(--color-text);
}

.secondary-btn:hover {
  transform: scale(1.05);
}

.secondary-btn:active {
  transform: scale(0.95);
}

.trust-line {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-subtle);
  margin: 0;
}

.hero-image img {
  width: 100%;
  height: 420px;
  object-fit: cover;
  object-position: 50% 40%;
  border-radius: var(--radius-card);
  display: block;
}

@media (max-width: 900px) {
  .hero {
    grid-template-columns: 1fr;
    padding: 40px 24px;
  }

  .hero-text h1 {
    font-size: 56px;
    line-height: 0.85;
  }

  .subtitle {
    font-size: 18px;
  }

  .hero-image img {
    height: 280px;
  }
}
</style>
