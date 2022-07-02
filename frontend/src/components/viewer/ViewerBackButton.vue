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
  <router-link :to='routeName' class='flex items-center rounded-lg'>
    <primary-button bgColor='bg-gray-700' class='fixed top-3 left-3 z-10 w-auto shadow-md'>
      <Icon name='arrow-left' />
      <div class='ml-1'>{{ text }}</div>
    </primary-button>
  </router-link>
</template>
