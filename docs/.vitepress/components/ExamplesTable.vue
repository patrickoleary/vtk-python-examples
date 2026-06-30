<script setup>
import { computed } from 'vue'
import { withBase } from 'vitepress'

const props = defineProps({
  category: {
    type: String,
    required: true,
  },
  examples: {
    type: Array,
    required: true,
  },
})

const sortedExamples = computed(() => {
  if (!props.examples || !Array.isArray(props.examples)) return []
  return [...props.examples].sort((a, b) => a.title.localeCompare(b.title))
})
</script>

<template>
  <div class="examples-category-section">
    <h2 :id="category">{{ category }} ({{ examples?.length || 0 }})</h2>
    <table class="examples-list-table">
      <thead>
        <tr>
          <th class="thumb-cell"></th>
          <th>Title</th>
          <th>Events</th>
          <th>Phrases</th>
          <th>Topology</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ex in sortedExamples" :key="ex.title">
          <td class="thumb-cell">
            <img
              v-if="ex.imageSmall"
              :src="withBase(ex.imageSmall)"
              :alt="ex.title"
              width="44"
              height="44"
            />
          </td>
          <td>
            <a :href="withBase(ex.link)">{{ ex.title }}</a>
          </td>
          <td>{{ ex.n_events }}</td>
          <td>{{ ex.n_phrases }}</td>
          <td>{{ ex.topology }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.examples-category-section {
  margin-bottom: 3rem;
}

.examples-category-section h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  padding-top: 2rem;
}

.examples-list-table {
  width: 100%;
  max-width: 1200px;
  border-collapse: collapse;
  table-layout: fixed;
}

.examples-list-table th,
.examples-list-table td {
  padding: 0.5rem 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--vp-c-divider);
}

.examples-list-table th {
  font-weight: 600;
  background: var(--vp-c-bg-soft);
}

.examples-list-table .thumb-cell {
  width: 44px;
  padding: 0;
  vertical-align: middle;
}

.examples-list-table .thumb-cell img {
  display: block;
  border-radius: 4px;
}

.examples-list-table td:nth-child(2),
.examples-list-table th:nth-child(2) {
  width: auto;
  padding-left: 0.25rem;
}

.examples-list-table td:nth-child(3),
.examples-list-table th:nth-child(3),
.examples-list-table td:nth-child(4),
.examples-list-table th:nth-child(4) {
  width: 72px;
  text-align: center;
  white-space: nowrap;
}

.examples-list-table td:nth-child(5),
.examples-list-table th:nth-child(5) {
  width: 80px;
  text-align: center;
}

.examples-list-table td a {
  text-decoration: none;
  color: var(--vp-c-brand-1);
}

.examples-list-table td a:hover {
  text-decoration: underline;
}
</style>
