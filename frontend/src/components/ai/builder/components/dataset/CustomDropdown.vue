<script setup lang="ts">
import CustomSelect from '../../../../form/CustomSelect.vue';

defineProps({
  data: Object
});
</script>
<template>
  <custom-select
    @pointerdown.stop=""
    :values="data?.values"
    display-type="small"
    :is-searchable="false"
    :label="data?.label"
    empty-string="(Empty)"
    :initial-data="data?.values[0]"
  ></custom-select>
</template>
