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

const categories = computed(() => {
  const cats = [...new Set(props.examples.map((e) => e.category))]
  return cats.sort()
})

const filtered = computed(() => {
  const q = search.value.toLowerCase()
  return props.examples.filter((e) => {
    const matchesSearch =
      !q ||
      e.title.toLowerCase().includes(q) ||
      e.category.toLowerCase().includes(q)
    const matchesCategory =
      !selectedCategory.value || e.category === selectedCategory.value
    return matchesSearch && matchesCategory
  })
})
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
    </div>
    <p class="gallery-count">
      Showing {{ filtered.length }} of {{ examples.length }} examples
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
