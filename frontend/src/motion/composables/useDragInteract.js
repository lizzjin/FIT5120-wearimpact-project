/**
 * Drag-with-inertia primitive. Wraps GSAP Draggable + InertiaPlugin so
 * the element can be dragged with mouse/touch and glides to a stop on
 * release. Useful for touch swipe (BrandCarousel), wardrobe garment
 * drag, sortable lists.
 *
 *   const dragRef = ref(null)
 *   useDragInteract(dragRef, {
 *     type: 'x',
 *     bounds: '.carousel',
 *     onDragEnd: () => snapToNearest(),
 *   })
 */
import { onMounted, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'
import { Draggable, ensurePlugins } from '../registry'
import { isReduced } from '../matchMedia'

export function useDragInteract(elRef, options = {}) {
  const {
    type = 'x,y',
    bounds = null,
    inertia = true,
    edgeResistance = 0.65,
    onDragStart = null,
    onDrag = null,
    onDragEnd = null,
    onThrowComplete = null,
  } = options

  ensurePlugins()

  let instance = null

  onMounted(() => {
    const el = elRef?.value
    if (!el || isReduced()) return

    const arr = Draggable.create(el, {
      type,
      bounds,
      inertia,
      edgeResistance,
      cursor: type.includes('x') && type.includes('y') ? 'grab' : null,
      activeCursor: 'grabbing',
      onDragStart,
      onDrag,
      onDragEnd,
      onThrowComplete,
    })
    instance = arr[0]
  })

  onBeforeUnmount(() => {
    instance?.kill()
    instance = null
  })

  return {
    getDraggable: () => instance,
  }
}
