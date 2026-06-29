import { defineConfig } from 'vitepress'
import sidebarData from './sidebar.json'
import dslGrammar from './dsl.tmLanguage.json'

const dslLang = {
  ...dslGrammar,
  name: 'vtk-dsl',
}

const dslThemeLight = {
  name: 'vtk-dsl-light',
  type: 'light',
  settings: [
    { scope: 'keyword.control.dsl', settings: { foreground: '#d32f2f' } },
    { scope: 'entity.name.type.dsl', settings: { foreground: '#7b1fa2' } },
    { scope: 'keyword.operator.with.dsl', settings: { foreground: '#e65100' } },
    { scope: 'entity.name.tag.dsl', settings: { foreground: '#2e7d32' } },
    { scope: 'keyword.other.called.dsl', settings: { foreground: '#616161' } },
    { scope: 'variable.other.label.dsl', settings: { foreground: '#212121' } },
    { scope: 'keyword.other.connector.dsl', settings: { foreground: '#757575' } },
    { scope: 'constant.numeric.dsl', settings: { foreground: '#1565c0' } },
    { scope: 'constant.other.array.dsl', settings: { foreground: '#1565c0' } },
    { scope: 'constant.other.string.dsl', settings: { foreground: '#1565c0' } },
    { scope: 'comment', settings: { foreground: '#6a737d' } },
    { scope: 'keyword', settings: { foreground: '#d73a49' } },
    { scope: 'string', settings: { foreground: '#032f62' } },
    { scope: 'constant.numeric', settings: { foreground: '#005cc5' } },
    { scope: 'entity.name.function', settings: { foreground: '#6f42c1' } },
    { scope: 'storage.type', settings: { foreground: '#d73a49' } },
    { scope: 'variable', settings: { foreground: '#e36209' } },
    { scope: 'support', settings: { foreground: '#005cc5' } },
  ],
  colors: { 'editor.background': '#ffffff', 'editor.foreground': '#24292e' },
}

const dslThemeDark = {
  name: 'vtk-dsl-dark',
  type: 'dark',
  settings: [
    { scope: 'keyword.control.dsl', settings: { foreground: '#ef5350' } },
    { scope: 'entity.name.type.dsl', settings: { foreground: '#ce93d8' } },
    { scope: 'keyword.operator.with.dsl', settings: { foreground: '#ffb74d' } },
    { scope: 'entity.name.tag.dsl', settings: { foreground: '#81c784' } },
    { scope: 'keyword.other.called.dsl', settings: { foreground: '#9e9e9e' } },
    { scope: 'variable.other.label.dsl', settings: { foreground: '#e0e0e0' } },
    { scope: 'keyword.other.connector.dsl', settings: { foreground: '#9e9e9e' } },
    { scope: 'constant.numeric.dsl', settings: { foreground: '#64b5f6' } },
    { scope: 'constant.other.array.dsl', settings: { foreground: '#64b5f6' } },
    { scope: 'constant.other.string.dsl', settings: { foreground: '#64b5f6' } },
    { scope: 'comment', settings: { foreground: '#6a9955' } },
    { scope: 'keyword', settings: { foreground: '#569cd6' } },
    { scope: 'string', settings: { foreground: '#ce9178' } },
    { scope: 'constant.numeric', settings: { foreground: '#b5cea8' } },
    { scope: 'entity.name.function', settings: { foreground: '#dcdcaa' } },
    { scope: 'storage.type', settings: { foreground: '#569cd6' } },
    { scope: 'variable', settings: { foreground: '#9cdcfe' } },
    { scope: 'support', settings: { foreground: '#4ec9b0' } },
  ],
  colors: { 'editor.background': '#1e1e1e', 'editor.foreground': '#d4d4d4' },
}

export default defineConfig({
  title: 'VTK Python Examples',
  description: 'A browsable gallery of VTK Python examples with DSL mappings',
  cleanUrls: true,
  markdown: {
    languages: [dslLang as any],
    theme: {
      light: dslThemeLight as any,
      dark: dslThemeDark as any,
    },
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
