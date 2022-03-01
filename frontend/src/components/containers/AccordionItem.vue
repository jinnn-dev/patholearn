<template>
  <div class="mb-4">
    <div
      id="accordion-item-header"
      @click="
        $parent.select(index);
        toggleDisplay();
      "
      class="flex items-center bg-gray-700/60 p-2 hover:underline cursor-pointer"
      :class="expand ? 'rounded-t-lg' : 'rounded-lg'"
    >
      <Icon
        name="caret-right"
        height="20"
        width="20"
        class="mr-1 transform"
        :class="expand ? 'rotate-45' : 'rotate-0'"
        strokeWidth="24"
      />
      <span class="font-semibold">{{ title }}</span>
    </div>
    <collapse-transition>
      <div v-if="expand" class="bg-gray-700 p-2 rounded-b-lg">
        <slot></slot>
      </div>
    </collapse-transition>
  </div>
</template>
<script lang="ts">
import { nanoid } from 'nanoid';
import { defineComponent, inject, ref, Ref, watch } from 'vue';
export default defineComponent({
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
