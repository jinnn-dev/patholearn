<script setup lang="ts">
import { PresenceChannel } from 'pusher-js';
import { PropType, computed, onMounted, ref } from 'vue';
import { nanoid } from 'nanoid';
import InputField from '../form/InputField.vue';
import InputArea from '../form/InputArea.vue';
import CustomSlider from '../form/CustomSlider.vue';
import { debounceRef } from '../../utils/debounceRef';
import { AiService } from '../../services/ai.service';
import { useService } from '../../composables/useService';

type InputType = 'input' | 'area';

const { run: update } = useService(AiService.updateBuilderState);
const { run: lock } = useService(AiService.lock);
const { run: unlock } = useService(AiService.unlock);

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
  },
  id: {
    type: String,
    required: true
  },
  type: {
    type: String as PropType<InputType>,
    default: 'input'
  },
  initialValue: String,
  initialLockedBy: String,
  label: {
    type: String,
    required: true
  },
  tip: String
});

const modelValue = debounceRef(props.initialValue || '', 50);

const lockedBy = ref(props.initialLockedBy);

const lockedUser = computed(() => props.members?.find((member) => member.id === lockedBy.value));

const lockInput = async () => {
  await lock(props.id, props.me.id);

  props.channel.trigger(`client-lock-${props.id}`, {
    id: props.id,
    userId: props.me.id
  });
};

const input = (value: string) => {
  if (lockedBy.value !== null && lockedBy.value !== props.me.id) {
    return;
  }

  props.channel.trigger(`client-input-${props.id}`, {
    id: props.id,
    value: value,
    from: props.me.id
  });
};

const unlockInput = async () => {
  await Promise.all([update(props.id, modelValue.value), unlock(props.id)]);
  props.channel.trigger(`client-unlock-${props.id}`, {
    id: props.id,
    userId: props.me.id
  });
};

onMounted(() => {
  props.channel.bind(`client-lock-${props.id}`, (data: any) => {
    lockedBy.value = data.userId;
  });

  props.channel.bind(`client-input-${props.id}`, (value: any) => {
    if (value.from === props.me.id) {
      return;
    }

    modelValue.value = value.value;
  });
  props.channel.bind(`client-unlock-${props.id}`, (value: any) => {
    lockedBy.value = undefined;
  });
});
</script>
<template>
  <input-field
    v-if="type === 'input'"
    v-model="modelValue"
    :id="id"
    @focus="lockInput"
    @blur="unlockInput"
    @update:model-value="input"
    :locked-by="lockedUser?.info.first_name"
    :locked-color="lockedUser?.info.color"
    :label="label"
    :tip="tip"
  ></input-field>
  <input-area
    v-else
    v-model="modelValue"
    :id="id"
    @focus="lockInput"
    @blur="unlockInput"
    @update:model-value="input"
    :locked-by="lockedUser?.info.first_name"
    :locked-color="lockedUser?.info.color"
    :label="label"
    :tip="tip"
  ></input-area>
</template>
