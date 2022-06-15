<template>
  <!--  <div-->
  <!--    class='hidden backdrop-blur backdrop-blur-0 backdrop-blur-sm backdrop-blur-md backdrop-blur-lg backdrop-blur-xl backdrop-blur-2xl backdrop-blur-3xl'></div>-->
  <div class='w-full bg-gray-800 text-gray-100 min-h-screen'>
    <div
      v-if='showBrowserWarning'
      class='absolute right-5 top-5 border-red-500 border-2 px-10 py-5 bg-red-500/20 rounded-lg'
    >
      <p class='text-lg'>Dein Browser wird von dieser Software nicht unterstützt!</p>
      <p class='text-sm text-gray-200'>Bitte wechsel zu einem Chromium-basierten Browser wie Chrome oder Edge</p>
    </div>
    <router-view />
  </div>
  <error-bar></error-bar>
</template>

<script lang='ts'>
import { detect } from 'detect-browser';
import { defineComponent, onMounted, ref } from 'vue';
import { getEnv } from './config';

export default defineComponent({
  name: 'App',

  setup() {
    onMounted(async () => {
    });

    const title = getEnv('APP_TITLE');
    document.title = title || '';

    //set favicon dynamicly
    var link = document.querySelector('link[rel~=\'icon\']');
    if (!link) {
      link = document.createElement('link');
      link.rel = 'icon';
      document.getElementsByTagName('head')[0].appendChild(link);
    }
    link.href = '/' + getEnv('APP_FAVICON_URL') || '';

    const showBrowserWarning = ref(false);

    const detectedBrowser = detect();
    if (detectedBrowser) {
      switch (detectedBrowser.name) {
        case 'chrome':
          break;
        case 'edge-chromium':
          break;
        case 'opera':
          break;

        default:
          showBrowserWarning.value = true;
          break;
      }
    }

    return { showBrowserWarning };
  }
});
</script>

<style>
@font-face {
  font-family: 'Poppins';
  src: url('/Poppins/Poppins-Light.ttf') format('truetype');
  font-weight: 300;
  font-style: normal;
}

@font-face {
  font-family: 'Poppins';
  src: url('/Poppins/Poppins-Regular.ttf') format('truetype');
  font-weight: 400;
  font-style: normal;
}

@font-face {
  font-family: 'Poppins';
  src: url('/Poppins/Poppins-Medium.ttf') format('truetype');
  font-weight: 500;
  font-style: normal;
}

@font-face {
  font-family: 'Poppins';
  src: url('/Poppins/Poppins-SemiBold.ttf') format('truetype');
  font-weight: 600;
  font-style: normal;
}

@font-face {
  font-family: 'Poppins';
  src: url('/Poppins/Poppins-Bold.ttf') format('truetype');
  font-weight: 700;
  font-style: normal;
}

@font-face {
  font-family: 'Poppins';
  src: url('/Poppins/Poppins-ExtraBold.ttf') format('truetype');
  font-weight: 800;
  font-style: normal;
}

#app {
  font-family: 'Poppins', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100%;
}

kbd {
  @apply bg-gray-400;
  @apply py-1;
  @apply px-2;
  @apply border-2;
  @apply border-gray-500;
  @apply rounded-lg;
}

input[type='color'] {
  -webkit-appearance: none;
  border: none;
  width: 100%;
  min-height: 100%;
}

input[type='color']::-webkit-color-swatch-wrapper {
  padding: 0;
}

input[type='color']::-webkit-color-swatch {
  border: none;
}

::-webkit-scrollbar {
  width: 5px;
  height: 5px;
}

::-webkit-scrollbar-button {
  width: 1px;
  height: 1px;
}

::-webkit-scrollbar-thumb {
  background: #b3b3b3;
  border: 0px none #ffffff;
  border-radius: 100px;
}

::-webkit-scrollbar-thumb:hover {
  background: #878787;
}

::-webkit-scrollbar-thumb:active {
  background: #6b6b6b;
}

::-webkit-scrollbar-track {
  background: #666666;
  border: 16px none #ffffff;
  border-radius: 100px;
}

::-webkit-scrollbar-track:hover {
  background: #666666;
}

::-webkit-scrollbar-track:active {
  background: #333333;
}

::-webkit-scrollbar-corner {
  background: transparent;
}

::selection {
  @apply bg-highlight-900;
  @apply text-white;
}

::-moz-selection {
  @apply bg-highlight-900;
  @apply text-white;
}

.tippy-box[data-theme~='myDark'] {
  @apply bg-gray-900 !important;
  @apply text-gray-100;
  @apply shadow-lg;
}

.tippy-backdrop {
  @apply bg-gray-900 !important;
  @apply text-gray-100;
}

.tippy-content[data-theme~='myDark'] {
  @apply bg-gray-900 !important;
  @apply text-gray-100;
}

/* .tippy-box[data-theme~='myDark'][data-placement^='top'] > .tippy-arrow::before {
  @apply border-t-gray-700 !important;
}
.tippy-box[data-theme~='myDark'][data-placement^='bottom'] > .tippy-arrow::before {
  @apply border-b-gray-700 !important;
}
.tippy-box[data-theme~='myDark'][data-placement^='left'] > .tippy-arrow::before {
  @apply border-l-gray-700 !important;
}
.tippy-box[data-theme~='myDark'][data-placement^='right'] > .tippy-arrow::before {
  @apply border-r-gray-700 !important;
} */

/* The fill */
.tippy-box[data-theme~='myDark'] > .tippy-svg-arrow > svg:last-child {
  fill: black;
  @apply shadow-lg;
}

.tippy-array {
  @apply text-gray-700 !important;
  @apply bg-gray-700 !important;
}
</style>
