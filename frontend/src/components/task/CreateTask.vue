<template>
  <div>
    <h1 class="text-2xl text-center">Füge eine neue Aufgabe der {{ layerIndex }}. Ebene hinzu</h1>
    <form @submit.prevent="onSubmit" class="w-full">
      <input-field v-model="taskCreationForm.task_question" label="Fragestellung" placeholder="Markiere..." type="text" :required="true">
      </input-field>
      <Accordion>
        <AccordionItem title="Aufgabeneinstellungen" :first="true">
          <div class="mb-4">
            <div class="">
              <div>Wähle einen Aufgabentyp:</div>
              <div class="flex flex-col w-full justify-evenly gap-2 my-4">
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
                  v-for="taskType in taskTypes"
                  :key="taskType.index"
                  :class="taskCreationForm.task_type === taskType.index && 'bg-gray-500 ring-2 ring-highlight-900'"
                  @click="taskCreationForm.task_type = taskType.index"
                >
                  <div class="flex flex-col gap-3 justify-center items-center">
                    {{ taskType.description }}
                  </div>
                </div>
              </div>
              <div class="text-gray-200 flex text-sm items-center">
                <Icon name="info" width="20" height="20" />
                <div class="ml-2">Annotationsklassen geben einer Annotation einen bestimmten Typ / Namen.</div>
              </div>
            </div>

            <div class="my-8">
              <div class="mb-4">Welche Art von Annotation soll für die Aufgabe verwendet werden:</div>
              <div class="flex w-full justify-evenly">
                <div
                  class="
                    transition
                    flex
                    justify-center
                    items-center
                    w-32
                    h-20
                    bg-gray-400
                    hover:bg-gray-300 hover:ring-2
                    ring-highlight-900
                    cursor-pointer
                    rounded-lg
                  "
                  v-for="item in typeSelection"
                  :key="item.index"
                  :class="taskCreationForm.annotation_type === item.index && 'bg-gray-500 ring-2 ring-highlight-900'"
                  @click="taskCreationForm.annotation_type = item.index"
                >
                  <div class="flex flex-col gap-2 justify-center items-center">
                    <Icon :name="item.icon" :width="30" :height="30" />
                    {{ item.type }}
                  </div>
                </div>
              </div>
              <div class="h-8 mt-4">
                <div class="text-gray-200 flex text-sm items-center">
                  <Icon name="info" width="20" height="20" />
                  <div class="ml-2">Polygon: Die Annotationen können aus Polygonen, Rechtecken und Ellipsen bestehen</div>
                </div>
              </div>
            </div>
            <div class="my-8">
              <div>Welches Vorwissen ist bei den Lernenden vorhanden:</div>
              <div class="my-2 mb-4 break-words text-sm text-gray-200 py-2">
                Die Vorwissensstufe bestimmt den Schwierigkeitsgrad der Aufgabe. Mit steigender Stufe wird das Feedback weniger unterstützend.
                Außerdem wird die Aufgabenüberprüfung strenger.
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
                  :class="taskCreationForm.knowledge_level === level.index && 'bg-gray-500 ring-2 ring-highlight-900'"
                  @click="taskCreationForm.knowledge_level = level.index"
                >
                  <div class="flex gap-3 justify-center items-center text-center">
                    {{ level.name }}
                  </div>
                </div>
              </div>
            </div>
            <div class="my-4" v-if="taskCreationForm.task_type === 0">
              <div>Wie viele Annotationen müssen die Lernenden mindestens richtig treffen:</div>
              <div class="pb-4 pt-11">
                <Slider v-model="taskCreationForm.min_correct" :min="0" :max="50" :tooltips="true"></Slider>
              </div>
            </div>
          </div>
          <!-- <div class="flex justify-end">
            <save-button name="Speichern" type="submit" class="w-36" :loading="taskCreationLoading"></save-button>
          </div> -->
        </AccordionItem>
        <!-- <AccordionItem title="Tipps (optional)">
          <HintList :task="createdTask" />
        </AccordionItem> -->
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
        <save-button name="Speichern" type="submit" class="w-36" :loading="taskCreationLoading"></save-button>
      </div>
    </form>
  </div>
</template>
<script lang="ts">
import { useVuelidate } from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import Slider from '@vueform/slider';
import { Task, TaskCreate } from 'model/task';
import { TaskService } from '../../services/task.service';
import { defineComponent, reactive, ref } from 'vue';
import { knowledgeLevel, taskTypes } from './task-config';

export default defineComponent({
  components: { Slider },
  emits: ['close', 'taskCreated'],
  props: {
    layerIndex: {
      type: Number,
      required: true,
    },
    baseTaskId: {
      type: Number,
      required: true,
    },
  },
  setup(props, { emit }) {
    const typeSelection = [
      {
        index: 0,
        type: 'Punkt',
        icon: 'push-pin',
      },
      {
        index: 1,
        type: 'Linie',
        icon: 'activity',
      },
      {
        index: 2,
        type: 'Polygon',
        icon: 'triangle',
      },
    ];

    const taskCreationLoading = ref<Boolean>(false);

    const initialState = {
      layer: null,
      task_question: null,
      task_type: 0,
      annotation_type: 0,
      knowledge_level: 0,
      min_correct: 1,
    };

    const taskCreationForm = reactive<{
      layer: number | null;
      task_question: string | null;
      task_type: number;
      annotation_type: number;
      knowledge_level: number;
      min_correct: number;
    }>({
      ...initialState,
    });

    const notNull = (value: any) => value != null;

    const rules = {
      task_type: { required, notNull },
    };

    const validator = useVuelidate(rules, taskCreationForm);

    const expandTaskSettings = ref(true);

    const createdTask = ref<Task>();

    const onSubmit = () => {
      if (!validator.value.$invalid) {
        taskCreationLoading.value = true;
        const createTask: TaskCreate = {
          layer: props.layerIndex,
          task_question: taskCreationForm.task_question!,
          base_task_id: props.baseTaskId as number,
          task_type: taskCreationForm.task_type!,
          annotation_type: taskCreationForm.annotation_type,
          knowledge_level: taskCreationForm.knowledge_level,
          min_correct: taskCreationForm.min_correct,
          annotation_groups: [],
          hints: [],
        };
        TaskService.createTask(createTask).then((res: Task) => {
          emit('taskCreated', res);
          taskCreationLoading.value = false;
          createdTask.value = res;
          emit('close');
          // Object.assign(taskCreationForm, initialState);
        });
      }
    };

    return {
      taskCreationForm,
      taskCreationLoading,
      onSubmit,
      knowledgeLevel,
      taskTypes,
      typeSelection,
      expandTaskSettings,
      createdTask,
    };
  },
});
</script>
<style></style>
