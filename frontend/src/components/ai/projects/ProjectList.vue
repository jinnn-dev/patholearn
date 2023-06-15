<script setup lang="ts">
import ProjectCard from './ProjectCard.vue';
import { useService } from '../../../composables/useService';
import { Project, UpdateProject } from '../../../model/ai/projects/project';
import { AiService } from '../../../services/ai.service';
import SkeletonCard from '../../containers/SkeletonCard.vue';
import ProjectCreate from './ProjectCreate.vue';
import NoContent from '../../general/NoContent.vue';
import ModalDialog from '../../containers/ModalDialog.vue';
import { reactive, ref } from 'vue';
import ConfirmButtons from '../../general/ConfirmButtons.vue';
import InputField from '../../form/InputField.vue';
import InputArea from '../../form/InputArea.vue';

const { result: projects, loading, run } = useService(AiService.getProjects, true);

const { result: updateResult, run: updateProject, loading: updateLoading } = useService(AiService.updateProject);

const showEditDialog = ref(false);

const updateData = reactive<UpdateProject>({ id: '' });

const onProjectDelete = (projectId: string) => {
  const index = projects.value?.findIndex((project) => project.id === projectId);
  if (index !== undefined && index > -1) {
    projects.value?.splice(index, 1);
  }
};

const projectCreated = (project: Project) => {
  if (projects.value) {
    projects.value.push(project);
  } else {
    projects.value = [project];
  }
};

const editProject = async (project: Project) => {
  updateData.id = project.id;
  updateData.name = project.name;
  updateData.description = project.description;
  showEditDialog.value = true;
};

const runUpdate = async () => {
  await updateProject(updateData);
  showEditDialog.value = false;
  if (updateResult.value) {
    updateLocalProject(updateResult.value);
  }
};

const updateLocalProject = (updatedProject: Project) => {
  const index = projects.value?.findIndex((project) => project.id === updatedProject.id);
  if (index !== undefined && index > -1 && projects.value) {
    projects.value[index] = updatedProject;
  }
};

const cancelUpdate = async () => {
  updateData.name = undefined;
  updateData.description = undefined;
  showEditDialog.value = false;
};
</script>
<template>
  <div>
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
    <div v-if="loading" class="flex gap-5 flex-wrap">
      <skeleton-card :loading="true" v-for="i in [0, 1, 3, 4]" skeleton-classes="w-36 h-24"></skeleton-card>
    </div>
    <div v-else>
      <project-create @project-created="projectCreated"></project-create>
      <div>
        <div v-if="projects?.length !== 0" class="flex gap-4 flex-wrap mt-4">
          <div v-for="project in projects">
            <project-card :project="project" @delete="onProjectDelete" @edit="editProject(project)"></project-card>
          </div>
        </div>
        <no-content v-else text="Noch kein Projekt vorhanden"></no-content>
      </div>
    </div>
  </div>
</template>
