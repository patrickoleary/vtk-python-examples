<script setup>
import { ref, computed } from 'vue'
import { withBase } from 'vitepress'

const props = defineProps({
  examples: {
    type: Array,
    required: true,
  },
})

const search = ref('')
const selectedCategory = ref('')
const selectedSymbol = ref('')

const categories = computed(() => {
  const cats = [...new Set(props.examples.map((e) => e.category))]
  return cats.sort()
})

const allSymbols = computed(() => {
  const syms = new Set()
  for (const e of props.examples) {
    if (e.uses_symbols) {
      for (const s of e.uses_symbols) {
        syms.add(s)
      }
    }
  }
  return [...syms].sort()
})

const filteredSymbols = computed(() => {
  const q = symbolSearch.value.toLowerCase()
  if (!q) return allSymbols.value
  return allSymbols.value.filter((s) => s.toLowerCase().includes(q))
})

const symbolSearch = ref('')

const filtered = computed(() => {
  const q = search.value.toLowerCase()
  return props.examples.filter((e) => {
    const matchesSearch =
      !q ||
      e.title.toLowerCase().includes(q) ||
      e.category.toLowerCase().includes(q)
    const matchesCategory =
      !selectedCategory.value || e.category === selectedCategory.value
    const matchesSymbol =
      !selectedSymbol.value ||
      (e.uses_symbols && e.uses_symbols.includes(selectedSymbol.value))
    return matchesSearch && matchesCategory && matchesSymbol
  })
})

function clearSymbol() {
  selectedSymbol.value = ''
  symbolSearch.value = ''
}
</script>

<template>
  <div class="gallery-filter">
    <div class="gallery-filter-row">
      <input
        v-model="search"
        type="text"
        placeholder="Search examples..."
      />
      <select v-model="selectedCategory" class="gallery-select">
        <option value="">All categories</option>
        <option v-for="cat in categories" :key="cat" :value="cat">
          {{ cat }}
        </option>
      </select>
      <div class="vtk-class-filter">
        <input
          v-model="symbolSearch"
          type="text"
          placeholder="Filter VTK classes..."
          class="vtk-class-search"
        />
        <select v-model="selectedSymbol" class="gallery-select">
          <option value="">All VTK classes</option>
          <option v-for="sym in filteredSymbols" :key="sym" :value="sym">
            {{ sym }}
          </option>
        </select>
        <button v-if="selectedSymbol" class="vtk-class-clear" @click="clearSymbol">✕</button>
      </div>
    </div>
    <p class="gallery-count">
      Showing {{ filtered.length }} of {{ examples.length }} examples
      <span v-if="selectedSymbol"> using <strong>{{ selectedSymbol }}</strong></span>
    </p>
  </div>
  <div class="gallery-grid">
    <div v-for="ex in filtered" :key="ex.title" class="gallery-card">
      <a :href="withBase(ex.link)">
        <img
          v-if="ex.image"
          :src="withBase(ex.image)"
          :alt="ex.title"
          loading="lazy"
        />
        <div v-else class="gallery-placeholder">
          No screenshot
        </div>
        <div class="card-body">
          <p class="card-title">{{ ex.title }}</p>
          <p class="card-category">{{ ex.category }}</p>
        </div>
      </a>
    </div>
  </div>
</template>
