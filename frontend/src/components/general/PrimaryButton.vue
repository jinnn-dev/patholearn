<script lang="ts" setup>
import { computed, PropType } from 'vue';

type ButtonTypes = 'button' | 'submit' | 'reset';

const props = defineProps({
  name: String,
  bgColor: {
    type: String,
    default: 'bg-highlight-900'
  },
  bgHoverColor: {
    type: String
  },
  paddingHorizontal: {
    type: String,
    default: 'py-2'
  },
  paddingVertical: {
    type: String,
    default: 'px-2'
  },
  fontWeight: {
    type: String,
    default: 'font-medium'
  },
  fontSize: {
    type: String,
    default: 'text-md'
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
    type: String as PropType<ButtonTypes>,
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
    :class="`${bgColor} ${fontWeight} ${textColor} ${paddingHorizontal} ${paddingVertical} ${fontSize} ${
      disabled ? 'cursor-not-allowed' : `cursor-pointer hover:${bgHoverColor || generatedBgColor}  hover:ring-2`
    }`"
    :disabled="disabled"
    :type="type"
    class="flex justify-center items-center transition rounded-lg ring-gray-100 w-full min-w-[4rem]"
  >
    <slot></slot>
    {{ name }}
    <slot class="self-end" name="rightIcon"></slot>
  </button>
</template>
