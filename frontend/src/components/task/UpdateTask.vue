<template>
  <div>
    <h1 class='text-2xl text-center'>
      Füge eine neue Aufgabe der
      {{ taskUpdateForm.layer }}. Ebene hinzu
    </h1>
    <form class='w-full' @submit.prevent='updateTask'>
      <input-field
        v-model='taskUpdateForm.task_question'
        :required='true'
        label='Fragestellung'
        placeholder='Markiere...'
        type='text'
      >
      </input-field>

      <Accordion>
        <AccordionItem
          v-if='taskUpdateForm.task_type !== TaskType.IMAGE_SELECT'
          :first='true'
          title='Aufgabeneinstellungen'
        >
          <div v-if='taskUpdateForm.task_type === 0' class='my-8'>
            <div>Wie viele Annotationen müssen die Lernenden mindestens richtig treffen:</div>
            <CustomSlider
              :initialPosition='taskUpdateForm.min_correct'
              :max='50'
              :min='0'
              :tooltips='true'
              class='pb-4 pt-11'
              @isReleased='updateMinCorrect'
            >
            </CustomSlider>
          </div>

          <div class='my-8'>
            <div>Welches Vorwissen ist bei den Lernenden vorhanden:</div>
            <div class='my-2 break-words text-sm text-gray-200 py-2'>
              Die Vorwissensstufe bestimmt den Schwierigkeitsgrad der Aufgabe. Mit steigender Stufe wird das Feedback
              weniger unterstützend. Außerdem wird die Aufgabenüberprüfung strenger.
            </div>
            <div class='flex w-full justify-evenly gap-2 my-2'>
              <div
                v-for='level in knowledgeLevel'
                :key='level.index'
                :class="taskUpdateForm.knowledge_level === level.index && 'bg-gray-500 ring-2 ring-highlight-900'"
                class='transition flex justify-center items-center bg-gray-400 hover:bg-gray-300 hover:ring-2 ring-highlight-900 cursor-pointer rounded-lg p-2'
                @click='taskUpdateForm.knowledge_level = level.index'
              >
                <div class='flex flex-col gap-3 justify-center items-center text-center'>
                  <div>
                    {{ level.name }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class='my-8'>
            <div>Soll die Aufgabe von Nutzern lösbar sein?</div>
            <toggle-button
              :enabled='taskUpdateForm.can_be_solved'
              class='my-2'
              @changed='changeCanBeSolved'
            ></toggle-button>
          </div>
        </AccordionItem>
        <!-- <AccordionItem title="Tipps (optional)">
          <HintList :task="task" :isUpdate="true" />
        </AccordionItem> -->
      </Accordion>

      <confirm-buttons class='mt-4' :loading='taskUpdateLoading' reject-text='Abbrechen' @reject='$emit("close")'
                       confirm-text='Speichern'></confirm-buttons>
      
    </form>
  </div>
</template>
<script lang='ts'>
import { defineComponent, PropType, reactive, ref, watch } from 'vue';
import { Task } from '../../model/task/task';
import { TaskService } from '../../services/task.service';
import { knowledgeLevel, taskTypes } from './task-config';
import InputField from '../form/InputField.vue';
import Accordion from '../containers/Accordion.vue';
import AccordionItem from '../containers/AccordionItem.vue';
import CustomSlider from '../form/CustomSlider.vue';
import ToggleButton from '../form/ToggleButton.vue';
import PrimaryButton from '../general/PrimaryButton.vue';
import SaveButton from '../general/SaveButton.vue';
import { TaskType } from '../../core/types/taskType';
import ConfirmButtons from '../general/ConfirmButtons.vue';

export default defineComponent({
  components: {
    ConfirmButtons,
    SaveButton,
    PrimaryButton,
    ToggleButton,
    CustomSlider,
    AccordionItem,
    Accordion,
    InputField
  },
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

    const updateMinCorrect = (value: number) => {
      taskUpdateForm.min_correct = value;
    };

    return {
      taskUpdateForm,
      taskUpdateLoading,
      knowledgeLevel,
      taskTypes,
      TaskType,
      changeCanBeSolved,
      updateMinCorrect,
      updateTask
    };
  }
});
</script>
<style></style>
