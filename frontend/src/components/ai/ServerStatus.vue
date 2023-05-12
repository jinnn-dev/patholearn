<script setup lang="ts">
import { SlideService } from '../../services/slide.service';
import { useService } from '../../composables/useService';
import { AiService } from '../../services/ai.service';
import { wsIsConnected, websocketLoading } from '../../utils/app.state';
import StatusItem from './StatusItem.vue';
import { AuthService } from '../../services/auth.service';
const { result: aiResult, loading: aiLoading } = useService(AiService.ping, true);
const { result: clearmlResult, loading: clearmlLoading } = useService(AiService.pingClearml, true);
const { result: slideResult, loading: slideLoading } = useService(SlideService.ping, true);
const { result: authResult, loading: authLoading } = useService(AuthService.ping, true);
</script>
<template>
  <div
    class="flex flex-col w-full justify-center items-center rounded-lg border-[1px] bg-gray-700 border-gray-500 divide-y-[1px] divide-gray-500"
  >
    <status-item name="AI API" :status="aiResult === 'Ok' ? true : false" :loading="aiLoading"></status-item>
    <status-item
      name="AI Worker API"
      :status="clearmlResult === 'Ok' ? true : false"
      :loading="aiLoading"
    ></status-item>
    <status-item name="Websocket Server" :status="wsIsConnected" :loading="websocketLoading"> </status-item>
    <status-item name="WSI API" :status="slideResult?.Hello === 'World' ? true : false" :loading="slideLoading">
    </status-item>
    <status-item name="Auth API" :status="authResult" :loading="authLoading"> </status-item>
  </div>
</template>
