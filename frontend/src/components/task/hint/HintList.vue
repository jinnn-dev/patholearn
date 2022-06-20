<script lang='ts' setup>
import { computed, PropType, ref } from 'vue';
import { Task } from '../../../model/task';
import { getTaskHints, store } from '../../../utils/hint.store';
import { TaskHint } from '../../../model/taskHint';

const props = defineProps({
  task: {
    type: Object as PropType<Task>,
    required: true
  },
  isUpdate: {
    type: Boolean,
    default: false
  }
});

getTaskHints(props.task.id);
const creatorOpen = ref(false);
const selectedHint = ref();

const sortedHints = computed(() => {
  return store.hints.sort((a: any, b: any) => {
    return a.needed_mistakes - b.needed_mistakes;
  });
});

function selectHint(hint: TaskHint) {
  selectedHint.value = hint;
  creatorOpen.value = true;
}

function closeCreator() {
  selectedHint.value = null;
  creatorOpen.value = false;
}

function updateList(updatedHint: TaskHint) {
  store.hints.forEach((hint) => {
    if (hint.id == updatedHint.id) {
      hint.content = updatedHint.content;
      hint.hint_type = updatedHint.hint_type;
      hint.images = updatedHint.images;
      hint.needed_mistakes = updatedHint.needed_mistakes;
      hint.order_position = updatedHint.order_position;
    }
  });
}

function deleteHint(hintId: number) {
  store.hints = store.hints.filter((hint) => hint.id != hintId);
}

function addHint(hint: TaskHint) {
  store.hints.push(hint);
}
</script>
<template>
  <div class='flex justify-between items-center mb-2' v-if='!creatorOpen'>
    <div v-if='task && task.hints.length === 0' class='text-xl'>Keine Tipps vorhanden</div>

    <primary-button type='button' name='Tipp' class='w-24' bgColor='bg-gray-500' @click.native='creatorOpen = true'
    >
      <Icon name='plus' class='mr-1'
      />
    </primary-button>
  </div>
  <HintCreator
    v-if='creatorOpen'
    :taskId='task.id'
    :hint='selectedHint'
    @closeMe='closeCreator'
    :key='creatorOpen'
    @updated='updateList'
    @created='addHint'
  />

  <div class='overflow-y-auto max-h-[500px]' v-if='task && !creatorOpen && task?.hints.length > 0'>
    <Hint
      v-for='(hint, index) in sortedHints'
      :key='index'
      :hint='hint'
      @edit='selectHint(hint)'
      @delete='deleteHint'
    ></Hint>
  </div>
</template>
