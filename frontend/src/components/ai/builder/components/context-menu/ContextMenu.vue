<script setup lang="ts">
import { PropType, ref } from 'vue';
import { debounce } from './debounce';
import Block from './Block.vue';
import Search from './Search.vue';
import Item from './Item.vue';

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
  <div class="context-menu" @mouseover="hide.cancel()" @mouseleave="hide.call()" data-testid="context-menu">
    <block v-if="searchBar">
      <search :text="filter" @change="filter = $event"></search>
    </block>
    <item
      class="item"
      v-for="item of getItems()"
      :key="item.key"
      @select="item.handler($event)"
      :delay="delay"
      @hide="$emit('hide')"
      :subitems="item.subitems"
      >{{ item.label }}</item
    >
  </div>
</template>
<style>
/* Context menu */

.search {
  color: #acadae !important;
  background-color: rgba(91, 93, 96, 0.8) !important;
  border-radius: 3px 3px 0 0 !important;
  border: 1px solid transparent !important;
}

.context-menu {
  font-family: 'Consolas', monospace !important;
  background-color: transparent !important;
  border-radius: 3px 3px 0 0 !important;
  border: 1px solid transparent !important;

  padding: 10px;
  width: 200px !important;
}

.context-menu .item,
.context-menu .subitem {
  border-radius: 0 !important;
  color: #000 !important;
  padding: 4px;
  border-bottom: 1px solid grey !important;
  background-color: rgba(128, 128, 128, 0.9) !important;
  cursor: pointer;
  width: 100%;
  position: relative;
}

.context-menu .item:hover,
.context-menu .subitem:hover {
  background-color: rgba(156, 156, 156, 0.9) !important;
}

.context-menu .search {
  background-color: rgba(91, 93, 96, 0.8) !important;
}

.context-menu .item.hasSubitems:after {
  content: '►' !important;
  position: absolute;
  opacity: 0.6;
  right: 5px;
  top: 5px;
}

.context-menu .item .subitems {
  position: absolute;
  top: 0;
  left: 100%;
  width: 120px;
}
</style>
