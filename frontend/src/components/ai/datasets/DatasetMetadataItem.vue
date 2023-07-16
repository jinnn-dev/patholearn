<script setup lang="ts">
import { PropType } from 'vue';
import Icon from '../../general/Icon.vue';
import { IconNames } from '../../../../icons';

type Size = 'normal' | 'big';

defineProps({
  iconName: String as PropType<IconNames>,
  metadata: [String, Number],
  size: {
    type: String as PropType<Size>,
    default: 'normal'
  }
});
</script>
<template>
  <div class="flex items-center rounded-md font-mono" :class="size === 'normal' ? 'text-sm gap-2 ' : 'text-lg gap-4'">
    <icon :name="iconName" stroke-width="0" :size="size === 'normal' ? 24 : 36"></icon>
    <div>
      {{ metadata ? metadata : '-' }}
    </div>
  </div>
</template>
