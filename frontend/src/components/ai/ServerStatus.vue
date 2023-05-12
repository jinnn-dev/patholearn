<script setup lang="ts">
import { useService } from '../../composables/useService';
import Icon from '../../components/general/Icon.vue';
import { AiService } from '../../services/ai.service';
import Spinner from '../../components/general/Spinner.vue';
import { onMounted } from 'vue';
const { result: aiResult, loading: aiLoading } = useService(AiService.ping, true);
const { result: clearmlResult, loading: clearmlLoading } = useService(AiService.pingClearml, true);

const ICON_SIZE = 48;
const CONNECTION_ICON_SIZE = 32;
</script>
<template>
  <div class="flex justify-center items-center">
    <div class="p-2 bg-gray-500 rounded-xl"><icon name="desktop-tower" stroke-width="0" :size="ICON_SIZE"></icon></div>
    <div class="w-full flex items-center">
      <div
        class="w-full h-2"
        :class="aiLoading ? 'bg-gray-500' : aiResult === 'Ok' ? 'bg-green-800' : 'bg-red-700'"
      ></div>
      <div class="flex justify-center bg-gray-700 p-2 rounded-xl">
        <spinner v-if="aiLoading"></spinner>
        <div v-else>
          <icon v-if="aiResult == 'Ok'" name="plugs-connected" stroke-width="0" :size="CONNECTION_ICON_SIZE"></icon>
          <icon v-else name="plugs" stroke-width="0" :size="CONNECTION_ICON_SIZE"></icon>
        </div>
      </div>
      <div
        class="w-full h-2"
        :class="aiLoading ? 'bg-gray-500' : aiResult === 'Ok' ? 'bg-green-800' : 'bg-red-700'"
      ></div>
    </div>
    <div class="p-2 bg-gray-500 rounded-xl"><icon name="hard-drives" stroke-width="0" :size="ICON_SIZE"></icon></div>
    <div class="w-full flex items-center">
      <div
        class="w-full h-2"
        :class="clearmlLoading ? 'bg-gray-500' : clearmlResult === 'Ok' ? 'bg-green-800' : 'bg-red-700'"
      ></div>
      <div class="flex justify-center bg-gray-700 p-2 rounded-xl">
        <spinner v-if="clearmlLoading"></spinner>
        <div v-else>
          <icon
            v-if="clearmlResult == 'Ok'"
            name="plugs-connected"
            stroke-width="0"
            :size="CONNECTION_ICON_SIZE"
          ></icon>
          <icon v-else name="plugs" stroke-width="0" :size="CONNECTION_ICON_SIZE"></icon>
        </div>
      </div>
      <div
        class="w-full h-2"
        :class="clearmlLoading ? 'bg-gray-500' : clearmlResult === 'Ok' ? 'bg-green-800' : 'bg-red-700'"
      ></div>
    </div>
    <div class="p-2 bg-gray-500 rounded-xl"><icon name="computer-tower" stroke-width="0" :size="ICON_SIZE"></icon></div>
  </div>
</template>
