<script lang='ts' setup>
import PrimaryButton from '../general/PrimaryButton.vue';
import Icon from '../general/Icon.vue';

defineProps({
  routeName: {
    type: String,
    required: true
  },
  text: {
    type: String,
    default: 'Zurück zur Aufgabengruppe'
  }
});
</script>

<template>
  <router-link class='flex items-center rounded-lg' :to='routeName'>
    <primary-button class='fixed top-4 left-2 z-10 w-auto shadow-md' bgColor='bg-gray-700'>
      <Icon name='arrow-left' />
      <div class='ml-1'>{{ text }}</div>
    </primary-button>
  </router-link>
</template>
