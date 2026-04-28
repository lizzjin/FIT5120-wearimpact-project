/**
 * Epic 4 brand service — Brand Transparency & Sustainability Inquiry.
 *
 * Handles all backend API calls:
 *   - searchBrands()      → GET /api/brands/search?q=...  (Step 1)
 *   - fetchCompanyDetail() → GET /api/brands/{company_id}  (Step 2)
 */

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

/**
 * Fetch a paginated list of all companies ordered by ethical score.
 *
 * @param {number} page - 1-based page number
 * @param {number} pageSize - Results per page
 * @returns {Promise<{results: Array, total: number, page: number, page_size: number}>}
 * @throws {Error} On network failure or non-2xx response
 */
/**
 * Fetch the entire company list by paging through the API.
 *
 * The public list endpoint caps page_size at 50, so to obtain the full
 * dataset (~247 companies) we make the first call, read the total, then
 * fan out the remaining pages in parallel.
 *
 * @returns {Promise<Array>} Flat list of all company rows.
 */
export async function fetchAllCompaniesAll() {
  const PAGE_SIZE = 50
  const first = await fetchAllCompanies(1, PAGE_SIZE)
  const total = first.total ?? first.results.length
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE))
  if (totalPages <= 1) return first.results

  const rest = await Promise.all(
    Array.from({ length: totalPages - 1 }, (_, i) => fetchAllCompanies(i + 2, PAGE_SIZE)),
  )
  return [...first.results, ...rest.flatMap((r) => r.results ?? [])]
}

export async function fetchAllCompanies(page = 1, pageSize = 9) {
  const params = new URLSearchParams({ page, page_size: pageSize })
  const response = await fetch(`${API_BASE}/api/brands?${params}`)

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}))
    throw new Error(errorBody?.detail || `Fetch failed (HTTP ${response.status})`)
  }

  return response.json()
}

/**
 * Search brands and companies by name with fuzzy matching.
 *
 * @param {string} query - Search string (min 1 char)
 * @returns {Promise<{results: Array, message: string|null}>}
 * @throws {Error} On network failure or non-2xx response
 */
export async function searchBrands(query) {
  const params = new URLSearchParams({ q: query })
  const response = await fetch(`${API_BASE}/api/brands/search?${params}`)

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}))
    throw new Error(errorBody?.detail || `Search failed (HTTP ${response.status})`)
  }

  return response.json()
}

/**
 * Fetch full sustainability detail for a company.
 *
 * @param {number} companyId - Company primary key
 * @returns {Promise<object>} Full CompanyDetailResponse
 * @throws {Error} On network failure, 404, or 503
 */
export async function fetchCompanyDetail(companyId) {
  const response = await fetch(`${API_BASE}/api/brands/${companyId}`)

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}))
    throw new Error(errorBody?.detail || `Detail fetch failed (HTTP ${response.status})`)
  }

  return response.json()
}
