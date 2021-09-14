import { defineConfig } from 'vite-plugin-windicss';
import formsPlugin from 'windicss/plugin/forms';

export default defineConfig({
  darkMode: 'class',

  theme: {
    extend: {
      animation: {
        skeleton: 'pulse 1.5s ease-in-out infinite'
      },
      colors: {
        gray: {
          100: '#DEE3EA',
          200: '#B2BDCD',
          300: '#5D7290',
          400: '#4F617A',
          500: '#404F64',
          600: '#333D4D',
          700: '#242C37',
          800: '#151A21',
          900: '#0B0E11'
        },

        highlight: {
          100: '#FFE0B2',
          200: '#FFCC80',
          300: '#FFB74D',
          400: '#FFA726',
          500: '#FF9800',
          600: '#FB8C00',
          700: '#F57C00',
          800: '#EF6C00',
          900: '#E65100'
        }
      }
    }
  },
  plugins: [formsPlugin]
});
