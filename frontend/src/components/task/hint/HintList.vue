<template>
  <div class="flex justify-between items-center mb-2" v-if="!creatorOpen">
    <div v-if="task && task.hints.length === 0" class="text-xl">Keine Tipps vorhanden</div>

    <primary-button type="button" name="Tipp" class="w-24" bgColor="bg-gray-500" @click.native="creatorOpen = true"
      ><Icon name="plus" class="mr-1"
    /></primary-button>
  </div>
  <HintCreator v-if="creatorOpen" :taskId="task.id" :hint="selectedHint" />

  <div class="overflow-y-auto max-h-[500px]" v-if="task && !creatorOpen && task?.hints.length > 0">
    <Hint v-for="(hint, index) in task?.hints" :key="index" :hint="hint" @edit="selectHint(hint)"></Hint>
  </div>
</template>
<script lang="ts">
import { Task } from '../../../model/task';
import { defineComponent, PropType, ref } from 'vue';
import { TaskHint } from 'model/taskHint';
export default defineComponent({
  props: {
    task: {
      type: Object as PropType<Task>,
      required: true,
    },
    isUpdate: {
      type: Boolean,
      default: false,
    },
  },
  setup() {
    const creatorOpen = ref(false);
    const selectedHint = ref();

    function selectHint(hint: TaskHint) {
      selectedHint.value = hint;
      creatorOpen.value = true;
    }

    return {
      selectedHint,
      creatorOpen,
      selectHint,
    };
  },
});
</script>
<style></style>
