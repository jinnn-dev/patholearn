<script lang='ts' setup>
defineProps({
  text: String,
  textSize: {
    type: String,
    default: 'text-xl'
  },
  iconSize: {
    type: String,
    default: 'w-32'
  }
});
</script>
<template>
  <div class='flex w-full justify-center'>
    <div class='flex flex-col justify-center w-full'>
      <div class='flex justify-center'>
        <img :class='iconSize' alt='no Content' src='../../assets/no_content.svg' />
      </div>
      <div :class='textSize' class='text-center mt-3 font-medium text-gray-200'>
        {{ text }}
      </div>
    </div>
  </div>
</template>
