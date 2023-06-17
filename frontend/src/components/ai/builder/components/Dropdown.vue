<script setup lang="ts">
import { PropType, computed, ref, watch } from 'vue';
import CustomSelect from '../../../form/CustomSelect.vue';
import Icon from '../../../general/Icon.vue';
import { builderState, isTraining } from '../../../../core/ai/builder/state';
import { LockStatus } from 'core/ai/builder/sync';

const props = defineProps({
  id: String,
  label: String,
  values: Array,
  value: String,
  lockStatus: Object as PropType<LockStatus>
});

const emit = defineEmits(['valueChanged', 'onFocus', 'onFocusOut']);

const isExpanded = ref(false);

const container = ref<HTMLElement | null>(null);

const selectedValue = ref(props.value || props.values![0]);

const valueChanged = (change: any) => {
  selectedValue.value = change;
  container.value?.blur();
  emit('valueChanged', change);
};

const onFocusOut = () => {
  if (isDisbaled.value) {
    return;
  }
  isExpanded.value = false;
  emit('onFocusOut');
};

const onFocus = () => {
  if (isDisbaled.value) {
    container.value?.blur();

    return;
  }
  isExpanded.value = true;
  emit('onFocus');
};
const isDisbaled = computed(() => props.lockStatus?.externalLock !== undefined || isTraining.value);

watch(
  () => props.value,
  () => {
    if (props.lockStatus?.lockedBy && props.value) {
      selectedValue.value = props.value;
    }
  }
);

const computedClasses = computed(() => {
  const classes = [];
  if (props.lockStatus?.lockedControlId === props?.id) {
    classes.push('ring-2');
  } else {
    classes.push('ring-1');
  }

  if (isDisbaled.value) {
    classes.push('text-gray-200 bg-gray-500/50 ring-gray-500');
  }
  return classes.join(' ');
});
</script>
<template>
  <div class="mb-1" v-if="label">{{ label }}:</div>
  <div
    ref="container"
    class="relative focus:outline-none focus:ring-2 focus:ring-highlight-500 rounded-lg"
    tabindex="0"
    @focusout="onFocusOut"
    @focus="onFocus"
  >
    <div
      class="flex justify-between ring-gray-400 w-full bg-gray-500 py-0.5 items-center px-2 rounded-lg focus:ring-highlight-500 focus:ring-2 focus:outline-none"
      :style="lockStatus?.lockedControlId === id ? `--tw-ring-color: ${lockStatus?.lockedBy.info.color};` : ''"
      :class="computedClasses"
    >
      <div>{{ selectedValue }}</div>
      <icon name="caret-up-down" stroke-width="0" size="16"></icon>
    </div>
    <div
      v-if="isExpanded"
      class="absolute shadow-lg shadow-gray-800 z-10 w-full overflow-hidden bg-gray-500 top-9 rounded-lg ring-1 ring-gray-300"
    >
      <div v-for="value in values" class="px-2 py-0.5 hover:bg-gray-400" @click="valueChanged(value)">
        {{ value }}
      </div>
    </div>
  </div>
</template>
