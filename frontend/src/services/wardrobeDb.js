/**
 * Epic 3 — Digital Wardrobe local persistence (Dexie / IndexedDB).
 *
 * All wardrobe data is stored only in the browser. Clearing site data clears
 * the wardrobe. No backend persistence, no login. See CLAUDE.md §E3.
 */
import Dexie from 'dexie'

const db = new Dexie('WearImpactWardrobe')

db.version(1).stores({
  // Indexed fields: main_category for category grouping queries,
  // uploaded_at for recency stats.
  garments: '++id, main_category, uploaded_at'
})

// v2 — Epic 3.6: wash-label OCR materials + try-on cache. New fields
// (materials, raw_label_text, label_image_base64, label_uploaded_at) are
// not indexed so the schema stores stay the same; Dexie auto-migrates and
// records that don't have them just read back as `undefined`.
db.version(2).stores({
  garments: '++id, main_category, uploaded_at',
  tryon_cache: '++id, &garment_key, generated_at'
})

export const MAIN_CATEGORIES = ['upper_body', 'lower_body', 'footwear']

export async function addGarment(record) {
  return db.garments.add(record)
}

export async function getAllGarments() {
  return db.garments.orderBy('uploaded_at').reverse().toArray()
}

export async function getGarmentsByCategory(mainCategory) {
  return db.garments
    .where('main_category')
    .equals(mainCategory)
    .reverse()
    .sortBy('uploaded_at')
}

export async function countTotal() {
  return db.garments.count()
}

export async function countRecent(days = 7) {
  const since = Date.now() - days * 24 * 60 * 60 * 1000
  return db.garments.where('uploaded_at').above(since).count()
}

export async function deleteGarment(id) {
  return db.garments.delete(id)
}

export async function clearWardrobe() {
  await db.tryon_cache.clear()
  return db.garments.clear()
}

export async function updateGarmentImage(id, image_base64) {
  return db.garments.update(id, { image_base64 })
}

/**
 * Replace the OCR-derived material composition + raw label record for one
 * garment. Pass `{ materials, raw_label_text, label_image_base64,
 * label_uploaded_at }` — fields not provided are left untouched.
 */
export async function updateGarmentMaterials(id, payload) {
  return db.garments.update(id, payload)
}

export async function putTryOnCache(entry) {
  // Upsert keyed by `garment_key` (garment id + mannequin signature) so a
  // repeat try-on overwrites the previous result instead of stacking.
  return db.tryon_cache.put(entry)
}

export async function getTryOnCache(garmentKey) {
  return db.tryon_cache.where('garment_key').equals(garmentKey).first()
}

export default db
