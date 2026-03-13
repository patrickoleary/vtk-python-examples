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

const THUMB = 24
const GAP = 3

// Half-circle: place items in semicircular arcs (bottom half = flat edge at top)
const positions = computed(() => {
  const items = shuffled.value
  const result = []
  const cx = containerWidth.value / 2
  const cy = 0 // top edge is the flat side of the half-circle
  let placed = 0
  const step = THUMB + GAP

  // Ring 0: center item at the top-center
  if (placed < items.length) {
    result.push({ x: cx, y: cy + THUMB / 2 + 4, ring: 0 })
    placed++
  }

  // Subsequent semicircular rings (only bottom half: 0 to PI)
  let ring = 1
  while (placed < items.length) {
    const radius = ring * step
    // Items along a semicircle (PI radians)
    const arcLength = Math.PI * radius
    const count = Math.min(
      Math.floor(arcLength / (THUMB + GAP / 2)),
      items.length - placed
    )
    for (let i = 0; i < count && placed < items.length; i++) {
      // Distribute from 0 to PI (left to right semicircle below center)
      const angle = (Math.PI * (i + 0.5)) / count
      result.push({
        x: cx + radius * Math.cos(Math.PI - angle),
        y: cy + radius * Math.sin(angle),
        ring,
      })
      placed++
    }
    ring++
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
    class="spiral-wrapper"
  >
    <div
      class="spiral-container"
      :style="{
        width: containerWidth + 'px',
        height: containerHeight + 'px',
      }"
    >
      <a
        v-for="(ex, idx) in shuffled"
        :key="ex.title"
        :href="withBase(ex.link)"
        class="spiral-thumb"
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
          :src="withBase(ex.image)"
          :alt="ex.title"
          loading="lazy"
        />
        <span v-if="hoveredIndex === idx" class="spiral-tooltip">
          {{ ex.title }}
        </span>
      </a>
    </div>
  </div>
</template>
