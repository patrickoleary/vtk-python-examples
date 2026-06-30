<script setup>
import { ref, computed, onMounted } from 'vue'
import { withBase } from 'vitepress'
import MarkdownIt from 'markdown-it'
import { createHighlighter } from 'shiki'
import vtkDslGrammar from '../grammars/vtkdsl.tmLanguage.json'

const props = defineProps({
  example: {
    type: Object,
    required: true,
  },
})

const md = new MarkdownIt()
const navVisible = ref(true)
const highlighter = ref(null)

onMounted(async () => {
  highlighter.value = await createHighlighter({
    themes: ['github-dark', 'github-light'],
    langs: [
      'python',
      { ...vtkDslGrammar, name: 'vtkdsl' },
    ],
  })
})

const highlightCode = (code, lang) => {
  if (!highlighter.value) return `<pre><code>${code}</code></pre>`
  const isDark = document.documentElement.classList.contains('dark')
  const theme = isDark ? 'github-dark' : 'github-light'
  try {
    return highlighter.value.codeToHtml(code, { lang, theme })
  } catch (e) {
    return `<pre><code>${code}</code></pre>`
  }
}

const copyCode = async (code) => {
  try {
    await navigator.clipboard.writeText(code)
  } catch (e) {
    console.error('Failed to copy:', e)
  }
}

const sortedEventActions = computed(() => {
  if (!props.example.eventActions || !Array.isArray(props.example.eventActions)) return []
  return [...props.example.eventActions].sort((a, b) => a.index - b.index)
})

const renderedDescription = computed(() => {
  if (!props.example.description) return ''
  return md.render(props.example.description)
})

const sections = computed(() => {
  const secs = []
  if (props.example.description) secs.push({ id: 'description', label: 'Description' })
  if (props.example.vtkClasses && props.example.vtkClasses.length) secs.push({ id: 'vtk-classes', label: 'VTK Classes' })
  if (props.example.dataFiles && props.example.dataFiles.length) secs.push({ id: 'data-files', label: 'Data Files' })
  if (props.example.dsl) secs.push({ id: 'dsl', label: 'DSL' })
  if (props.example.sourceCode) secs.push({ id: 'source-code', label: 'Source Code' })
  if (sortedEventActions.value.length) secs.push({ id: 'event-actions', label: 'Event Actions' })
  return secs
})

const toggleNav = () => {
  navVisible.value = !navVisible.value
}
</script>

<template>
  <div class="example-detail">
    <div class="example-header">
      <h1>{{ example.title }}</h1>
      <div class="example-meta">
        <span class="tag">Tag: {{ example.tag }}</span>
        <span class="topology">Topology: <strong>{{ example.topology }}</strong></span>
        <span class="events">{{ example.n_events }} events</span>
        <span class="phrases">{{ example.n_phrases }} phrases</span>
      </div>
    </div>

    <button
      class="nav-toggle"
      :class="{ 'nav-toggle-on': navVisible }"
      @click="toggleNav"
      role="switch"
      type="button"
      :aria-checked="navVisible"
      :title="navVisible ? 'Hide navigation' : 'Show navigation'"
      aria-label="Toggle navigation"
    >
      <span class="nav-toggle-check">
        <span class="nav-toggle-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
          </svg>
        </span>
      </span>
    </button>

    <div v-if="navVisible" class="example-nav">
      <h3>On this page</h3>
      <ul>
        <li v-for="section in sections" :key="section.id">
          <a :href="`#${section.id}`">{{ section.label }}</a>
        </li>
      </ul>
      <ul class="event-nav">
        <li v-for="action in sortedEventActions" :key="action.index">
          <a :href="`#event-${action.index}`">#{{ action.index }} · {{ action.type }}</a>
        </li>
      </ul>
    </div>

    <div v-if="example.image" class="example-image">
      <img :src="withBase(example.image)" :alt="example.title" />
    </div>

    <div v-if="example.description" id="description" class="example-description">
      <h2>Description</h2>
      <div v-html="renderedDescription"></div>
    </div>

    <div v-if="example.vtkClasses && example.vtkClasses.length" id="vtk-classes" class="example-classes">
      <h2>VTK Classes</h2>
      <p>{{ example.pipeline }}</p>
      <ul>
        <li v-for="cls in example.vtkClasses" :key="cls.name">
          <a :href="cls.link" target="_blank">{{ cls.name }}</a> — {{ cls.description }}
        </li>
      </ul>
    </div>

    <div v-if="example.dataFiles && example.dataFiles.length" id="data-files" class="example-data">
      <h2>Data Files</h2>
      <ul>
        <li v-for="file in example.dataFiles" :key="file.name">
          <a :href="withBase(file.path)" target="_blank">{{ file.name }}</a>
        </li>
      </ul>
    </div>

    <div v-if="example.sourcePath" class="example-source-link">
      <strong>Source:</strong> <a :href="withBase(example.sourcePath)" target="_blank">{{ example.sourceFile }}</a>
    </div>

    <div v-if="example.dsl" id="dsl" class="example-dsl">
      <h2>DSL</h2>
      <div class="code-block-wrapper">
        <button class="copy-button" @click="copyCode(example.dsl)" title="Copy code">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
          </svg>
        </button>
        <div class="code-block" v-html="highlightCode(example.dsl, 'vtkdsl')"></div>
      </div>
    </div>

    <div v-if="example.sourceCode" id="source-code" class="example-source">
      <h2>Source Code</h2>
      <div class="code-block-wrapper">
        <button class="copy-button" @click="copyCode(example.sourceCode)" title="Copy code">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
          </svg>
        </button>
        <div class="code-block" v-html="highlightCode(example.sourceCode, 'python')"></div>
      </div>
    </div>

    <div v-if="sortedEventActions.length" id="event-actions" class="example-events">
      <h2>Event Actions ({{ sortedEventActions.length }})</h2>
      <div v-for="action in sortedEventActions" :key="action.index" :id="`event-${action.index}`" class="event-action">
        <h3>#{{ action.index }} · {{ action.phase }} · <strong>{{ action.type }}</strong> "{{ action.label }}"</h3>
        <div class="code-block-wrapper">
          <button class="copy-button" @click="copyCode(action.dsl)" title="Copy code">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
          </button>
          <div class="code-block" v-html="highlightCode(action.dsl, 'vtkdsl')"></div>
        </div>
        <div class="event-meta">
          <p><strong>line:</strong> {{ action.line }}</p>
          <p><strong>vtk class:</strong> {{ action.vtkClass }}</p>
          <p><strong>verb:</strong> {{ action.verb }}</p>
          <p><strong>noun:</strong> {{ action.noun }}</p>
          <p v-if="action.label"><strong>label:</strong> {{ action.label }}</p>
        </div>
        <div v-if="action.properties && Object.keys(action.properties).length" class="event-properties">
          <h4>Properties:</h4>
          <div v-for="(value, key) in action.properties" :key="key" class="property">
            <strong>{{ key }} →</strong> {{ value }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.example-detail {
  max-width: 100%;
  padding: 2rem 2rem 4rem;
  margin: 0 auto;
  position: relative;
}

.nav-toggle {
  position: fixed;
  top: 21px;
  right: 6.5rem;
  z-index: 99999;
  width: 40px;
  height: 22px;
  padding: 0;
  border: 1px solid var(--vp-c-border);
  border-radius: 11px;
  background-color: var(--vp-c-bg-soft);
  cursor: pointer;
  transition: border-color 0.25s, background-color 0.25s;
  display: block;
  pointer-events: auto !important;
}

.nav-toggle:hover {
  border-color: var(--vp-c-brand-1);
}

.nav-toggle.nav-toggle-on {
  background-color: var(--vp-c-brand-soft);
}

.nav-toggle-check {
  position: absolute;
  top: 1px;
  left: 1px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background-color: var(--vp-c-bg);
  box-shadow: var(--vp-shadow-1);
  transition: transform 0.25s;
}

.nav-toggle.nav-toggle-on .nav-toggle-check {
  transform: translateX(18px);
}

.nav-toggle-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  color: var(--vp-c-text-2);
}

.nav-toggle.nav-toggle-on .nav-toggle-icon {
  color: var(--vp-c-brand-1);
}

.nav-toggle-icon svg {
  width: 12px;
  height: 12px;
}

.example-nav {
  position: fixed;
  top: 3rem;
  right: 1rem;
  width: 250px;
  max-height: calc(100vh - 4rem);
  overflow-y: auto;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  padding: 0.75rem;
  z-index: 99;
}

.example-nav h3 {
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.example-nav h4 {
  font-size: 0.8rem;
  margin: 0.75rem 0 0.25rem 0;
  font-weight: 600;
}

.example-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.example-nav li {
  padding: 0.1rem 0;
}

.example-nav a {
  text-decoration: none;
  color: var(--vp-c-text-2);
  font-size: 0.8rem;
}

.example-nav a:hover {
  color: var(--vp-c-text-1);
}

.example-nav .event-nav {
  margin-top: 0.1rem;
}

.example-nav .event-nav li {
  padding: 0;
  line-height: 1.2;
}

.example-header h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.example-meta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  font-size: 0.9rem;
  color: var(--vp-c-text-2);
  margin-bottom: 1.5rem;
}

.example-meta .topology strong {
  color: var(--vp-c-text-1);
}

.example-image {
  margin-bottom: 2rem;
}

.example-image img {
  max-width: 100%;
  border-radius: 8px;
}

.example-description,
.example-classes,
.example-data,
.example-dsl,
.example-source,
.example-events {
  margin-bottom: 2rem;
}

.example-description h2,
.example-classes h2,
.example-data h2,
.example-dsl h2,
.example-source h2,
.example-events h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  padding-top: 2rem;
}

.example-description :deep(p) {
  margin: 0.5rem 0;
  line-height: 1.6;
}

.example-description :deep(ul),
.example-description :deep(ol) {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
  list-style: disc;
}

.example-description :deep(ol) {
  list-style: decimal;
}

.example-description :deep(li) {
  margin: 0.25rem 0;
}

.example-description :deep(code) {
  background: var(--vp-c-bg-soft);
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: var(--vp-font-family-mono);
  font-size: 0.9em;
}

.example-description :deep(a) {
  text-decoration: none;
  color: var(--vp-c-brand-1);
}

.example-description :deep(a:hover) {
  text-decoration: underline;
}

.example-classes ul,
.example-data ul {
  list-style: none;
  padding: 0;
}

.example-classes li,
.example-data li {
  padding: 0.25rem 0;
}

.example-classes a,
.example-data a,
.example-source-link a {
  text-decoration: none;
  color: var(--vp-c-brand-1);
}

.example-classes a:hover,
.example-data a:hover,
.example-source-link a:hover {
  text-decoration: underline;
}

.example-source-link {
  margin-bottom: 2rem;
}

.example-dsl pre,
.example-source pre {
  background: var(--vp-c-bg-soft);
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.example-dsl code,
.example-source code {
  font-family: var(--vp-font-family-mono);
  font-size: 0.9rem;
}

.code-block-wrapper {
  position: relative;
}

.copy-button {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-border);
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
  color: var(--vp-c-text-2);
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.copy-button:hover {
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  border-color: var(--vp-c-brand-1);
}

.code-block :deep(pre) {
  background: var(--vp-c-bg-soft);
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: var(--vp-font-family-mono);
  font-size: 0.9rem;
}

.event-action {
  margin-bottom: 2rem;
  padding: 1rem;
  background: var(--vp-c-bg-soft);
  border-radius: 6px;
}

.event-action h3 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.event-action pre {
  background: var(--vp-c-bg);
  padding: 0.75rem;
  border-radius: 4px;
  overflow-x: auto;
  margin-bottom: 0.75rem;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.event-action code {
  font-family: var(--vp-font-family-mono);
  font-size: 0.85rem;
}

.event-meta {
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
  margin-bottom: 0.25rem;
}

.event-meta p {
  margin: 0;
  line-height: 1.2;
}

.event-properties {
  margin-top: 0.25rem;
}

.event-properties h4 {
  font-size: 0.9rem;
  margin-bottom: 0.1rem;
}

.property {
  font-size: 0.85rem;
  padding: 0;
  line-height: 1.2;
}
</style>
