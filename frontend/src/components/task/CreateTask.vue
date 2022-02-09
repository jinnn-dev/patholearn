<template>
  <div>
    <h1 class="text-2xl text-center">
      Füge eine neue Aufgabe der
      {{ layerIndex }}. Ebene hinzu
    </h1>
    <form @submit.prevent="onSubmit" class="w-full">
      <input-field
        v-model="taskCreationForm.task_question"
        label="Fragestellung"
        placeholder="Markiere..."
        type="text"
        :required="true"
      >
      </input-field>
      <Accordion>
        <AccordionItem title="Aufgabeneinstellungen" :first="true">
          <div>Wähle einen Aufgabentyp:</div>

          <div class="flex justify-evenly gap-4 mt-4">
            <div
              class="transition flex justify-center items-center w-48 h-20 bg-gray-400 hover:bg-gray-300 hover:ring-2 ring-highlight-900 cursor-pointer rounded-lg"
              :class="selectedTaskType === 0 && 'bg-gray-500 ring-2 ring-highlight-900'"
              @click="selectedTaskType = 0"
            >
              <div class="flex flex-col justify-center items-center text-center">
                <Icon name="polygon" size="46" />
                Annotationen zeichen
              </div>
            </div>
            <div
              class="transition flex justify-center items-center w-48 h-20 bg-gray-400 hover:bg-gray-300 hover:ring-2 ring-highlight-900 cursor-pointer rounded-lg"
              :class="selectedTaskType === 1 && 'bg-gray-500 ring-2 ring-highlight-900'"
              @click="
                selectedTaskType = 1;
                taskCreationForm.task_type = 2;
              "
            >
              <div class="flex flex-col justify-center items-center text-center">
                <Icon name="squares-four" size="46" />
                Bilder auswählen
              </div>
            </div>
          </div>

          <div class="my-4" v-if="selectedTaskType === 0">
            <div>
              <div>Wähle eine Annotationseigenschaft:</div>
              <div class="flex flex-col w-full justify-evenly gap-2 my-4">
                <div
                  class="transition flex justify-center items-center bg-gray-400 hover:bg-gray-300 hover:ring-2 ring-highlight-900 cursor-pointer rounded-lg p-2"
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
                  class="transition flex justify-center items-center w-32 h-20 bg-gray-400 hover:bg-gray-300 hover:ring-2 ring-highlight-900 cursor-pointer rounded-lg"
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
                  <div class="ml-2">
                    Polygon: Die Annotationen können aus Polygonen, Rechtecken und Ellipsen bestehen
                  </div>
                </div>
              </div>
            </div>
            <div class="my-8">
              <div>Welches Vorwissen ist bei den Lernenden vorhanden:</div>
              <div class="my-2 mb-4 break-words text-sm text-gray-200 py-2">
                Die Vorwissensstufe bestimmt den Schwierigkeitsgrad der Aufgabe. Mit steigender Stufe wird das Feedback
                weniger unterstützend. Außerdem wird die Aufgabenüberprüfung strenger.
              </div>
              <div class="flex w-full justify-evenly gap-2 my-2">
                <div
                  class="transition flex justify-center items-center bg-gray-400 hover:bg-gray-300 hover:ring-2 ring-highlight-900 cursor-pointer rounded-lg p-2"
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

          <div v-if="selectedTaskType === 1">
            <div class="my-2 flex gap-2 flex-col">
              <div class="mt-2">Wähle eine Reihe von Bilder:</div>
              <div>
                <div
                  class="h-20 w-20 bg-gray-500 rounded-lg inline-block mx-2 my-2"
                  v-for="(image, index) in tempPreviewImages"
                  :key="image"
                >
                  <UploadPreviewImage :imgSrc="image" @click="deleteImage(index)" />
                </div>
                <div
                  class="h-20 w-20 mx-2 my-2 bg-highlight-900 rounded-lg flex items-center justify-center cursor-pointer hover:bg-highlight-800 transition"
                  @click="fileRef?.click()"
                >
                  <Icon name="plus" width="30" height="30" stroke-width="25" />
                </div>
              </div>
            </div>
            <div v-if="noImageSelectedError" class="text-red-400 font-semibold">
              Bitte wähle mindestens ein Bild aus
            </div>
            <input type="file" ref="fileRef" v-show="false" @change="onFileChange($event)" multiple="multiple" />
          </div>
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
        <save-button name="Speichern" type="submit" class="w-36" :loading="taskCreationLoading"></save-button>
      </div>
    </form>
  </div>
</template>
<script lang="ts">
import Slider from '@vueform/slider';
import { useVuelidate } from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { defineComponent, reactive, ref } from 'vue';
import { SLIDE_IMAGE_URL } from '../../config';
import { Task, TaskCreate, TaskType } from '../../model/task';
import { TaskImageService } from '../../services/task-image.service';
import { TaskService } from '../../services/task.service';
import { knowledgeLevel, taskTypes } from './task-config';

export default defineComponent({
  components: { Slider },
  emits: ['close', 'taskCreated'],
  props: {
    layerIndex: {
      type: Number,
      required: true
    },
    baseTaskId: {
      type: Number,
      required: true
    }
  },
  setup(props, { emit }) {
    const fileRef = ref<HTMLInputElement>();
    const tempPreviewImages = ref<string[]>([]);
    const tempImages = ref<File[]>([]);
    const noImageSelectedError = ref(false);

    const typeSelection = [
      {
        index: 0,
        type: 'Punkt',
        icon: 'push-pin'
      },
      {
        index: 1,
        type: 'Linie',
        icon: 'activity'
      },
      {
        index: 2,
        type: 'Polygon',
        icon: 'triangle'
      }
    ];

    const taskCreationLoading = ref<Boolean>(false);

    const initialState = {
      layer: null,
      task_question: null,
      task_type: 0,
      annotation_type: 0,
      knowledge_level: 0,
      min_correct: 1
    };

    const taskCreationForm = reactive<{
      layer: number | null;
      task_question: string | null;
      task_type: number;
      annotation_type: number;
      knowledge_level: number;
      min_correct: number;
    }>({
      ...initialState
    });

    const notNull = (value: any) => value != null;

    const rules = {
      task_type: { required, notNull }
    };

    const validator = useVuelidate(rules, taskCreationForm);

    const expandTaskSettings = ref(true);

    const createdTask = ref<Task>();

    const selectedTaskType = ref<number>(0);

    const onSubmit = async () => {
      if (!validator.value.$invalid) {
        taskCreationLoading.value = true;

        if (taskCreationForm.task_type === TaskType.IMAGE_SELECT) {
          if (!tempImages.value.length) {
            taskCreationLoading.value = false;
            noImageSelectedError.value = true;
          } else {
            noImageSelectedError.value = false;

            const imageNames = [];
            for await (const img of tempImages.value) {
              const name = await uploadImage(img);
              imageNames.push(name.task_image_id);
            }

            const createTask: TaskCreate = {
              layer: props.layerIndex,
              task_question: taskCreationForm.task_question!,
              base_task_id: props.baseTaskId as number,
              task_type: taskCreationForm.task_type!,
              task_data: imageNames,
              annotation_type: 0,
              knowledge_level: 1,
              min_correct: imageNames.length,
              hints: []
            };

            const task = await TaskService.createTask(createTask);
            emit('taskCreated', task);
            taskCreationLoading.value = false;
            createdTask.value = task;
            emit('close');

            tempImages.value = [];
            tempPreviewImages.value = [];
          }
        } else {
          const createTask: TaskCreate = {
            layer: props.layerIndex,
            task_question: taskCreationForm.task_question!,
            base_task_id: props.baseTaskId as number,
            task_type: taskCreationForm.task_type!,
            annotation_type: taskCreationForm.annotation_type,
            knowledge_level: taskCreationForm.knowledge_level,
            min_correct: taskCreationForm.min_correct,
            annotation_groups: [],
            hints: []
          };
          TaskService.createTask(createTask).then((res: Task) => {
            emit('taskCreated', res);
            taskCreationLoading.value = false;
            createdTask.value = res;
            emit('close');
            // Object.assign(taskCreationForm, initialState);
          });
        }
      }
    };

    function onFileChange(e: any) {
      const files = e.target.files || e.dataTransfer.files;
      noImageSelectedError.value = false;

      if (!files.length) return;
      for (const file of files) {
        tempPreviewImages.value.push(URL.createObjectURL(file));
        tempImages.value.push(file);
      }
    }

    function deleteImage(imageIndex: number) {
      tempPreviewImages.value.splice(imageIndex, 1);
      tempImages.value.splice(imageIndex, 1);
    }

    const uploadImage = async (image: File) => {
      const formData = new FormData();
      formData.append('images', image);
      formData.append('names', image.name);
      return await TaskImageService.uploadTaskImage(formData);
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
      selectedTaskType,
      tempImages,
      tempPreviewImages,
      fileRef,
      onFileChange,
      deleteImage,
      SLIDE_IMAGE_URL,
      noImageSelectedError
    };
  }
});
</script>
<style></style>
