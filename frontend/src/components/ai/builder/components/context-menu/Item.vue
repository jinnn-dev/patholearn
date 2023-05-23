<script setup lang="ts">
import { debounce } from './debounce';
import Block from './Block.vue';
import { PropType, onMounted, ref } from 'vue';

const props = defineProps({
  subitems: {
    type: Array as PropType<any[]>
  },
  delay: {
    type: Number,
    default: 200
  }
});

defineEmits(['select', 'hide']);

const visibleSubitems = ref();
const hide = debounce(props.delay, hideSubitems);

function hideSubitems() {
  visibleSubitems.value = false;
}
</script>
<template>
  <block
    class="relative p-1 rounded-lg bg-gray-800 cursor-pointer w-full hover:ring-1 hover:ring-gray-500 hover:bg-gray-600"
    :class="{ hasSubitems: subitems }"
    @click.stop="
      $emit('select', $event);
      $emit('hide');
    "
    @wheel.stop=""
    @pointerover="
      hide.cancel();
      visibleSubitems = true;
    "
    @pointerleave="hide.call()"
    @pointerdown.stop=""
    data-testid="context-menu-item"
  >
    <slot></slot>
    <div class="absolute top-0 left-full w-fit-content px-2" v-if="subitems && visibleSubitems">
      <item
        v-for="item of subitems"
        :key="item.key"
        @select="item.handler($event)"
        :delay="0"
        @hide="$emit('hide')"
        :subitems="item.subitems"
        >{{ item.label }}</item
      >
    </div>
  </block>
</template>
<style scoped>
.hasSubitems::after {
  content: '►';
  position: absolute;
  opacity: 0.6;
  right: 5px;
  top: 5px;
}
</style>
