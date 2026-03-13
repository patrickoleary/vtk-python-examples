import DefaultTheme from 'vitepress/theme'
import ExampleGallery from '../components/ExampleGallery.vue'
import RandomHero from '../components/RandomHero.vue'
import SpiralGallery from '../components/SpiralGallery.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('ExampleGallery', ExampleGallery)
    app.component('RandomHero', RandomHero)
    app.component('SpiralGallery', SpiralGallery)
  },
}
