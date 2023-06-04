<script setup lang="ts">
import Prism from 'prismjs';
import 'prismjs/components/prism-python';
import 'prism-themes/themes/prism-one-dark.css';
import { onMounted } from 'vue';

onMounted(() => {
  Prism.highlightAll();
});
</script>
<template>
  <pre><code class="language-py"><slot></slot></code></pre>
</template>
<style>
code[class*='language-'],
pre[class*='language-'] {
  @apply font-mono;
  @apply bg-gray-900;
}
</style>
