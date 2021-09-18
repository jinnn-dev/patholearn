<template>
  <div class="w-full flex items-center justify-between p-2 bg-gray-600 sticky top-0">
    <div class="mr-2">{{ layerIndex }}. Ebene</div>
    <role-only class="flex gap-2" v-if="isOwner">
      <ph-minus
        v-if="layerIndex !== 1"
        :size="18"
        class="text-white cursor-pointer"
        weight="bold"
        @click="removeLayer"
      ></ph-minus>
    </role-only>
  </div>
  <div class="w-full cursor-pointer">
    <task-item
      v-for="(task, taskIndex) in tasks"
      :key="task.id"
      :isOwner="isOwner"
      :question="task.task_question"
      :userSolution="task.user_solution"
      :class="selectedTaskId === task.id ? 'ring-2 ring-highlight-800' : ''"
      @click.stop="selectTask(task)"
      @deleteTask="deleteTask(task.id, taskIndex)"
      @editTask="editTask(task)"
    ></task-item>
    <role-only v-if="isOwner"
      ><div class="p-2 px-18 my-2">
        <primary-button @click="showTaskDialog" class="">Neue Aufgabe</primary-button>
      </div>
    </role-only>
  </div>

  <role-only>
    <modal-dialog :show="taskCreationModal">
      <div>
        <h1 class="text-2xl text-center">Füge eine neue Aufgabe der {{ taskCreationForm.layer }}. Ebene hinzu</h1>
        <form @submit.prevent="onSubmit" class="w-full">
          <input-field
            v-model="taskCreationForm.task_question"
            label="Fragestellung"
            placeholder="Markiere..."
            type="text"
            :required="true"
          >
          </input-field>

          <div class="my-4">
            <div>Wähle einen Aufgabentyp:</div>
            <div class="flex flex-col w-full justify-evenly gap-2 my-2">
              <div
                class="
                  transition
                  flex
                  justify-center
                  items-center
                  bg-gray-600
                  hover:bg-gray-500 hover:ring-2
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
          </div>

          <div class="my-8">
            <div class="mb-2">Welcher Annotationstyp soll verwendet werden:</div>
            <div class="flex w-full justify-evenly">
              <div
                class="
                  transition
                  flex
                  justify-center
                  items-center
                  w-20
                  h-20
                  bg-gray-600
                  hover:bg-gray-500 hover:ring-2
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
                  <component :is="item.icon" :size="30" />
                  {{ item.type }}
                </div>
              </div>
            </div>
          </div>
          <div class="my-8">
            <div>Welches Vorwissen ist bei den Lernenden vorhanden:</div>
            <div class="my-2 w-130 break-words text-sm text-gray-200">
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
                  bg-gray-600
                  hover:bg-gray-500 hover:ring-2
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
                <div class="flex gap-3 justify-center items-center">
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
          <div class="flex justify-end w-full">
            <primary-button
              @click.prevent="taskCreationModal = false"
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
    </modal-dialog>
    <modal-dialog :show="taskUpdateModal">
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

          <div class="my-8" v-if="taskUpdateForm.task_type === 0">
            <div>Wie viele Annotationen müssen die Lernenden mindestens richtig treffen:</div>
            <div class="pb-4 pt-11">
              <Slider v-model="taskUpdateForm.min_correct" :min="0" :max="50" :tooltips="true"></Slider>
            </div>
          </div>

          <div class="my-8">
            <div>Welches Vorwissen ist bei den Lernenden vorhanden:</div>
            <div class="my-2 w-140 break-words text-sm text-gray-200">
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
                  bg-gray-600
                  hover:bg-gray-500 hover:ring-2
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
                <div class="flex flex-col gap-3 justify-center items-center">
                  {{ level.name }}
                </div>
              </div>
            </div>
          </div>

          <div class="flex justify-end w-full">
            <primary-button
              @click.prevent="taskUpdateModal = false"
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
    </modal-dialog>
  </role-only>
</template>
<script lang="ts">
import { defineComponent, PropType, reactive, ref } from 'vue';
import { required } from '@vuelidate/validators';
import useVuelidate from '@vuelidate/core';
import { Task, TaskCreate } from '../../model';
import { TaskService } from '../../services';
import '@vueform/slider/themes/default.css';
import Slider from '@vueform/slider';

export default defineComponent({
  components: { Slider },

  props: {
    layerIndex: {
      type: Number,
      required: true
    },
    tasks: {
      type: Array as PropType<Task[]>,
      default: []
    },
    baseTaskId: {
      type: Number,
      required: true
    },
    selectedTaskId: Number,
    isOwner: {
      type: Boolean,
      default: false
    }
  },

  emits: ['taskCreated', 'taskUpdated', 'taskSelected', 'taskDeleted', 'layerDeleted'],

  setup(props, { emit }) {
    const taskTypes = [
      {
        index: 0,
        description: 'Beliebige Anzahl von Annotationen einer Annotationsklasse'
      },
      {
        index: 1,
        description: 'Beliebige Anzahl von Annotationen verschiedener Annotationsklassen'
      }
    ];

    const typeSelection = [
      {
        index: 0,
        type: 'Punkt',
        icon: 'ph-push-pin'
      },
      {
        index: 1,
        type: 'Linie',
        icon: 'ph-activity'
      },
      {
        index: 2,
        type: 'Polygon',
        icon: 'ph-triangle'
      }
    ];

    const knowledgeLevel = [
      {
        index: 0,
        name: 'Geringes Vorwissen'
      },
      {
        index: 1,
        name: 'Mittelmäßiges Vorwissen'
      },
      {
        index: 2,
        name: 'Ausgeprägtes Vorwissen'
      }
    ];

    const selectedType = ref<Number>(0);

    const taskCreationModal = ref<Boolean>(false);

    const taskUpdateLoading = ref<Boolean>(false);

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

    const taskUpdateModal = ref<Boolean>(false);
    const taskUpdateForm = reactive<{
      layer: number;
      task_question: string | null;
      knowledge_level: number;
      min_correct: number;
      task_id: number;
      task_type: number;
    }>({
      layer: 0,
      task_question: '',
      knowledge_level: 0,
      min_correct: 0,
      task_id: 0,
      task_type: 0
    });

    const notNull = (value: any) => value != null;

    const rules = {
      task_type: { required, notNull }
    };

    const validator = useVuelidate(rules, taskCreationForm);

    const taskCreationLoading = ref<Boolean>(false);

    const showTaskDialog = () => {
      taskCreationForm.layer = props.layerIndex;
      taskCreationModal.value = true;
    };

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
          annotation_groups: []
        };
        TaskService.createTask(createTask).then((res: Task) => {
          emit('taskCreated', res);
          taskCreationLoading.value = false;
          taskCreationModal.value = false;
          Object.assign(taskCreationForm, initialState);
        });
      }
    };

    const updateTask = async () => {
      taskUpdateLoading.value = true;
      const res = await TaskService.updateTask({
        task_id: taskUpdateForm.task_id,
        task_question: taskUpdateForm.task_question!,
        min_correct: taskUpdateForm.min_correct,
        knowledge_level: taskUpdateForm.knowledge_level
      });
      taskUpdateLoading.value = false;
      taskUpdateModal.value = false;
      emit('taskUpdated', res);
    };

    const selectTask = (task: Task) => {
      emit('taskSelected', task);
    };

    const deleteTask = (taskId: number, taskIndex: number) => {
      TaskService.deleteTask(taskId).then((res: Task) => {
        emit('taskDeleted', { task: res, taskIndex: taskIndex });
      });
    };

    const editTask = (task: Task) => {
      taskUpdateModal.value = true;
      taskUpdateForm.task_id = task.id;
      taskUpdateForm.layer = task.layer;
      taskUpdateForm.task_question = task.task_question;
      taskUpdateForm.knowledge_level = task.knowledge_level;
      taskUpdateForm.min_correct = task.min_correct;
      taskUpdateForm.task_type = task.task_type;
    };

    const removeLayer = async () => {
      for (const task of props.tasks) {
        await TaskService.deleteTask(task.id);
      }
      emit('layerDeleted', props.layerIndex);
    };

    return {
      taskCreationModal,
      taskCreationForm,
      taskCreationLoading,
      validator,
      typeSelection,
      selectedType,
      knowledgeLevel,
      taskTypes,
      showTaskDialog,
      removeLayer,
      onSubmit,
      deleteTask,
      taskUpdateForm,
      taskUpdateLoading,
      editTask,
      selectTask,
      taskUpdateModal,
      updateTask
    };
  }
});
</script>
<style>
.slider-connect,
.slider-tooltip {
  @apply bg-highlight-900;
  @apply border-highlight-900;
}
</style>
