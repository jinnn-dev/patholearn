<template>
  <div>
    <input-field
      label="Anzahl benötigter Fehler"
      v-model="neededMistakes"
      type="number"
      tip="Wenn eine lernende Person die hinterlegte Fehleranzahl erreicht hat, wird ihm dieser Tipp angezeigt"
    ></input-field>
    <input-area
      v-model="hintText"
      class="h-40"
      label="Inhalt des Tipps"
      tip="Hier muss der Inhalt des Tipps hinterlegt werden den die lernenden Person angezeigt wird "
    />
    <div class="my-2 flex gap-2">
      <div class="h-20 w-20 bg-gray-500 rounded-lg" v-viewer></div>
      <div class="h-20 w-20 bg-gray-500 rounded-lg"></div>
      <div
        class="
          h-20
          w-20
          bg-green-600
          rounded-lg
          flex
          items-center
          justify-center
          cursor-pointer
          hover:bg-green-500
          transition
        "
      >
        <Icon name="plus" width="30" height="30" stroke-width="25" />
      </div>
    </div>

    <div class="flex justify-end">
      <save-button type="button" name="Tipp speichern" class="w-48" @click="createHint"></save-button>
    </div>
  </div>
</template>
<script lang="ts">
import { TaskService } from '../../../services/task.service';
import { defineComponent, PropType, ref } from 'vue';
import { Task } from '../../../model/task';
import { HintType } from '../../../model/taskHint';
export default defineComponent({
  props: {
    task: Object as PropType<Task>,
    selectedHint: Number
  },
  setup(props) {
    const hintText = ref('');
    const neededMistakes = ref(0);
    function createHint() {
      TaskService.createHint(props.task!.id, {
        task_id: props.task!.id,
        content: hintText.value,
        needed_mistakes: neededMistakes.value,
        hint_type: HintType.IMAGE,
        images: []
      });
    }
    return { createHint, hintText, neededMistakes };
  }
});
</script>
<style></style>
