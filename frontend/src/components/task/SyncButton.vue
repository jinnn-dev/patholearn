<template>
  <div class="flex justify-center items-center p-2 bg-gray-700 rounded-r-md cursor-pointer" @click="createOrJoinRoom">
    <Icon name="users-three" class="text-green-500"></Icon>
    {{ taskSocketState.joinedUsers.length }}
  </div>
</template>

<script lang="ts">
import { TaskSocket, taskSocketState } from '../../services/sockets/task.socket';
import { defineComponent, onMounted, PropType } from 'vue-demi';
import { BaseTask } from '../../model/baseTask';
import { Task } from '../../model/task';

export default defineComponent({
  props: {
    baseTask: {
      type: Object as PropType<BaseTask>,
      required: true
    },
    task: {
      type: Object as PropType<Task>
    }
  },

  emits: ['joined'],

  setup(props, { emit }) {
    const connect = () => {
      emit('joined');
    };

    const createOrJoinRoom = () => {
      if (props.baseTask && props.task && !taskSocketState.isConnected) {
        TaskSocket.getInstance().connect(connect);
      }
    };

    return { createOrJoinRoom, taskSocketState };
  }
});
</script>
