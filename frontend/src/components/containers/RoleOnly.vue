<script lang='ts' setup>
import { appState } from '../../utils/app.state';

const isSuperuser = appState.user?.is_superuser;

</script>
<template>
  <div v-if='isSuperuser'>
    <slot></slot>
  </div>
</template>
