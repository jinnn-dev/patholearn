<script setup lang="ts">
import { AiService } from '../../../services/ai.service';
import { useService } from '../../../composables/useService';
import SkeletonCard from '../../../components/containers/SkeletonCard.vue';

import TaskCard from './TaskCard.vue';
import TaskCreate from './TaskCreate.vue';
import NoContent from '../../general/NoContent.vue';
import ModalDialog from '../../containers/ModalDialog.vue';
import ConfirmButtons from '../../general/ConfirmButtons.vue';
import InputField from '../../form/InputField.vue';
import InputArea from '../../form/InputArea.vue';

import { Task, UpdateTask } from '../../../model/ai/tasks/task';
import { reactive, ref } from 'vue';

const props = defineProps({
  projectId: {
    type: String,
    required: true
  }
});

const { result: tasks, loading, run } = useService(AiService.getTasksToProject, true, props.projectId);

const { result: updateResult, loading: updateLoading, run: updateTask } = useService(AiService.updateTask);

const showEditDialog = ref();

const updateData = reactive<UpdateTask>({ id: '' });

const onTaskDelete = (taskId: string) => {
  const index = tasks.value?.findIndex((task) => task.id === taskId);
  if (index !== undefined && index > -1) {
    tasks.value?.splice(index, 1);
  }
};

const taskCreated = (task: Task) => {
  if (tasks.value) {
    tasks.value.push(task);
  } else {
    tasks.value = [task];
  }
};

const editTask = async (project: Task) => {
  updateData.id = project.id;
  updateData.name = project.name;
  updateData.description = project.description;
  showEditDialog.value = true;
};

const runUpdate = async () => {
  await updateTask(updateData);
  showEditDialog.value = false;
  if (updateResult.value) {
    updateLocalTask(updateResult.value);
  }
};

const updateLocalTask = (updatedTask: Task) => {
  const index = tasks.value?.findIndex((task) => task.id === updatedTask.id);
  if (index !== undefined && index > -1 && tasks.value) {
    tasks.value[index] = updatedTask;
  }
};

const cancelUpdate = async () => {
  updateData.name = undefined;
  updateData.description = undefined;
  showEditDialog.value = false;
};
</script>
<template>
  <modal-dialog :show="showEditDialog" custom-classes="w-96">
    <input-field
      v-model:model-value="updateData.name"
      label="Name"
      tip="Name des Projekts"
      :required="true"
    ></input-field>
    <input-area
      v-model:model-value="updateData.description"
      class="h-64"
      label="Beschreibung"
      tip="Beschreibung des Projekts"
    ></input-area>
    <confirm-buttons
      confirm-text="Speichern"
      reject-text="Abbrechen"
      @confirm="runUpdate"
      @reject="cancelUpdate"
      :loading="updateLoading"
    ></confirm-buttons>
  </modal-dialog>
  <div>
    <div v-if="loading" class="flex gap-5 flex-wrap">
      <skeleton-card :loading="true" v-for="i in [0, 1, 3, 4]" skeleton-classes="w-36 h-24"></skeleton-card>
    </div>
    <div v-else>
      <div>
        <task-create :project-id="projectId" @task-created="taskCreated"></task-create>
      </div>
      <div class="mt-4">
        <div v-if="!tasks || tasks.length === 0">
          <no-content text="Keine Aufgaben vorhanden"></no-content>
        </div>
        <div class="flex gap-4 flex-wrap" v-else>
          <task-card v-for="task in tasks" :task="task" @task-deleted="onTaskDelete" @edit="editTask(task)"></task-card>
        </div>
      </div>
    </div>
  </div>
</template>
