<script lang='ts' setup>
import { useVuelidate } from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { reactive, ref } from 'vue';
import { Task, TaskCreate, TaskType } from '../../model/task';
import { TaskImageService } from '../../services/task-image.service';
import { TaskService } from '../../services/task.service';
import { knowledgeLevel, taskTypes } from './task-config';

const emit = defineEmits(['close', 'taskCreated']);

const props = defineProps({
  layerIndex: {
    type: Number,
    required: true
  },
  baseTaskId: {
    type: Number,
    required: true
  }
});

const noImageSelectedError = ref(false);
const imageSelectImages = ref<{ fileUrl: string; file: File }[]>([]);
const resetImageSelectImage = ref(false);

const typeSelection = [
  {
    index: 0,
    type: 'Punkt',
    icon: 'push-pin'
  },
  {
    index: 1,
    type: 'Linie',
    icon: 'line-segments'
  },
  {
    index: 2,
    type: 'Polygon',
    icon: 'polygon-segments'
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
      if (!imageSelectImages.value.length) {
        taskCreationLoading.value = false;
        noImageSelectedError.value = true;
      } else {
        noImageSelectedError.value = false;

        const taskImages = await uploadImageSelectImages();
        const taskImageIds = taskImages.map((taskImage) => taskImage.task_image_id);

        const createTask: TaskCreate = {
          layer: props.layerIndex,
          task_question: taskCreationForm.task_question!,
          base_task_id: props.baseTaskId as number,
          task_type: taskCreationForm.task_type!,
          task_data: taskImageIds,
          annotation_type: 0,
          knowledge_level: 1,
          min_correct: taskImageIds.length,
          hints: []
        };

        const task = await TaskService.createTask(createTask);
        emit('taskCreated', task);
        taskCreationLoading.value = false;
        createdTask.value = task;
        resetForm();
        emit('close');
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
        resetForm();
        emit('close');
      });
    }
  }
};

const uploadImageSelectImages = async () => {
  const formData = new FormData();
  for (const image of imageSelectImages.value) {
    formData.append('images', image.file);
    formData.append('names', image.file.name);
  }

  const imageIds = TaskImageService.uploadMultipleTaskImages(formData, (value: any) => {
  });

  return imageIds;
};

const setImages = (images: { fileUrl: string; file: File }[]) => {
  imageSelectImages.value = images;
};

const resetForm = () => {
  Object.assign(taskCreationForm, initialState);
  resetImageSelectImage.value = true;
  imageSelectImages.value = [];
};
</script>
<template>
  <div>
    <h1 class='text-2xl text-center'>
      Füge eine neue Aufgabe der
      {{ layerIndex }}. Ebene hinzu
    </h1>
    <form @submit.prevent='onSubmit' class='w-full'>
      <input-field
        v-model='taskCreationForm.task_question'
        label='Fragestellung'
        placeholder='Markiere...'
        type='text'
        :required='true'
      >
      </input-field>
      <Accordion>
        <AccordionItem title='Aufgabeneinstellungen' :first='true'>
          <div>Wähle einen Aufgabentyp:</div>

          <div class='flex justify-evenly gap-4 mt-4'>
            <div
              class='transition flex justify-center items-center w-48 h-20 bg-gray-400 hover:bg-gray-300 hover:ring-2 ring-highlight-900 cursor-pointer rounded-lg'
              :class="selectedTaskType === 0 && 'bg-gray-500 ring-2 ring-highlight-900'"
              @click='selectedTaskType = 0'
            >
              <div class='flex flex-col justify-center items-center text-center'>
                <Icon name='polygon' size='46' />
                Annotationen zeichen
              </div>
            </div>
            <div
              class='transition flex justify-center items-center w-48 h-20 bg-gray-400 hover:bg-gray-300 hover:ring-2 ring-highlight-900 cursor-pointer rounded-lg'
              :class="selectedTaskType === 1 && 'bg-gray-500 ring-2 ring-highlight-900'"
              @click='
                selectedTaskType = 1;
                taskCreationForm.task_type = 2;
              '
            >
              <div class='flex flex-col justify-center items-center text-center'>
                <Icon name='squares-four' size='46' />
                Bilder auswählen
              </div>
            </div>
          </div>

          <div class='my-4' v-if='selectedTaskType === 0'>
            <div>
              <div>Wähle eine Annotationseigenschaft:</div>
              <div class='flex flex-col w-full justify-evenly gap-2 my-4'>
                <div
                  class='transition flex justify-center items-center bg-gray-400 hover:bg-gray-300 hover:ring-2 ring-highlight-900 cursor-pointer rounded-lg p-2'
                  v-for='taskType in taskTypes'
                  :key='taskType.index'
                  :class="taskCreationForm.task_type === taskType.index && 'bg-gray-500 ring-2 ring-highlight-900'"
                  @click='taskCreationForm.task_type = taskType.index'
                >
                  <div class='flex flex-col gap-3 justify-center items-center'>
                    {{ taskType.description }}
                  </div>
                </div>
              </div>
              <div class='text-gray-200 flex text-sm items-center'>
                <Icon name='info' width='20' height='20' />
                <div class='ml-2'>Annotationsklassen geben einer Annotation einen bestimmten Typ / Namen.</div>
              </div>
            </div>

            <div class='my-8'>
              <div class='mb-4'>Welche Art von Annotation soll für die Aufgabe verwendet werden:</div>
              <div class='flex w-full justify-evenly'>
                <div
                  class='transition flex justify-center items-center w-32 h-20 bg-gray-400 hover:bg-gray-300 hover:ring-2 ring-highlight-900 cursor-pointer rounded-lg'
                  v-for='item in typeSelection'
                  :key='item.index'
                  :class="taskCreationForm.annotation_type === item.index && 'bg-gray-500 ring-2 ring-highlight-900'"
                  @click='taskCreationForm.annotation_type = item.index'
                >
                  <div class='flex flex-col gap-2 justify-center items-center'>
                    <Icon :name='item.icon' :width='30' :height='30' />
                    {{ item.type }}
                  </div>
                </div>
              </div>
              <div class='h-8 mt-4'>
                <div class='text-gray-200 flex text-sm items-center'>
                  <Icon name='info' width='20' height='20' />
                  <div class='ml-2'>
                    Polygon: Die Annotationen können aus Polygonen, Rechtecken und Ellipsen bestehen
                  </div>
                </div>
              </div>
            </div>
            <div class='my-8'>
              <div>Welches Vorwissen ist bei den Lernenden vorhanden:</div>
              <div class='my-2 mb-4 break-words text-sm text-gray-200 py-2'>
                Die Vorwissensstufe bestimmt den Schwierigkeitsgrad der Aufgabe. Mit steigender Stufe wird das Feedback
                weniger unterstützend. Außerdem wird die Aufgabenüberprüfung strenger.
              </div>
              <div class='flex w-full justify-evenly gap-2 my-2'>
                <div
                  class='transition flex justify-center items-center bg-gray-400 hover:bg-gray-300 hover:ring-2 ring-highlight-900 cursor-pointer rounded-lg p-2'
                  v-for='level in knowledgeLevel'
                  :key='level.index'
                  :class="taskCreationForm.knowledge_level === level.index && 'bg-gray-500 ring-2 ring-highlight-900'"
                  @click='taskCreationForm.knowledge_level = level.index'
                >
                  <div class='flex gap-3 justify-center items-center text-center'>
                    {{ level.name }}
                  </div>
                </div>
              </div>
            </div>
            <div class='my-4' v-if='taskCreationForm.task_type === 0'>
              <div>Wie viele Annotationen müssen die Lernenden mindestens richtig treffen:</div>
              <CustomSlider
                :initial-position='taskCreationForm.min_correct'
                @is-released='taskCreationForm.min_correct = $event'
                :min='0'
                :max='50'
                :tooltips='true'
                class='pb-4 pt-11'
              ></CustomSlider>
            </div>
          </div>

          <div v-if='selectedTaskType === 1'>
            <div class='my-2 flex gap-2 flex-col'>
              <div class='mt-2'>Wähle eine Reihe von Bilder:</div>

              <MultiImageUpload
                label='Bilder hochladen'
                tip='Wähle Bilder aus oder ziehe sie in das Feld'
                @images-dropped='setImages'
                :reset-array='resetImageSelectImage'
              ></MultiImageUpload>
            </div>
            <div v-if='noImageSelectedError' class='text-red-400 font-semibold'>
              Bitte wähle mindestens ein Bild aus
            </div>
          </div>
        </AccordionItem>
      </Accordion>
      <div class='flex justify-end w-full mt-4'>
        <primary-button
          @click.prevent="
            $emit('close');
            resetForm();
          "
          class='mr-2 w-32'
          name='Abbrechen'
          bgColor='bg-gray-500'
          bgHoverColor='bg-gray-700'
          fontWeight='font-normal'
        ></primary-button>
        <save-button name='Speichern' type='submit' class='w-36' :loading='taskCreationLoading'></save-button>
      </div>
    </form>
  </div>
</template>
