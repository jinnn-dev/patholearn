<script setup lang="ts">
import { PropType, computed, onMounted, ref, watch } from 'vue';
import CustomSelect from '../../../form/CustomSelect.vue';
import Icon from '../../../general/Icon.vue';
import { builderState, versionHasStatus } from '../../../../core/ai/builder/state';
import Dropdown from '../components/Dropdown.vue';
import { LockStatus } from '../../../../core/ai/builder/sync';
import { AsyncFunctionName, asyncFunctionMapping } from '../../../../core/ai/builder/controls/async-dropdown-control';
import { useService } from '../../../../composables/useService';
import Spinner from '../../../general/Spinner.vue';

interface DataInterface {
  id: string;
  label: string;
  value: string;
  setValue: Function;
  asyncFunction: AsyncFunctionName;
  lockStatus: LockStatus;
}

const props = defineProps({
  data: Object as PropType<DataInterface>,
  seed: Number
});

const { loading, result, run } = useService(asyncFunctionMapping[props.data!.asyncFunction]);

const selectedValue = ref(props.data?.value);

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

onMounted(async () => {
  await run();
});

watch(
  () => props.data?.value,
  () => {
    console.log('MOUNTING');

    if (props.data?.lockStatus?.lockedBy) {
      selectedValue.value = props.data?.value;
    }
  }
);
</script>
<template>
  <div v-if="loading" class="flex items-center justify-center gap-2 h-full">
    <div class="scale-75">
      <spinner></spinner>
    </div>
    <div class="text-sm">Loading datasets</div>
  </div>
  <dropdown
    v-else
    :id="data?.id"
    :label="data?.label"
    :values="result"
    :value="data?.value"
    :lock-status="data?.lockStatus"
    display-field="name"
    @value-changed="valueChanged"
    @on-focus="onFocus"
    @on-focus-out="onFocusOut"
  ></dropdown>
</template>
