<script setup lang="ts">
import { PropType, ref } from 'vue';
import { debounce } from './debounce';
import Block from './Block.vue';
import Search from './Search.vue';
import Item from './Item.vue';
import { versionHasStatus } from '../../../../core/ai/builder/state';

const props = defineProps({
  items: {
    type: Array as PropType<any[]>,
    default: []
  },
  delay: {
    type: Number,
    default: 200
  },
  searchBar: Boolean,
  onHide: {
    type: Function as PropType<() => void>,
    required: true
  }
});

const filter = ref();
const hide = debounce(props.delay, props.onHide);

function getItems() {
  const filterRegexp = new RegExp(filter.value, 'i');
  const filteredList = props.items.filter((item) => item.label.match(filterRegexp));
  return filteredList;
}
</script>
<template>
  <div
    class="bg-gray-700 p-2 w-36 rounded-lg shadow-md shadow-gray-900"
    @mouseover="hide.cancel()"
    @mouseleave="hide.call()"
    data-testid="context-menu"
    v-if="items.length !== 0 && !versionHasStatus"
  >
    <!-- <block v-if="searchBar">
      <search :text="filter" @change="filter = $event"></search>
    </block> -->
    <item
      class="my-1"
      v-for="item of getItems()"
      :key="item.key"
      @select="item.handler($event)"
      :delay="0"
      @hide="$emit('hide')"
      :subitems="item.subitems"
      >{{ item.label }}</item
    >
  </div>
</template>
<style></style>
