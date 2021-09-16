import vue from '@vitejs/plugin-vue';
import { visualizer } from 'rollup-plugin-visualizer';
import Components from 'unplugin-vue-components/vite';
import { defineConfig } from 'vite';
import WindiCSS from 'vite-plugin-windicss';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    Components({
      dts: true
    }),
    visualizer(),
    vue(),
    WindiCSS({
      safelist: [
        'stroke-green-500',
        'text-lg',
        'w-2/7',
        'w-2/4',
        'w-[700px]',
        'bg-green-500',
        'font-semibold',
        'group-hover:block',
        'border-green-500',
        'border-red-500',
        'border-yellow-500',
        'text-green-500',
        'text-red-500',
        'text-yellow-500',
        'hover:bg-highlight-600',
        'bg-highlight-800',
        'hover:bg-gray-300',
        'hover:bg-gray-400',
        'hover:bg-gray-500',
        'hover:bg-gray-600',
        'hover:bg-gray-700'
      ]
    })
  ]
});
