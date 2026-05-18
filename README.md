# WearImpact

WearImpact is a sustainable-fashion web application that helps users reduce textile waste by making eco-friendly choices easier to discover, understand, and act on. It combines a map-based eco-shop navigator, a privacy-first digital wardrobe with automatic clothing recognition, a care-label reader, an AI sustainability advisor, an outfit try-on preview, and a brand sustainability search into a single web experience.

---

## Project Goals

- Help users find nearby second-hand, donation, and recycling destinations.
- Provide AI-driven guidance on extending garment life and making greener purchasing decisions.
- Let users build a personal digital wardrobe from photos, with automatic clothing recognition.
- Translate fabric compositions and care instructions into clear longevity and disposal guidance.
- Surface sustainability information for fashion brands at the moment of decision.
- Lower the knowledge barrier to circular-fashion practices through accessible content.

---

## Feature Overview

### Local Eco-Shop Navigator
An interactive map that surfaces second-hand shops, donation points, and recycling centres around the user's current or chosen location. Results are clustered by type, sorted by straight-line distance, and rendered as map markers users can tap or click to inspect.

Each result expands into a detail panel showing address, opening hours, phone, and website, so users can decide between *go now*, *call ahead*, or *plan a route* without leaving the page. A user-defined search radius lets people scope the catchment to a walking trip or a broader weekend errand. Place details are cached for repeat lookups to keep the experience instant on revisit.

### Digital Wardrobe
Users upload garment photos; a clothing-recognition pipeline removes the background, segments the person from the clothing, and classifies each item into a main category (upper body / lower body / footwear) and a fine-grained subcategory (e.g. t-shirt, denim trousers, sneaker). Recognised items land in a visual catalogue grouped by category.

The entire wardrobe lives on the user's device. There is no account, no upload to a personal profile, and no server-side storage of clothing imagery — clearing browser storage clears the wardrobe. This makes the feature usable without commitments and removes a common reason people hesitate to digitise personal belongings.

### Wash Label Recognition
A label reader that turns the small print on a garment's care tag into actionable understanding. The user photographs the tag; the recognition pipeline extracts the fibre composition (e.g. *60% cotton, 40% polyester*) and the care icons (wash temperature, drying, ironing, dry-clean status), then translates them into plain language with longevity, care-routine, and end-of-life implications.

Non-English labels are recognised and translated automatically, so a garment bought abroad still produces useful guidance. The reader is integrated with the wardrobe: once a label is read, its data attaches to the corresponding wardrobe entry and feeds the advisor.

### AI Sustainability Advisor
A wardrobe-aware advisor that turns the actual contents of the user's wardrobe into personalised, evidence-based guidance. Instead of generic tips, suggestions are grounded in the user's real fibre mix, category distribution, and recently added items.

The advisor covers four recurring user intents: reducing footprint, rethinking new purchases, extending garment life, and disposing more responsibly. Output is structured into a clear headline, a short summary, a handful of fact cards, and concrete recommendations the user can accept and act on. Follow-up questions surface naturally, so the experience reads like an informed conversation rather than a static report.

### Outfit & Try-On Preview
A preview tool that lets users assemble outfit combinations from items already in their wardrobe and visualise them on a stylised mannequin. The goal is to encourage re-wear: by making it easy to *see* how existing items combine into fresh looks, the feature reduces the perceived need for new purchases.

Try-on previews are generated locally where possible and never require uploading the user's wardrobe to a remote profile.

### Brand Sustainability Search
A searchable index of fashion brands and the sustainability-relevant information attached to them — certifications, materials policies, manufacturing transparency, and recommended alternatives. The search is designed to be quick enough to use at the moment of purchase decision: type a brand name, see at a glance how it compares, and surface gentler alternatives if it falls short.

### Knowledge Hub & Home
An editorial surface that introduces the impact of fast fashion, the principles of a circular wardrobe, and the application's tools through approachable, scrollable storytelling. The Home view doubles as the project's narrative entry point — explaining *why* before the user reaches the *how* — and the Knowledge Hub anchors the deeper concepts users may want to revisit.

---

## Architecture

WearImpact is composed of three independent, decoupled layers that communicate over standard HTTP. The split keeps each layer's footprint and failure modes contained, and lets the privacy-sensitive parts of the experience stay on the user's device.

```
┌──────────────── Browser-based Client ────────────────┐
│  Home · Knowledge · Eco-Shop Map · Wardrobe          │
│  Wash-Label Reader · Advisor · Try-On · Brand Search │
└────┬──────────────────────┬─────────────────────┬────┘
     │ REST                 │ REST (multipart)    │ REST
     ▼                      ▼                     ▼
 API Service          Recognition Service      API Service
 (location search,    (clothing classification, (advisor,
  place details)       background removal,       brand search)
                       care-label OCR)
```

- **Client** — a single-page application running entirely in the browser. Holds the user's wardrobe in on-device storage, handles map interactions, composes outfits, and orchestrates calls to the recognition service and the API service.
- **API service** — provides location search, place details, brand search, and the wardrobe sustainability advisor. Stateless and horizontally scalable; relies on a cache layer to keep upstream traffic and response latency low.
- **Recognition service** — performs garment classification, background removal, and care-label optical character recognition. Lives as a separate workload because the model footprint is large; isolating it prevents the rest of the system from inheriting that weight.

---

## Repository Layout

```
.
├── frontend/        Browser-based single-page application
├── backend/         API service for locations, brands, and advisor
└── README.md
```

The recognition service is maintained and deployed as an independent workload, kept outside the main repository's build path so the API service and the client remain lightweight.

---

## API Surface (high level)

These are the public endpoints the client consumes. They are described in user terms; full request and response shapes live in the source.

- **Find eco-shops nearby** — returns second-hand, donation, and recycling destinations near a coordinate, sorted by distance.
- **Get place details** — returns address, opening hours, phone, and website for a single destination.
- **Search brands** — returns brand sustainability records matching a query.
- **Generate wardrobe advice** — produces personalised sustainability guidance grounded in the user's wardrobe.
- **Classify uploaded garments** — recognises one or more garment images and returns category, subcategory, and a transparent preview per item.
- **Read a care label** — extracts fibre composition and care instructions from a photographed garment tag, with automatic translation when needed.

---

## Privacy

- The digital wardrobe never leaves the user's browser. Uploaded photos are processed transiently for recognition; the resulting previews and metadata are persisted only on the user's device, not on any server.
- No login, account, or personal identifier is required to use any feature.
- Clearing browser storage clears the wardrobe completely — the user controls retention end-to-end.
- The recognition service receives images only for the duration of processing and does not retain them after the response is returned.
