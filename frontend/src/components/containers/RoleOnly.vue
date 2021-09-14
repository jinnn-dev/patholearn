<template>
  <div v-if="isSuperuser">
    <slot></slot>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { appState } from '../../utils/app.state';

export default defineComponent({
  setup() {
    const isSuperuser = appState.user?.is_superuser;

    return { isSuperuser };
  }
});
</script>

<style></style>
