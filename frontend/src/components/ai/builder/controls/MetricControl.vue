<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { builderState } from '../../../../core/ai/builder/state';
import Dropdown from '../components/Dropdown.vue';
import AnimatedNumber from '../components/AnimatedNumber.vue';

const props = defineProps({
  data: Object,
  seed: Number
});

const selectedValue = ref<string>(props.data?.value || props.data?.values[0]);

const valueChanged = (change: any) => {
  props.data!.setValue(change);
  selectedValue.value = change;
  builderState.syncPlugin?.controlChanged(props.data!.id, change);
};

const onFocusOut = () => {
  builderState.syncPlugin?.unselectControl(props.data!.id);
};

const onFocus = () => {
  builderState.syncPlugin?.selectControl(props.data!.id);
};

const filteredMetric = computed(() => {
  if (!builderState.versionMetrics) {
    return undefined;
  }
  const keys = Object.keys(builderState.versionMetrics);
  const train_key = keys.find((key) => key == 'train_' + selectedValue.value);
  const valid_key = keys.find((key) => key == 'valid_' + selectedValue.value);
  const test_key = keys.find((key) => key == 'test_' + selectedValue.value);

  const result = { train: undefined, valid: undefined, test: undefined };
  if (train_key) {
    result.train = (builderState.versionMetrics as any)[train_key][train_key];
  }
  if (valid_key) {
    result.valid = (builderState.versionMetrics as any)[valid_key][valid_key];
  }

  if (test_key) {
    result.test = (builderState.versionMetrics as any)[test_key][test_key];
  }

  return result;
});
</script>
<template>
  <div class="flex flex-col justify-between">
    <dropdown
      :id="data?.id"
      :values="data?.values"
      :value="data?.value"
      :lock-status="data?.lockStatus"
      @value-changed="valueChanged"
      @on-focus="onFocus"
      @on-focus-out="onFocusOut"
    ></dropdown>
    <div class="flex flex-col justify-center items-center mt-3">
      <div class="text-center">
        <div>Last:</div>
        <animated-number :to="(filteredMetric?.train as any)?.last * 100"></animated-number>
      </div>

      <div class="flex justify-between w-full">
        <div class="flex flex-col justify-center items-center w-full">
          <div>Min:</div>
          <animated-number :to="(filteredMetric?.train as any)?.min * 100"></animated-number>
        </div>
        <div class="flex flex-col justify-center items-center w-full">
          <div>Min:</div>
          <animated-number :to="(filteredMetric?.train as any)?.max * 100"></animated-number>
        </div>
      </div>
    </div>
  </div>
</template>
