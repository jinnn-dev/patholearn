<script lang='ts' setup>
defineProps({
  count: Number
});
</script>
<template>
  <div class='text-gray-200 font-semibold text-sm'>
    {{ count }}
    {{ count === 1 ? 'Aufgabe' : 'Aufgaben' }}
  </div>
</template>
