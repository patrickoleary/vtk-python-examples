import { defineConfig } from 'vitepress'
import sidebar from './generated/sidebar.mjs'

export default defineConfig({
  title: 'VTK Python Examples',
  description: 'A collection of VTK Python examples with screenshots and source code',
  base: '/vtk-python-examples/',
  ignoreDeadLinks: true,
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Gallery', link: '/gallery' },
      { text: 'Examples', link: '/examples/' },
      { text: 'Navigation', link: '/navigation' },
    ],
    sidebar: {
      '/examples/': sidebar,
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/Kitware/vtk-python-examples' },
    ],
  },
})
