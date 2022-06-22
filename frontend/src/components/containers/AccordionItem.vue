<script lang='ts' setup>
import { inject, Ref, ref, watch } from 'vue';
import { nanoid } from 'nanoid';
import CollapseTransition from './CollapseTransition.vue';
import Icon from '../general/Icon.vue';

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  first: {
    type: Boolean,
    default: false
  }
});

const expand = ref(false);
const selectedIndex = inject<Ref>('selectedIndex');
const collapse = inject<Ref>('collapse');
const index = nanoid(5);

if (props.first) {
  expand.value = true;
}

watch(
  () => selectedIndex,
  () => {
    if (collapse) {
      expand.value = selectedIndex?.value === index;
    }
  },
  { deep: true }
);

function toggleDisplay() {
  if (index === selectedIndex?.value) {
    expand.value = !expand.value;
  }
}
</script>
<template>
  <div>
    <div
      id='accordion-item-header'
      :class="expand ? 'rounded-t-lg' : 'rounded-lg'"
      class='flex items-center bg-gray-500 p-2 hover:underline cursor-pointer'
      @click='
        $parent.select(index);
        toggleDisplay();
      '
    >
      <Icon
        :class="expand ? 'rotate-45' : 'rotate-0'"
        class='mr-1'
        height='20'
        name='caret-right'
        strokeWidth='24'
        width='20'
      />
      <span class='font-semibold'>{{ title }}</span>
      <slot name='header'></slot>
    </div>
    <collapse-transition>
      <div v-if='expand' class='bg-gray-700 p-2 rounded-b-lg border-b-2 border-x-2 border-gray-500'>
        <slot></slot>
      </div>
    </collapse-transition>
  </div>
</template>
