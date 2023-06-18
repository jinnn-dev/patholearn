<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { builderState } from '../../../../core/ai/builder/state';
import Dropdown from '../components/Dropdown.vue';
import AnimatedNumber from '../components/AnimatedNumber.vue';
import TripleMetric from '../components/metrics/TripleMetric.vue';
import EpochMetric from '../components/metrics/EpochMetric.vue';
import { MetricDisplayName, MetricVariableMapping } from '../../../../core/ai/builder/controls';

const props = defineProps({
  data: Object,
  seed: Number
});

const isNotTripeMetric = computed(() => selectedValue.value === 'Epoch');

const selectedValue = ref<MetricDisplayName>(props.data?.value || props.data?.values[0]);

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
</script>
<template>
  <div class="flex flex-col h-full">
    <dropdown
      :id="data?.id"
      :values="data?.values"
      :value="data?.value"
      :lock-status="data?.lockStatus"
      @value-changed="valueChanged"
      @on-focus="onFocus"
      @on-focus-out="onFocusOut"
    ></dropdown>
    <div class="h-full flex justify-center items-center">
      <epoch-metric v-if="isNotTripeMetric"></epoch-metric>
      <triple-metric v-else :metric-key="MetricVariableMapping[selectedValue]"></triple-metric>
    </div>
  </div>
</template>
