# Illustration assets

All illustrations in this directory follow the WearImpact 3-tier system defined in
[DESIGN.md §10](../../../../DESIGN.md) and the
[`wise-aesthetic-redesign` change spec](../../../../openspec/changes/wise-aesthetic-redesign/specs/illustration-system/spec.md).

## Tiers

| Tier | Source | Width | Role |
|------|--------|-------|------|
| **L1 Hero** | unDraw (re-tinted) | 320–480px | Emotional anchor; max one per page |
| **L2 Section** | Storyset / unDraw cropped | 180–280px | Solution sections, empty states, fact cards |
| **L3 Mini** | Iconify (`solar` pack) or hand-drawn line-art | 48–80px | Card corners, inline icons, decorative marks |

## Default Iconify pack

The product defaults to the **Solar** Iconify pack (`solar:` prefix) for system icons. It
matches the brand's hand-drawn warmth without leaning on geometric/material defaults.

```vue
<Icon icon="solar:map-point-bold-duotone" />
```

Mixing icon packs on a single surface is forbidden — pick one and stick to it.

## Re-tint palette (mandatory)

Every imported illustration must be re-tinted to the Wise palette before commit:

| Role | Hex |
|------|-----|
| Primary fill | `#9fe870` (Wise Lime) |
| Stroke / outline | `#163300` (Dark Green), 1.5–2px |
| Accent | `#ffc091` (Warm Orange) |
| Neutral fill | `#e2f6d5` (Light Mint) |

**Banned source colors:** `#6c63ff` (unDraw cobalt), Storyset purple, any cyan / magenta /
cobalt. Re-tint or reject.

## Filename convention

`<page>-<role>-<slug>.svg`

Examples:

- `home-hero-bridge.svg` — L1 illustration on `HomeView §4 Bridge`
- `home-watermark-hanger.svg` — L3 watermark on `HomeView §1 Hero`
- `home-corner-mappin.svg` — L3 corner mark on `HomeView §5`
- `knowledge-hero-globe.svg` — L1 hero on `KnowledgeView`
- `knowledge-fact-water.svg` — L2 fact-card on a quiz question about water
- `brand-empty-shelves.svg` — L2 empty state on `BrandSearchView`
- `eco-empty-bag.svg` — L2 empty state on `EcoShopView`

## Stroke draw-on requirement

Illustrations enter via SVG `stroke-dasharray` draw-on, not opacity fade-in. Every visible
path must have a continuous stroke (or use a small `clip-path` reveal workaround for
solid-fill paths). The `useDrawOnSvg` composable at
[`frontend/src/composables/useDrawOnSvg.js`](../../composables/useDrawOnSvg.js) handles the
animation — pass an inline SVG element ref.

## Decorative-layer opacity cap

When an illustration sits behind content as decoration, its rest opacity must be ≤ 12%.
On hover (or another explicit reveal trigger) it may rise to ≈ 25%. Anything brighter
competes with foreground typography.

## Authoring checklist

Before committing a new SVG:

1. ✅ Filename matches `<page>-<role>-<slug>.svg`
2. ✅ Palette restricted to Wise tokens (no `#6c63ff`, no purple, no cyan)
3. ✅ Stroke widths between 1.5 and 2px
4. ✅ ViewBox is a clean square or rectangle (no leftover artboard padding)
5. ✅ File optimized via SVGO (`npx svgo -i illustrations/<file>.svg`)
6. ✅ If used as decoration: rest opacity ≤ 12%
7. ✅ If L1: not centered on the page — anchor left, right, or corner
