<script lang='ts' setup>
import Icon from './general/Icon.vue';

defineProps({
  link: String,
  linkText: String,
  text: String,
  subText: String
});
</script>
<template>
  <div class='flex justify-center w-full'>
    <div id='test' class='flex w-11/12 relative items-center bg-gray-700 rounded-xl bg-opacity-40 py-5'>
      <div class='flex transition ml-2 text-xl items-center cursor-pointer hover:text-highlight-500 absolute'>
        <router-link :to='link' class='flex p-2 items-center text-base lg:text-xl'>
          <Icon class='mr-2' name='arrow-left' />
          {{ linkText }}
        </router-link>
      </div>
      <div class='w-full flex flex-col gap-4'>
        <h1 class='text-lg md:text-2xl lg:text-4xl xl:text-5xl flex-1'>
          {{ text || 'Loading...' }}
        </h1>
        <h2 v-if='subText' class='text-2xl'>
          {{ subText }}
        </h2>
      </div>
    </div>
  </div>
</template>
