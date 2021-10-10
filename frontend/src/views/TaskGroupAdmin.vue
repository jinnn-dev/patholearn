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
          <router-link :to="'/task/' + baseTask.short_name + '/admin'">
            <skeleton-card class="min-w-40">
              <div class="text-xl flex justify-between items-center">
                <div>
                  {{ baseTask.name }}
                </div>
                <div>
                  <Icon
                    name="trash"
                    class="text-red-400 cursor-pointer ml-4 hover:text-red-500"
                    weight="bold"
                    @click.prevent="
                      showDeleteBaseTask = true;
                      deleteBaseTaskItem = baseTask;
                    "
                  ></Icon>
                </div>
              </div>

              <task-count-badge :count="baseTask.task_count"></task-count-badge>
              <div class="flex mt-2 items-center">
                <div class="w-24 text-sm font-medium">
                  <div v-if="baseTask.enabled" class="text-green-500">Aktiviert</div>
                  <div v-else class="text-red-400">Deaktiviert</div>
                </div>
                <button
                  @click.prevent="toggleEnabledState(baseTask)"
                  type="button"
                  class="
                    bg-gray-200
                    relative
                    inline-flex
                    flex-shrink-0
                    h-6
                    w-11
                    border-2 border-transparent
                    rounded-full
                    cursor-pointer
                    transition-colors
                    ease-in-out
                    duration-200
                    focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500
                  "
                  role="switch"
                  aria-checked="false"
                  :class="baseTask.enabled ? 'bg-green-300' : 'bg-gray-400'"
                >
                  <span
                    aria-hidden="true"
                    class="
                      pointer-events-none
                      inline-block
                      h-5
                      w-5
                      rounded-full
                      bg-white
                      shadow
                      transform
                      ring-0
                      transition
                      ease-in-out
                      duration-200
                    "
                    :class="baseTask.enabled ? 'translate-x-5' : 'translate-x-0'"
                  ></span>
                </button>
              </div>
            </skeleton-card>
          </router-link>
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
import { defineComponent, onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';
import { TaskGroup, Slide, BaseTask } from '../model';
import { TaskGroupService, TaskService } from '../services';
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

    const toggleEnabledState = async (baseTask: BaseTask) => {
      baseTask.enabled = !baseTask.enabled;

      await TaskService.updateBaseTask({ base_task_id: baseTask.id, enabled: baseTask.enabled });
    };

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
      toggleEnabledState,
      deleteBaseTask
    };
  }
});
</script>

<style>
#test {
  /* background: linear-gradient(to bottom right, rgb(245, 175, 25), rgb(17, 16, 16)); */
}
</style>
