<template>
  <content-container>
    <template v-slot:header v-if="isMember">
      <content-header
        :link="`/course/${taskGroup?.course_short_name}`"
        linkText="Zurück zum Kurs"
        :text="taskGroup?.name"
      ></content-header>
    </template>
    <template v-slot:content>
      <not-course-member v-if="!isMember" :course="course" @courseJoined="loadTaskGroup"></not-course-member>

      <div v-else>
        <div>
          <div class="flex justify-between items-center">
            <div class="w-full text-xl font-bold text-gray-200 uppercase">Deine Aufgaben</div>
          </div>

          <no-content v-if="taskGroup?.tasks.length === 0" text="Keine Aufgaben vorhanden" class="mt-12"></no-content>
          <div v-else class="flex flex-wrap my-8">
            <div v-for="baseTask in taskGroup?.tasks" :key="baseTask.id" class="ml-4 mb-4">
              <skeleton-card
                class="min-w-40 cursor-pointer relative"
                @click="baseTask.task_count && baseTask.task_count > 0 && $router.push('/task/' + baseTask.short_name)"
              >
                <div class="flex justify-between">
                  <div class="text-xl">{{ baseTask.name }}</div>
                </div>

                <progress-bar
                  :id="baseTask.short_name"
                  :percentage="baseTask.percentage_solved"
                  :correctTasks="baseTask.correct_tasks"
                  :wrongTasks="baseTask.wrong_tasks"
                  :taskCount="baseTask.task_count"
                ></progress-bar>
                <task-count-badge :count="baseTask.task_count"></task-count-badge>
                <new-task-badge v-if="baseTask.new_tasks"></new-task-badge>
              </skeleton-card>
            </div>
          </div>
        </div>
      </div>
    </template>
  </content-container>
  <div class="w-full flex justify-center pt-8">
    <div class="w-9/10"></div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';
import { TaskGroupService, TaskService } from '../services';
import { BaseTask, Course, Slide, TaskGroup } from '../model';

export default defineComponent({
  setup() {
    const showModal = ref<Boolean>(false);

    const taskGroup = ref<TaskGroup>();

    const route = useRoute();
    const isMember = ref<Boolean>(true);
    const course = ref<Course>();

    const formData = reactive({
      name: '',
      slide_id: -1
    });
    const taskLoading = ref<boolean>(false);
    const taskError = ref<boolean>(false);

    onMounted(() => {
      loadTaskGroup();
    });

    const loadTaskGroup = () => {
      TaskGroupService.getTaskGroup(route.params.id as string)
        .then((res: TaskGroup) => {
          taskGroup.value = res;
          isMember.value = true;
          taskLoading.value = false;
        })
        .catch((err) => {
          if (err.response) {
            if (err.response.status === 403) {
              isMember.value = false;
              taskLoading.value = false;
              course.value = err.response.data.detail.course;
            }
          }
        });
    };

    const setSlide = (slide: Slide) => {
      formData.slide_id = slide.id;
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

    return {
      taskGroup,
      showModal,
      formData,
      onSubmit,
      setSlide,
      taskLoading,
      taskError,
      isMember,
      course,
      onTaskClose,
      loadTaskGroup
    };
  }
});
</script>

<style></style>
