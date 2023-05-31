<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import CustomSelect from '../../../form/CustomSelect.vue';
import Icon from '../../../general/Icon.vue';
import { builderState } from '../../../../core/ai/builder/state';

const props = defineProps({
  data: Object,
  seed: Number
});

const isExpanded = ref(false);

const container = ref<HTMLElement | null>(null);

const selectedValue = ref(props.data?.value || props.data?.values[0]);

const valueChanged = (change: any) => {
  props.data!.setValue(change);
  selectedValue.value = change;
  builderState.syncPlugin?.controlChanged(props.data!.id, change);
  container.value?.blur();
};

const onFocusOut = () => {
  if (isDisbaled.value) {
    return;
  }
  isExpanded.value = false;
  builderState.syncPlugin?.unselectControl(props.data!.id);
};

const onFocus = () => {
  console.log(props.data?.lockStatus);

  if (isDisbaled.value) {
    container.value?.blur();

    return;
  }
  isExpanded.value = true;
  builderState.syncPlugin?.selectControl(props.data!.id);
};
const isDisbaled = computed(() => props.data?.lockStatus?.externalLock !== undefined);

watch(
  () => props.data?.value,
  () => {
    if (props.data?.lockStatus?.lockedBy) {
      selectedValue.value = props.data?.value;
    }
  }
);

const computedClasses = computed(() => {
  const classes = [];
  if (props.data?.lockStatus?.lockedControlId === props.data?.id) {
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
  <div class="mb-1">{{ data?.label }}:</div>
  <div
    ref="container"
    class="relative focus:outline-none focus:ring-2 focus:ring-highlight-500 rounded-lg"
    tabindex="0"
    @focusout="onFocusOut"
    @focus="onFocus"
  >
    <div
      class="flex justify-between ring-gray-400 w-full bg-gray-500 py-0.5 items-center px-2 rounded-lg focus:ring-highlight-500 focus:ring-2 focus:outline-none"
      :style="
        data?.lockStatus?.lockedControlId === data?.id
          ? `--tw-ring-color: ${data?.lockStatus.lockedBy.info.color};`
          : ''
      "
      :class="computedClasses"
    >
      <div>{{ selectedValue }}</div>
      <icon name="caret-up-down" stroke-width="0" size="16"></icon>
    </div>

    <div
      v-if="isExpanded"
      class="absolute shadow-lg shadow-gray-800 z-10 w-full overflow-hidden bg-gray-500 top-9 rounded-lg ring-1 ring-gray-300"
    >
      <div v-for="value in data?.values" class="px-2 py-0.5 hover:bg-gray-400" @click="valueChanged(value)">
        {{ value }}
      </div>
    </div>
  </div>
</template>
