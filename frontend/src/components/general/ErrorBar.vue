<script lang="ts" setup>
import { errorState } from '../../services/error-handler';
import ErrorNotification from './ErrorNotification.vue';

const removeItem = (index: number) => {
  errorState.value.splice(index, 1);
};
</script>
<template>
  <div class="fixed z-[99] bottom-4 left-1/2 transform -translate-x-1/2">
    <error-notification
      v-for="(error, index) in errorState"
      :key="index"
      :error="error"
      :index="index"
      @expired="removeItem($event)"
    >
    </error-notification>
  </div>
</template>
