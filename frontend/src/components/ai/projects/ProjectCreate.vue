<script setup lang="ts">
import { ref, reactive } from 'vue';

import PrimaryButton from '../../general/PrimaryButton.vue';
import ModalDialog from '../../containers/ModalDialog.vue';
import ConfirmButtons from '../../general/ConfirmButtons.vue';
import InputField from '../../form/InputField.vue';
import InputArea from '../../form/InputArea.vue';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';

const showCreate = ref<boolean>(false);

const createProjectData = reactive<{ name: string; description?: string }>({
  name: ''
});

const { result, loading, run } = useService(AiService.createProject);

const emit = defineEmits(['project-created']);

const createProject = async () => {
  await run(createProjectData.name, createProjectData.description);
  emit('project-created', result.value);
  showCreate.value = false;
  createProjectData.name = '';
  createProjectData.description = undefined;
};
</script>
<template>
  <div class="flex justify-end items-center">
    <div>
      <primary-button bg-color="bg-gray-500" name="Create Project" @click="showCreate = true"></primary-button>
    </div>
  </div>

  <modal-dialog :show="showCreate" custom-classes="w-96">
    <div class="text-xl">Create Project</div>
    <input-field v-model:model-value="createProjectData.name" label="Name" :required="true"></input-field>
    <input-area v-model:model-value="createProjectData.description" class="h-64" label="Description"></input-area>

    <confirm-buttons
      :loading="loading"
      confirm-text="Save"
      reject-text="Abort"
      @reject="showCreate = false"
      @confirm="createProject"
    ></confirm-buttons>
  </modal-dialog>
</template>
