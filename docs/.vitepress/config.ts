import { defineConfig } from 'vitepress'
import sidebarData from './sidebar.json'
import vtkDslGrammar from './grammars/vtkdsl.tmLanguage.json'

export default defineConfig({
  title: 'VTK Python Examples',
  description: 'A browsable gallery of VTK Python examples with DSL mappings',
  // Base path for deployment. For a GitHub project site this is "/<repo>/".
  // CI sets DOCS_BASE; defaults to "/" for local dev.
  base: process.env.DOCS_BASE
    ? '/' + process.env.DOCS_BASE.replace(/^\/+|\/+$/g, '') + '/'
    : '/',
  cleanUrls: true,
  // Generated example pages embed corpus explanation prose that may reference
  // other examples by name; those are not guaranteed to resolve to pages.
  ignoreDeadLinks: true,
  markdown: {
    languages: [
      {
        ...vtkDslGrammar,
        aliases: ['vtk', 'vtk-dsl']
      }
    ]
  },
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Gallery', link: '/gallery' },
      { text: 'Examples', link: '/examples/' },
    ],
    sidebar: { ...sidebarData },
    search: {
      provider: 'local',
    },
    outline: {
      level: [2, 3],
    },
  },
})
