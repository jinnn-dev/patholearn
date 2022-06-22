<script lang='ts' setup>
defineProps({
  text: {
    type: String,
    required: true
  }
});
</script>
<template>
  <div class='w-full text-xl font-bold text-gray-200 uppercase'>
    {{ text }}
  </div>
</template>