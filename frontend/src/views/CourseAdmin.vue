<template>
  <content-container>
    <template v-slot:header>
      <content-header link="/home" linkText="Zurück zur Kursauswahl" :text="course?.name"></content-header>
    </template>
    <template v-slot:content>
      <div class="flex gap-10 flex-1">
        <div class="flex-1">
          <subheader text="Aufgabengruppen"></subheader>

          <div class="flex justify-between gap-4 my-4">
            <div class="flex gap-4">
              <primary-button
                bgColor="bg-gray-400"
                class="w-64 h-10"
                name="Neue Aufgabengruppe"
                @click="showGroupModal = !showGroupModal"
              >
                <Icon name="plus" class="mr-2" weight="bold" />
              </primary-button>
            </div>
            <primary-button
              class="w-32"
              fontWeight="font-medium"
              textColor="text-red-400"
              bgColor="bg-gray-700"
              name="Kurs löschen"
              @click="showDeleteCourse = true"
            ></primary-button>
          </div>
          <div class="my-8">
            <div v-if="loading" class="flex">
              <skeleton-card
                v-for="i in 4"
                :loading="loading"
                :key="i"
                skeletonClasses="h-24 w-46 ml-4"
              ></skeleton-card>
            </div>
            <div v-else class="flex flex-wrap">
              <div v-for="taskgroup in course?.task_groups" :key="taskgroup.short_name" class="ml-4 mb-4">
                <router-link :to="'/group/' + taskgroup.short_name + '/admin'">
                  <skeleton-card>
                    <div class="text-xl flex justify-between items-center">
                      <div>
                        {{ taskgroup.name }}
                      </div>
                      <div>
                        <Icon
                          name="trash"
                          class="text-red-400 cursor-pointer ml-4 hover:text-red-500"
                          weight="bold"
                          @click.prevent="
                            showDeleteTaskGroup = true;
                            deleteTaskGroupItem = taskgroup;
                          "
                        ></Icon>
                      </div>
                    </div>

                    <task-count-badge :count="taskgroup.task_count"></task-count-badge>
                  </skeleton-card>
                </router-link>
              </div>
              <no-content v-if="course?.task_groups?.length === 0" text="Keine Aufgabengrupppen erstellt"></no-content>
            </div>
          </div>
        </div>

        <div class="bg-gray-700 rounded-lg min-w-56 px-4 max-w-64 max-h-150 overflow-auto">
          <h2 class="sticky top-0 text-xl font-medium mb-4 py-2 bg-gray-700">Mitglieder</h2>
          <no-content
            class="mt-10"
            v-if="course?.members?.length === 0"
            text="Keine Mitglieder"
            iconSize="w-20"
          ></no-content>

          <div class="overflow-y-auto">
            <skeleton-card
              v-for="member of course?.members"
              :key="member.id"
              class="bg-gray-600 w-full rounded-lg p-1 px-2 my-2 min-h-8"
            >
              {{ member.firstname }} {{ member.middlename }} {{ member.lastname }}
            </skeleton-card>
          </div>
        </div>
      </div>
    </template>
  </content-container>

  <modal-dialog :show="showGroupModal">
    <div class="relative">
      <h1 class="text-2xl text-center">Erstelle eine neue Aufgabengruppe</h1>
      <form @submit.prevent="onGroupSubmit" class="w-full">
        <input-field
          v-model="fromGroupData.name"
          label="Gruppenname"
          placeholder="Entzündungen"
          tip="Gebe der Gruppe einen eindeutigen Namen"
          :errorMessage="taskGroupExists ? 'Es existiert bereits eine Gruppe mit diesem Namen' : ''"
          type="text"
          :required="true"
          class="w-96"
        >
        </input-field>

        <div class="flex flex-end">
          <primary-button
            @click.prevent="onTaskGroupClose"
            class="mr-2"
            name="Abbrechen"
            bgColor="bg-gray-500"
            bgHoverColor="bg-gray-700"
            fontWeight="font-normal"
          ></primary-button>
          <save-button name="Speichern" type="submit" :loading="taskGroupLoading"></save-button>
        </div>
      </form>
    </div>
  </modal-dialog>

  <modal-dialog :show="showDeleteCourse">
    <div class="relative">
      <h1 class="text-2xl">Möchtest du den Kurs wirklich löschen?</h1>
      <div class="my-4">Alle zugehörigen Aufgabengruppen, Aufgaben und Lösungen werden gelöscht.</div>
      <div class="flex justify-end">
        <primary-button
          @click.prevent="showDeleteCourse = false"
          class="mr-2 w-28"
          name="Nein"
          bgColor="bg-gray-500"
          bgHoverColor="bg-gray-700"
          fontWeight="font-normal"
        ></primary-button>
        <save-button name="Ja" type="submit" :loading="deleteLoading" @click="deleteCourse" class="w-28"></save-button>
      </div>
    </div>
  </modal-dialog>

  <role-only>
    <modal-dialog :show="showDeleteTaskGroup">
      <div class="relative">
        <h1 class="text-2xl">Möchtest du die Aufgabengruppe löschen?</h1>
        <div class="my-4">Alle Aufgaben und Lösungen werden gelöscht.</div>
        <div class="flex justify-end">
          <primary-button
            @click.prevent="showDeleteTaskGroup = false"
            class="mr-2 w-28"
            name="Nein"
            bgColor="bg-gray-500"
            bgHoverColor="bg-gray-700"
            fontWeight="font-normal"
          ></primary-button>
          <save-button
            name="Ja"
            type="submit"
            :loading="deleteTaskGroupLoading"
            @click="deleteTaskGroup"
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
import { Course } from '../model/course';
import { CourseService } from '../services/course.service';
import { TaskService } from '../services/task.service';
import { Slide } from '../model/slide';
import { TaskGroupService } from '../services/task-group.service';
import { TaskGroup } from '../model/taskGroup';
import { BaseTask } from '../model/baseTask';
import router from '../router';

export default defineComponent({
  setup() {
    const course = ref<Course>();
    const route = useRoute();

    const loading = ref<Boolean>(true);

    const showModal = ref<Boolean>(false);
    const formData = reactive({ name: '', slide_id: '', task_group_id: -1 });
    const taskLoading = ref<boolean>(false);
    const taskError = ref<boolean>(false);

    const fromGroupData = reactive({ name: '' });
    const taskGroupExists = ref<boolean>(false);
    const taskGroupLoading = ref<boolean>(false);
    const showGroupModal = ref<Boolean>(false);

    const taskGroups = ref<TaskGroup[]>([]);

    const baseTasksWithoutGroups = ref<BaseTask[]>([]);

    const showDeleteCourse = ref<Boolean>(false);
    const deleteLoading = ref<Boolean>(false);

    const showDeleteTaskGroup = ref<Boolean>(false);
    const deleteTaskGroupLoading = ref<Boolean>(false);
    const deleteTaskGroupItem = ref<TaskGroup>();

    onMounted(async () => {
      course.value = await CourseService.getCourseDetails(route.params.id as string);
      loading.value = false;
    });

    const onSubmit = () => {
      taskLoading.value = true;
      TaskService.createBaseTask({
        name: formData.name,
        slide_id: formData.slide_id,
        ...(formData.task_group_id !== -1 && { task_group_id: formData.task_group_id }),
        course_id: course.value?.id as number
      })
        .then((res: BaseTask) => {
          taskLoading.value = false;
          showModal.value = false;
          formData.name = '';
          formData.slide_id = '';
          formData.task_group_id = -1;
        })
        .catch((error) => {
          if (error.response) {
            if (error.response.status === 400) {
              taskError.value = true;
            }
          }
          taskLoading.value = false;
        });
    };

    const loadTaskGroups = () => {
      TaskGroupService.getTaskGroups(course.value?.id as number).then((res: TaskGroup[]) => {
        taskGroups.value = res;
      });
    };

    const onGroupSubmit = () => {
      taskGroupLoading.value = true;
      TaskGroupService.createTaskGroup(fromGroupData.name, course.value?.id as number)
        .then((res) => {
          res.task_count = 0;
          course.value?.task_groups.push(res);
          showGroupModal.value = false;
          taskGroupLoading.value = false;
        })
        .catch((error) => {
          if (error.response) {
            if (error.response.status === 400) {
              taskGroupExists.value = true;
            }
          }
          taskGroupLoading.value = false;
        });
    };

    const onTaskGroupClose = () => {
      showGroupModal.value = false;
      fromGroupData.name = '';
      taskGroupExists.value = false;
    };

    const onTaskClose = () => {
      showModal.value = false;
      formData.name = '';
      formData.slide_id = '';
      formData.task_group_id = -1;
    };

    const setSlide = (slide: Slide) => {
      formData.slide_id = slide.id + '';
    };

    const setGroup = (taskGroup: TaskGroup) => {
      formData.task_group_id = taskGroup.id;
    };

    const deleteCourse = () => {
      deleteLoading.value = true;
      CourseService.deleteCourse(course.value!.short_name!)
        .then((res: Course) => {
          if (res) {
            router.push('/home');
          }
          deleteLoading.value = false;
          showDeleteCourse.value = false;
        })
        .catch((err) => {
          console.log(err);
          deleteLoading.value = false;
          showDeleteCourse.value = false;
        });
    };

    const deleteTaskGroup = () => {
      deleteTaskGroupLoading.value = true;

      TaskGroupService.removeTaskGroup(deleteTaskGroupItem.value!.short_name).finally(() => {
        course.value!.task_groups = course.value?.task_groups.filter(
          (item) => item.short_name != deleteTaskGroupItem.value!.short_name
        )!;
        showDeleteTaskGroup.value = false;
        deleteTaskGroupLoading.value = false;
      });
    };
    return {
      course,
      loading,
      showModal,
      onSubmit,
      formData,
      setSlide,
      showGroupModal,
      fromGroupData,
      onGroupSubmit,
      setGroup,
      loadTaskGroups,
      taskGroups,
      taskGroupExists,
      baseTasksWithoutGroups,
      taskGroupLoading,
      onTaskGroupClose,
      taskError,
      taskLoading,
      deleteLoading,
      showDeleteCourse,
      onTaskClose,
      deleteCourse,
      showDeleteTaskGroup,
      deleteTaskGroupLoading,
      deleteTaskGroup,
      deleteTaskGroupItem
    };
  }
});
</script>

<style></style>
