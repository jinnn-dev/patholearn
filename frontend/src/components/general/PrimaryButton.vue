<script lang='ts' setup>
import { computed } from 'vue';

const props = defineProps({
  name: String,
  bgColor: {
    type: String,
    default: 'bg-highlight-900'
  },
  bgHoverColor: {
    type: String
  },
  fontWeight: {
    type: String,
    default: 'font-medium'
  },
  textColor: {
    type: String,
    default: 'text-white'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  type: {
    type: String,
    default: 'submit'
  }
});

const generatedBgColor = computed(() => {
  const colors = props.bgColor.split('-');

  return colors[0] + '-' + colors[1] + '-' + (+colors[2] - 200);
});
</script>
<template>
  <button
    :class="`${bgColor} ${fontWeight} ${textColor} ${
      disabled ? 'cursor-not-allowed' : `cursor-pointer hover:${bgHoverColor || generatedBgColor}  hover:ring-2`
    }`"
    :disabled='disabled'
    :type='type'
    class='flex justify-center items-center w-full transition rounded-lg py-2 text-md px-2 ring-gray-100 w-full min-w-[4rem]'
  >
    <slot></slot>
    {{ name }}
    <slot class='self-end' name='rightIcon'></slot>
  </button>
</template>
