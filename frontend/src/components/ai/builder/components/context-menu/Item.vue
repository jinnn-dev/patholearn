<script setup lang="ts">
import { debounce } from './debounce';
import Block from './Block.vue';
import { PropType, ref } from 'vue';

const props = defineProps({
  subitems: {
    type: Array as PropType<any[]>
  },
  delay: {
    type: Number,
    default: 200
  }
});

const visibleSubitems = ref();
const hide = debounce(props.delay, hideSubitems);

function hideSubitems() {
  visibleSubitems.value = false;
}
</script>
<template>
  <block
    class="item cursor-pointer hover:bg-gray-500"
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
    <div class="subitems" v-if="subitems &amp;&amp; visibleSubitems">
      <item
        v-for="item of subitems"
        :key="item.key"
        @select="item.handler($event)"
        :delay="delay"
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

.subitems {
  position: absolute;
  top: 0;
  left: 100%;
  width: fit-content;
}
</style>
