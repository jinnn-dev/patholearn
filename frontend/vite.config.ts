import vue from '@vitejs/plugin-vue';
import { visualizer } from 'rollup-plugin-visualizer';
import Components from 'unplugin-vue-components/vite';
import { defineConfig } from 'vite';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    Components({
      dts: true
    }),
    visualizer(),
    vue()
  ]
});
