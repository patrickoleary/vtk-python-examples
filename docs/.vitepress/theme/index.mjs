import DefaultTheme from 'vitepress/theme'
import ExampleGallery from '../components/ExampleGallery.vue'
import TrapezoidGallery from '../components/TrapezoidGallery.vue'
import ExamplesTable from '../components/ExamplesTable.vue'
import ExampleDetail from '../components/ExampleDetail.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('ExampleGallery', ExampleGallery)
    app.component('TrapezoidGallery', TrapezoidGallery)
    app.component('ExamplesTable', ExamplesTable)
    app.component('ExampleDetail', ExampleDetail)
  },
}
