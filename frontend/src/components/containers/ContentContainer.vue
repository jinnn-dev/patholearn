<script lang="ts" setup>
import Icon from '../../components/general/Icon.vue';

defineProps({
  loading: {
    type: Boolean,
    default: false
  },
  margin: {
    type: String,
    default: '12'
  },
  backRoute: String,
  backText: {
    type: String,
    default: 'Zurück'
  }
});
</script>
<template>
  <div>
    <div class="relative flex flex-col items-start gap-4 p-8">
      <div v-if="loading" class="w-full flex justify-center items-center">
        <div class="animate-skeleton w-96 h-14 bg-gray-700 rounded-lg"></div>
      </div>

      <div v-else class="w-full text-center text-5xl"><slot name="header"></slot></div>
      <div class="w-full" v-if="loading">
        <div class="animate-skeleton w-36 h-5 4 bg-gray-700 rounded-lg"></div>
      </div>
      <div v-if="!loading && backRoute" class="text-lg">
        <router-link :to="backRoute" tag="span">
          <div class="flex gap-2 items-center hover:text-highlight-800">
            <icon name="arrow-left"></icon>
            <div>{{ backText }}</div>
          </div>
        </router-link>
      </div>
    </div>

    <div class="flex justify-center" :class="margin">
      <div class="w-11/12 mb-8">
        <slot name="content"></slot>
      </div>
    </div>
  </div>
</template>
