<template>
  <div class="mb-4">
    <div
      id="accordion-item-header"
      :class="expand ? 'rounded-t-lg' : 'rounded-lg'"
      class="flex items-center bg-gray-700/60 p-2 hover:underline cursor-pointer"
      @click="
        $parent.select(index);
        toggleDisplay();
      "
    >
      <Icon
        :class="expand ? 'rotate-45' : 'rotate-0'"
        class="mr-1 transform"
        height="20"
        name="caret-right"
        strokeWidth="24"
        width="20"
      />
      <span class="font-semibold">{{ title }}</span>
    </div>
    <collapse-transition>
      <div v-show="expand" class="bg-gray-700 p-2 rounded-b-lg">
        <slot></slot>
      </div>
    </collapse-transition>
  </div>
</template>
<script lang="ts">
import { nanoid } from 'nanoid';
import { defineComponent, inject, ref, Ref, watch } from 'vue';
import CollapseTransition from './CollapseTransition.vue';
import Icon from '../general/Icon.vue';

export default defineComponent({
  components: { Icon, CollapseTransition },
  props: {
    title: {
      type: String,
      default: ''
    },
    first: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const expand = ref(false);
    const selectedIndex = inject<Ref>('selectedIndex');
    const index = nanoid(5);
    if (props.first) {
      expand.value = true;
    }
    watch(
      () => selectedIndex,
      () => {
        if (selectedIndex?.value === index) {
          expand.value = true;
        } else {
          expand.value = false;
        }
      },
      { deep: true }
    );

    function toggleDisplay() {
      if (index === selectedIndex?.value) {
        expand.value = !expand.value;
      }
    }

    return {
      expand,
      selectedIndex,
      index,
      toggleDisplay
    };
  }
});
</script>
<style></style>
