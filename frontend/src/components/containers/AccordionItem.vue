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
      @click='
        $parent.select(index);
        toggleDisplay();
      '
      class='flex items-center bg-gray-500 p-2 hover:underline cursor-pointer'
      :class="expand ? 'rounded-t-lg' : 'rounded-lg'"
    >
      <Icon
        name='caret-right'
        height='20'
        width='20'
        class='mr-1'
        :class="expand ? 'rotate-45' : 'rotate-0'"
        strokeWidth='24'
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