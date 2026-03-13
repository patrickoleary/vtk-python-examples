<script setup>
import { ref, onMounted } from 'vue'
import { withBase } from 'vitepress'
import gallery from '../generated/gallery.mjs'

const example = ref(null)

function pickRandom() {
  const idx = Math.floor(Math.random() * gallery.length)
  example.value = gallery[idx]
}

onMounted(() => {
  pickRandom()
  setInterval(pickRandom, 5000)
})
</script>

<template>
  <div v-if="example" class="random-hero">
    <a :href="withBase(example.link)">
      <img
        :src="withBase(example.image)"
        :alt="example.title"
        class="random-hero-img"
      />
      <p class="random-hero-caption">{{ example.title }}</p>
    </a>
  </div>
</template>
