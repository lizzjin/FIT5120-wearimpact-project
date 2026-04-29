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
  return db.garments.clear()
}

export async function updateGarmentImage(id, image_base64) {
  return db.garments.update(id, { image_base64 })
}

export default db
