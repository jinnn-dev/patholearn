import vue from '@vitejs/plugin-vue';
import { defineConfig } from 'vite';
import { visualizer } from 'rollup-plugin-visualizer';
import Markdown from 'unplugin-vue-markdown/vite';
import prism from 'markdown-it-prism';
import markdownItPrismBackticks from 'markdown-it-prism-backticks';
import mathjax from 'markdown-it-mathjax3';
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({
      include: [/\.vue$/, /\.md$/]
    }),
    Markdown({ markdownItUses: [prism, markdownItPrismBackticks, mathjax], frontmatter: true }),
    visualizer()
  ]
});
