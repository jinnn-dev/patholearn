<script setup lang="ts">
import { PropType } from 'vue';
import Icon from '../../general/Icon.vue';
import { IconNames } from '../../../../icons';

type Size = 'small' | 'normal' | 'big';

defineProps({
  iconName: String as PropType<IconNames>,
  metadata: [String, Number],
  size: {
    type: String as PropType<Size>,
    default: 'small'
  }
});
</script>
<template>
  <div
    class="flex items-center rounded-md font-mono"
    :class="size === 'small' ? 'text-sm gap-2 ' : size === 'normal' ? 'text-base gap-3' : 'text-lg gap-4'"
  >
    <icon :name="iconName" stroke-width="0" :size="size === 'small' ? 24 : size === 'normal' ? 28 : 36"></icon>
    <div>
      {{ metadata ? metadata : '-' }}
    </div>
  </div>
</template>
