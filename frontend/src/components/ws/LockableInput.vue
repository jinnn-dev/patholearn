<script setup lang="ts">
import { PresenceChannel } from 'pusher-js';
import { PropType, computed, onMounted, ref } from 'vue';
import { nanoid } from 'nanoid';
import InputField from '../form/InputField.vue';
import InputArea from '../form/InputArea.vue';
import CustomSlider from '../form/CustomSlider.vue';
import { debounceRef } from '../../utils/debounceRef';

const id = '123456';

const modelValue = debounceRef('', 50);

const props = defineProps({
  channel: {
    type: Object as PropType<PresenceChannel>,
    required: true
  },
  members: {
    type: Object as PropType<any[]>
  },
  me: {
    type: Object as PropType<any>,
    required: true
  },
  rateLimit: {
    type: Number,
    default: 50
  }
});

const lockedBy = ref();

const lockedUser = computed(() => props.members?.find((member) => member.id === lockedBy.value));

const lockInput = () => {
  console.log('Lock');

  props.channel.trigger(`client-lock-${id}`, {
    id: id,
    userId: props.me.id
  });
};

const input = (value: string) => {
  props.channel.trigger(`client-input-${id}`, {
    id: id,
    value: value
  });
};

const unlockInput = () => {
  console.log('UnLOCK');

  props.channel.trigger(`client-unlock-${id}`, {
    id: id,
    userId: props.me.id
  });
};

onMounted(() => {
  props.channel.bind(`client-lock-${id}`, (data: any) => {
    lockedBy.value = data.userId;
  });

  props.channel.bind(`client-input-${id}`, (value: any) => {
    if (value.userId === props.me.id) {
      return;
    }

    modelValue.value = value.value;
  });
  props.channel.bind(`client-unlock-${id}`, (value: any) => {
    lockedBy.value = undefined;
  });
});
</script>
<template>
  <input-area
    v-model="modelValue"
    :id="id"
    @focus="lockInput"
    @blur="unlockInput"
    @update:model-value="input"
    :locked-by="lockedUser?.info.first_name"
    :locked-color="lockedUser?.info.color"
  ></input-area>
</template>
