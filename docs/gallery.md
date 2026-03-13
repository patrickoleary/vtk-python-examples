---
title: Gallery
layout: page
---

<script setup>
import examples from './.vitepress/generated/gallery.mjs'
</script>

<div class="gallery-page">

# Example Gallery

Browse all VTK Python examples visually. Click any card to view the full source code and details.

<ExampleGallery :examples="examples" />

</div>
