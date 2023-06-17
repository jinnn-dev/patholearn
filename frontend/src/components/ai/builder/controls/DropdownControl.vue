<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import CustomSelect from '../../../form/CustomSelect.vue';
import Icon from '../../../general/Icon.vue';
import { builderState, isTraining } from '../../../../core/ai/builder/state';
import Dropdown from '../components/Dropdown.vue';

const props = defineProps({
  data: Object,
  seed: Number
});

const selectedValue = ref(props.data?.value || props.data?.values[0]);

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

watch(
  () => props.data?.value,
  () => {
    if (props.data?.lockStatus?.lockedBy) {
      selectedValue.value = props.data?.value;
    }
  }
);
</script>
<template>
  <dropdown
    :id="data?.id"
    :label="data?.label"
    :values="data?.values"
    :value="data?.value"
    :lock-status="data?.lockStatus"
    @value-changed="valueChanged"
    @on-focus="onFocus"
    @on-focus-out="onFocusOut"
  ></dropdown>
</template>
