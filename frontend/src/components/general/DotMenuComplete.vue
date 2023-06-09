<script setup lang="ts">
import { onClickOutside } from '@vueuse/core';
import { ref } from 'vue';
import Icon from './Icon.vue';
import DotMenu from './DotMenu.vue';
const target = ref(null);
const dotMenuOpen = ref(false);

defineEmits(['delete', 'edit']);

onClickOutside(target, () => (dotMenuOpen.value = false));
</script>
<template>
  <div class="relative">
    <Icon
      class="cursor-pointer rounded-md hover:bg-gray-500"
      name="dots-three-vertical"
      weight="bold"
      @click.prevent.stop="dotMenuOpen = !dotMenuOpen"
    ></Icon>
    <dot-menu ref="target" :optionsOpen="dotMenuOpen" @delete="$emit('delete')" @edit="$emit('edit')" />
  </div>
</template>
