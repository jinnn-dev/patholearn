<template class="relative">
  <content-container>
    <template v-slot:header>
      <content-header
        :link="`/course/${taskGroup?.course_short_name}/admin`"
        linkText="Zurück zum Kurs"
        :text="taskGroup?.name"
      ></content-header>
    </template>
    <template v-slot:content>
      <div class="flex justify-between items-center">
        <div class="w-full text-xl font-bold text-gray-200 uppercase">Deine Aufgaben</div>
      </div>
      <div class="my-4 flex justify-between">
        <primary-button class="w-48 h-10" name="Neue Aufgabe" bgColor="bg-gray-400" @click="showModal = !showModal">
          <Icon name="plus" class="mr-2" weight="bold" />
        </primary-button>
        <primary-button
          class="w-56"
          fontWeight="font-medium"
          textColor="text-red-400"
          bgColor="bg-gray-700"
          name="Aufgabengruppe löschen"
          @click="showTaskgroupDelete = true"
        ></primary-button>
      </div>

      <div class="flex flex-wrap my-8">
        <no-content v-if="taskGroup?.tasks.length === 0" text="Noch keine Aufgaben erstellt"></no-content>
        <div v-for="baseTask in taskGroup?.tasks" :key="baseTask.id" class="ml-4 mb-4">
          <task-group-admin-card
            :baseTask="baseTask"
            @deleteBaseTask="
              showDeleteBaseTask = true;
              deleteBaseTaskItem = baseTask;
            "
          ></task-group-admin-card>
        </div>
      </div>
    </template>
  </content-container>

  <modal-dialog :show="showModal">
    <div class="relative">
      <h1 class="text-2xl text-center">Erstelle eine neue Aufgabe</h1>
      <form @submit.prevent="onSubmit" class="w-full">
        <input-field
          v-model="formData.name"
          label="Aufgabenname"
          placeholder="Markiere alle ..."
          tip="Gebe der Aufgabe einen eindeutigen Namen"
          type="text"
          :required="true"
          class="w-96"
          :errorMessage="taskError ? 'Es gibt bereits eine Aufgabe mit diesem Namen' : ''"
        >
        </input-field>
        <slide-select @slideChanged="setSlide($event)"></slide-select>

        <div class="flex flex-end">
          <primary-button
            @click.prevent="onTaskClose"
            class="mr-2"
            name="Abbrechen"
            bgColor="bg-gray-500"
            bgHoverColor="bg-gray-700"
            fontWeight="font-normal"
          ></primary-button>
          <save-button name="Speichern" type="submit" :loading="taskLoading"></save-button>
        </div>
      </form>
    </div>
  </modal-dialog>

  <modal-dialog :show="showTaskgroupDelete">
    <div class="relative">
      <h1 class="text-2xl">Möchtest du die Aufgabengruppe löschen?</h1>
      <div class="my-4">Alle zugehörigen Aufgaben und Lösungen werden gelöscht.</div>
      <div class="flex justify-end">
        <primary-button
          @click.prevent="showTaskgroupDelete = false"
          class="mr-2 w-28"
          name="Nein"
          bgColor="bg-gray-500"
          bgHoverColor="bg-gray-700"
          fontWeight="font-normal"
        ></primary-button>
        <save-button
          name="Ja"
          type="submit"
          :loading="deleteLoading"
          @click="deleteTaskGroup"
          class="w-28"
        ></save-button>
      </div>
    </div>
  </modal-dialog>

  <role-only>
    <modal-dialog :show="showDeleteBaseTask">
      <div class="relative">
        <h1 class="text-2xl">Möchtest du die Aufgabe löschen?</h1>
        <div class="my-4">Alle Aufgaben und Lösungen werden gelöscht.</div>
        <div class="flex justify-end">
          <primary-button
            @click.prevent="showDeleteBaseTask = false"
            class="mr-2 w-28"
            name="Nein"
            bgColor="bg-gray-500"
            bgHoverColor="bg-gray-700"
            fontWeight="font-normal"
          ></primary-button>
          <save-button
            name="Ja"
            type="submit"
            :loading="deleteBaseLoading"
            @click="deleteBaseTask"
            class="w-28"
          ></save-button>
        </div>
      </div>
    </modal-dialog>
  </role-only>
</template>

<script lang="ts">
import { defineComponent, nextTick, onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';
import { TaskGroup } from '../model/taskGroup';
import { Slide } from '../model/slide';
import { BaseTask } from '../model/baseTask';
import { TaskService } from '../services/task.service';
import { TaskGroupService } from '../services/task-group.service';
import router from '../router';

export default defineComponent({
  setup() {
    const showDeleteBaseTask = ref<Boolean>(false);
    const deleteBaseLoading = ref<Boolean>(false);
    const deleteBaseTaskItem = ref<BaseTask>();

    const showModal = ref<Boolean>(false);

    const taskGroup = ref<TaskGroup>();

    const route = useRoute();

    const formData = reactive({
      name: '',
      slide_id: ''
    });

    const taskLoading = ref<Boolean>(false);
    const taskError = ref<Boolean>(false);

    const showTaskgroupDelete = ref<Boolean>(false);
    const deleteLoading = ref<Boolean>(false);

    onMounted(() => {
      TaskGroupService.getTaskGroup(route.params.id as string).then((res: TaskGroup) => {
        taskGroup.value = res;
      });
    });
    const setSlide = (slide: Slide) => {
      formData.slide_id = slide.slide_id;
    };

    const onSubmit = () => {
      taskLoading.value = true;
      TaskService.createBaseTask({
        name: formData.name,
        slide_id: formData.slide_id,
        course_id: taskGroup.value?.course_id as number,
        task_group_id: taskGroup.value?.id
      })
        .then((res: BaseTask) => {
          res.task_count = 0;
          taskGroup.value?.tasks.push(res);
          taskLoading.value = false;
          showModal.value = false;
        })
        .catch((error) => {
          if (error.response) {
            if (error.response.status === 400) {
              taskError.value = true;
              taskLoading.value = false;
            }
          }
        });
    };

    const onTaskClose = () => {
      showModal.value = false;
      formData.name = '';
      taskError.value = false;
    };

    const deleteTaskGroup = () => {
      TaskGroupService.removeTaskGroup(taskGroup.value!.short_name!)
        .then((res: TaskGroup) => {
          if (res) {
            showTaskgroupDelete.value = false;
            deleteLoading.value = false;
            router.push('/home');
          }
        })
        .catch((err) => {
          console.log(err);

          showTaskgroupDelete.value = false;
          deleteLoading.value = false;
        });
    };

    const deleteBaseTask = () => {
      deleteBaseLoading.value = true;
      TaskService.deleteBaseTask(deleteBaseTaskItem.value!.short_name)
        .then()
        .catch((err) => {
          console.log(err);
        })
        .finally(() => {
          taskGroup.value!.tasks = taskGroup.value?.tasks.filter(
            (item) => item.short_name !== deleteBaseTaskItem.value!.short_name
          )!;
          showDeleteBaseTask.value = false;
          deleteBaseLoading.value = false;
        });
    };

    return {
      taskGroup,
      showModal,
      formData,
      taskLoading,
      taskError,
      showTaskgroupDelete,
      deleteLoading,
      onTaskClose,
      deleteTaskGroup,
      onSubmit,
      setSlide,
      showDeleteBaseTask,
      deleteBaseLoading,
      deleteBaseTaskItem,
      deleteBaseTask
    };
  }
});
</script>

<style></style>
