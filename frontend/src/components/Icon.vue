<template>
  <div class="icon">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      :width="width"
      :height="height"
      :viewBox.camel="viewBox"
      v-bind="$attrs"
      v-html="icon"
      class="stroke-current fill-current"
      :stroke-width="strokeWidth"
    ></svg>
  </div>
</template>
<script lang="ts">
import { defineComponent, computed, PropType } from 'vue';
import { IconNames, Icon } from '../../icons';

let lib: Icon[] = [];

export default defineComponent({
  props: {
    name: {
      type: String as PropType<IconNames>,
      default: ''
    },
    iconStyle: {
      type: String,
      default: 'line'
    },
    width: {
      type: [String, Number],
      default: 24
    },
    height: {
      type: [String, Number],
      default: 24
    },
    strokeWidth: {
      type: [String, Number],
      default: 16
    },
    viewBox: {
      type: String,
      default: '0 0 256 256'
    }
  },

  add(icons: Icon[] | Icon) {
    if (Array.isArray(icons)) {
      lib = icons;
    } else {
      lib.push(icons);
    }
  },

  setup(props) {
    const icon = computed(() => {
      const icon = lib.find((i) => i.name === props.name && i.style === props.iconStyle);
      if (icon) {
        return icon.path;
      } else {
        console.error(`Name '${props.name}' of the icon is not correct`);
        return undefined;
      }
    });

    return {
      icon
    };
  }
});
</script>
<style></style>

<!-- inspired by https://github.com/antonreshetov/vue-unicons -->
