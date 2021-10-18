<template>
  <div class="w-full bg-gray-800 text-gray-100 min-h-screen">
    <router-view />
  </div>
  <error-bar></error-bar>
</template>

<script lang="ts">
import { User } from './model/user';
import { defineComponent, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

export default defineComponent({
  name: 'App',

  setup() {
    const user = ref<User>();
    const route = useRoute();
    onMounted(async () => {});

    return { user, route };
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
  @apply bg-gray-700 !important;
  @apply text-gray-100;
}
.tippy-backdrop {
  @apply bg-gray-700 !important;
  @apply text-gray-100;
}

.tippy-content[data-theme~='myDark'] {
  @apply bg-gray-700 !important;
  @apply text-gray-100;
}

.tippy-box[data-theme~='myDark'][data-placement^='top'] > .tippy-arrow::before {
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
}

.tippy-array {
  @apply text-gray-700 !important;
  @apply bg-gray-700 !important;
}
</style>
