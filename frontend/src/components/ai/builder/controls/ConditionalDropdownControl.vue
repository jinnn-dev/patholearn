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
import { ConditionalDatasetMap } from '../../../../model/ai/datasets/dataset';
import { validateUserSolutionAnnotations } from 'core/viewer/helper/validateAnnotations';
interface DataInterface {
  id: string;
  label: string;
  value: string;
  setValue: Function;
  lockStatus: LockStatus;
  conditionalMap: ConditionalDatasetMap<any>;
}

const props = defineProps({
  data: Object as PropType<DataInterface>,
  seed: Number
});

const selectedValue = ref(props.data?.value);
const values = ref<any[] | undefined>([]);

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

const updateValues = () => {
  if (builderState.selectedDatasset) {
    values.value = props.data?.conditionalMap[builderState.selectedDatasset.dataset_type]!;
    if (!values.value.includes(selectedValue.value)) {
      valueChanged(values.value[0]);
    }
  }
};

onMounted(() => {
  updateValues();
});

watch(
  () => props.data?.value,
  () => {
    if (props.data?.lockStatus?.lockedBy) {
      selectedValue.value = props.data?.value;
    }
  }
);

watch(
  () => builderState.selectedDatasset,
  () => {
    updateValues();
  }
);
</script>
<template>
  <dropdown
    :id="data?.id"
    :label="data?.label"
    :values="values"
    :value="data?.value"
    :lock-status="data?.lockStatus"
    no-select-string="Pick a dataset first"
    @value-changed="valueChanged"
    @on-focus="onFocus"
    @on-focus-out="onFocusOut"
  ></dropdown>
</template>
