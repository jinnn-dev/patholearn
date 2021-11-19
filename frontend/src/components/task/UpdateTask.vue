<template>
  <div>
    <h1 class="text-2xl text-center">Füge eine neue Aufgabe der {{ taskUpdateForm.layer }}. Ebene hinzu</h1>
    <form @submit.prevent="updateTask" class="w-full">
      <input-field
        v-model="taskUpdateForm.task_question"
        label="Fragestellung"
        placeholder="Markiere..."
        type="text"
        :required="true"
      >
      </input-field>

      <Accordion>
        <AccordionItem
          title="Aufgabeneinstellungen"
          :first="true"
          v-if="taskUpdateForm.task_type !== TaskType.IMAGE_SELECT"
        >
          <div class="my-8" v-if="taskUpdateForm.task_type === 0">
            <div>Wie viele Annotationen müssen die Lernenden mindestens richtig treffen:</div>
            <div class="pb-4 pt-11">
              <Slider v-model="taskUpdateForm.min_correct" :min="0" :max="50" :tooltips="true"></Slider>
            </div>
          </div>

          <div class="my-8">
            <div>Welches Vorwissen ist bei den Lernenden vorhanden:</div>
            <div class="my-2 break-words text-sm text-gray-200 py-2">
              Die Vorwissensstufe bestimmt den Schwierigkeitsgrad der Aufgabe. Mit steigender Stufe wird das Feedback
              weniger unterstützend. Außerdem wird die Aufgabenüberprüfung strenger.
            </div>
            <div class="flex w-full justify-evenly gap-2 my-2">
              <div
                class="
                  transition
                  flex
                  justify-center
                  items-center
                  bg-gray-400
                  hover:bg-gray-300 hover:ring-2
                  ring-highlight-900
                  cursor-pointer
                  rounded-lg
                  p-2
                "
                v-for="level in knowledgeLevel"
                :key="level.index"
                :class="taskUpdateForm.knowledge_level === level.index && 'bg-gray-500 ring-2 ring-highlight-900'"
                @click="taskUpdateForm.knowledge_level = level.index"
              >
                <div class="flex flex-col gap-3 justify-center items-center text-center">
                  <div>{{ level.name }}</div>
                </div>
              </div>
            </div>
          </div>

          <div class="my-8">
            <div>Soll die Aufgabe von Nutzern lösbar sein?</div>
            <toggle-button
              class="my-2"
              :enabled="taskUpdateForm.can_be_solved"
              @changed="changeCanBeSolved"
            ></toggle-button>
          </div>
        </AccordionItem>
        <AccordionItem title="Tipps (optional)">
          <HintList :task="task" :isUpdate="true" />
        </AccordionItem>
      </Accordion>

      <div class="flex justify-end w-full">
        <primary-button
          @click.prevent="$emit('close')"
          class="mr-2 w-32"
          name="Abbrechen"
          bgColor="bg-gray-500"
          bgHoverColor="bg-gray-700"
          fontWeight="font-normal"
        ></primary-button>
        <save-button name="Speichern" type="submit" class="w-36" :loading="taskUpdateLoading"></save-button>
      </div>
    </form>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref, reactive, PropType, watch } from 'vue';
import Slider from '@vueform/slider';

import { knowledgeLevel, taskTypes } from './task-config';
import { TaskService } from '../../services/task.service';
import { Task, TaskType } from '../../model/task';

export default defineComponent({
  components: { Slider },
  props: {
    task: {
      type: Object as PropType<Task>
    }
  },
  emits: ['close', 'taskUpdated'],
  setup(props, { emit }) {
    const taskUpdateLoading = ref<Boolean>(false);

    const taskUpdateForm = reactive<{
      layer: number;
      task_question: string | null;
      knowledge_level: number;
      min_correct: number;
      task_id: number;
      task_type: number;
      can_be_solved: boolean;
    }>({
      layer: 0,
      task_question: '',
      knowledge_level: 0,
      min_correct: 0,
      task_id: 0,
      task_type: 0,
      can_be_solved: true
    });

    watch(
      () => props.task,
      () => {
        taskUpdateForm.layer = props.task!.layer;
        taskUpdateForm.task_question = props.task!.task_question;
        taskUpdateForm.knowledge_level = props.task!.knowledge_level;
        taskUpdateForm.min_correct = props.task!.min_correct;
        taskUpdateForm.task_id = props.task!.id;
        taskUpdateForm.task_type = props.task!.task_type;
        taskUpdateForm.can_be_solved = props.task!.can_be_solved;
      }
    );

    const updateTask = async () => {
      taskUpdateLoading.value = true;

      const res = await TaskService.updateTask({
        task_id: taskUpdateForm.task_id,
        task_question: taskUpdateForm.task_question!,
        min_correct: taskUpdateForm.min_correct,
        knowledge_level: taskUpdateForm.knowledge_level,
        can_be_solved: taskUpdateForm.can_be_solved
      });
      taskUpdateLoading.value = false;

      emit('close');
      emit('taskUpdated', res);
    };

    const changeCanBeSolved = (value: boolean) => {
      taskUpdateForm.can_be_solved = value;
    };
    return { taskUpdateForm, updateTask, taskUpdateLoading, knowledgeLevel, taskTypes, TaskType, changeCanBeSolved };
  }
});
</script>
<style></style>
