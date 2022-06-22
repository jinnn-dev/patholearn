<script lang='ts' setup>
import Navigation from '../Navigation.vue';
</script>
<template>
  <div>
    <navigation></navigation>
    <div>
      <div class='text-center text-5xl pt-8'>
        <slot name='header'></slot>
      </div>
      <div class='flex justify-center mt-12'>
        <div class='w-11/12 mb-8'>
          <slot name='content'></slot>
        </div>
      </div>
    </div>
  </div>
</template>

