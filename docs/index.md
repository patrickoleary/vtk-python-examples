---
layout: page
title: VTK Python Examples
---

<script setup>
import gallery from './.vitepress/generated/gallery.mjs'
</script>

<div class="spiral-hero">
  <div class="spiral-hero-text">
    <h1 class="spiral-hero-title">VTK Python Examples</h1>
    <p class="spiral-hero-tagline">A curated collection of VTK examples in Python. Browse, learn, and reuse visualization patterns.</p>
    <div class="spiral-hero-actions">
      <a href="/vtk-python-examples/gallery" class="spiral-btn spiral-btn-brand">Browse Gallery</a>
      <a href="/vtk-python-examples/examples/" class="spiral-btn spiral-btn-alt">View Examples</a>
    </div>
  </div>
  <SpiralGallery :examples="gallery" />
</div>
