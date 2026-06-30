<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { withBase } from 'vitepress'

const props = defineProps({
  examples: {
    type: Array,
    required: true,
  },
})

const hoveredIndex = ref(null)
const containerWidth = ref(1000)
const containerRef = ref(null)

// Shuffle examples once for visual variety (seeded by length for consistency)
const shuffled = computed(() => {
  const arr = [...props.examples].filter(e => e.image)
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[arr[i], arr[j]] = [arr[j], arr[i]]
  }
  return arr
})

const THUMB = 44
const GAP = 6

// Trapezoid → rectangle: centered rows that widen from the top until they
// reach the full container width, then stay full (so nothing overflows).
const positions = computed(() => {
  const items = shuffled.value
  const result = []
  const step = THUMB + GAP
  const maxCols = Math.max(1, Math.floor(containerWidth.value / step))
  const startCols = Math.max(1, Math.ceil(maxCols / 3))

  let placed = 0
  let row = 0
  while (placed < items.length) {
    let cols = Math.min(startCols + row * 2, maxCols)
    cols = Math.min(cols, items.length - placed)
    const rowWidth = cols * step - GAP
    const startX = (containerWidth.value - rowWidth) / 2 + THUMB / 2
    const y = row * step + THUMB / 2 + 4
    for (let i = 0; i < cols; i++) {
      result.push({ x: startX + i * step, y })
      placed++
    }
    row++
  }
  return result
})

// Container height = max Y position + thumb size + padding
const containerHeight = computed(() => {
  if (positions.value.length === 0) return 200
  let maxY = 0
  for (const p of positions.value) {
    if (p.y > maxY) maxY = p.y
  }
  return Math.ceil(maxY + THUMB + 8)
})

function handleMouseEnter(idx) {
  hoveredIndex.value = idx
}

function handleMouseLeave() {
  hoveredIndex.value = null
}

function updateWidth() {
  if (containerRef.value) {
    containerWidth.value = containerRef.value.clientWidth
  }
}

onMounted(() => {
  updateWidth()
  window.addEventListener('resize', updateWidth)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateWidth)
})
</script>

<template>
  <div
    ref="containerRef"
    class="trapezoid-wrapper"
  >
    <div
      class="trapezoid-container"
      :style="{
        width: containerWidth + 'px',
        height: containerHeight + 'px',
      }"
    >
      <a
        v-for="(ex, idx) in shuffled"
        :key="ex.title"
        :href="withBase(ex.link)"
        class="trapezoid-thumb"
        :class="{ 'is-hovered': hoveredIndex === idx }"
        :style="{
          left: positions[idx]?.x + 'px',
          top: positions[idx]?.y + 'px',
          zIndex: hoveredIndex === idx ? 50 : 1,
        }"
        @mouseenter="handleMouseEnter(idx)"
        @mouseleave="handleMouseLeave"
        :title="ex.title + ' — ' + ex.category"
      >
        <img
          :src="withBase(ex.imageSmall || ex.image)"
          :alt="ex.title"
          loading="lazy"
        />
        <span v-if="hoveredIndex === idx" class="trapezoid-tooltip">
          {{ ex.title }}
        </span>
      </a>
    </div>
    <p class="trapezoid-count">
      Showing all {{ shuffled.length.toLocaleString() }} examples
    </p>
  </div>
</template>
