<template>
  <div
    class="fixed z-10 bg-gray-600/70 filter backdrop-blur-md top-1/2 transform -translate-y-1/2 text-white rounded-r-lg overflow-hidden"
    v-if="!userSolutionLocked && !viewerLoadingState.solveResultLoading"
  >
    <tool-item
      @click="changeTool(tool, $event)"
      :class="currentTool === tool ? 'bg-gray-300' : ''"
      v-for="tool in tools"
      :key="tool"
      :comp="TOOL_COMPONENTS[tool]"
      :hint="TOOL_HINTS[tool]"
    ></tool-item>
  </div>
</template>
<script lang="ts">
import { defineComponent, onMounted, PropType, ref, watch } from 'vue';

import { Tool, TOOL_COMPONENTS, TOOL_HINTS } from '../../model/viewer/tools';
import { userSolutionLocked, viewerLoadingState } from './core/viewerState';

export default defineComponent({
  props: {
    tools: Array as PropType<Tool[]>,
    setMoving: Boolean,
    changeToolTo: Number as PropType<Tool>
  },

  emits: ['toolUpdate'],

  setup(props, { emit }) {
    const currentTool = ref<Tool>();

    const changeTool = (tool: Tool, event: any) => {
      currentTool.value = tool;
      emit('toolUpdate', { tool, event });
    };

    watch(
      () => props.changeToolTo,
      () => {
        if (props.changeToolTo !== undefined) {
          changeTool(props.changeToolTo, null);
        }
      }
    );

    watch(
      () => props.setMoving,
      (newVal, _) => {
        if (newVal) {
          changeTool(Tool.MOVE, null);
        }
      }
    );

    onMounted(() => {
      changeTool(Tool.MOVE, null);
    });
    return {
      TOOL_COMPONENTS,
      TOOL_HINTS,
      currentTool,
      changeTool,
      userSolutionLocked,
      viewerLoadingState
    };
  }
});
</script>
