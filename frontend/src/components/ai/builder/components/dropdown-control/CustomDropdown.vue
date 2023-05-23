<script setup lang="ts">
import CustomSelect from '../../../../form/CustomSelect.vue';

const props = defineProps({
  data: Object
});

const valueChanged = (change: any) => {
  props.data!.setValue(change);
};
</script>
<template>
  <custom-select
    @pointerdown.stop=""
    :values="data?.values"
    display-type="small"
    :is-searchable="false"
    :label="data?.label"
    empty-string="(Empty)"
    :initial-data="data?.value || data?.values[0]"
    @value-changed="valueChanged"
  ></custom-select>
</template>
