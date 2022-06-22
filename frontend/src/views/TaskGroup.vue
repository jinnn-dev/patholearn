<script lang='ts' setup>
import { onMounted, reactive, ref } from 'vue';
import { TaskGroup } from '../model/taskGroup';
import { useRoute } from 'vue-router';
import { Course } from '../model/course';
import { TaskGroupService } from '../services/task-group.service';
import { TaskService } from '../services/task.service';
import { BaseTask } from '../model/baseTask';
import ContentContainer from '../components/containers/ContentContainer.vue';
import TaskCountBadge from '../components/TaskCountBadge.vue';
import NewTaskBadge from '../components/NewTaskBadge.vue';
import SkeletonCard from '../components/containers/SkeletonCard.vue';
import ProgressBar from '../components/ProgressBar.vue';
import NoContent from '../components/NoContent.vue';
import NotCourseMember from '../components/NotCourseMember.vue';
import ContentHeader from '../components/ContentHeader.vue';

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

const onSubmit = () => {
  taskLoading.value = true;
  TaskService.createBaseTask({
    name: formData.name,
    slide_id: formData.slide_id + '',
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
</script>
<template>
  <content-container>
    <template v-if='isMember' v-slot:header>
      <content-header
        :link='`/course/${taskGroup?.course_short_name}`'
        :text='taskGroup?.name'
        linkText='Zurück zum Kurs'
      ></content-header>
    </template>
    <template v-slot:content>
      <not-course-member v-if='!isMember' :course='course' @courseJoined='loadTaskGroup'></not-course-member>

      <div v-else>
        <div>
          <div class='flex justify-between items-center'>
            <div class='w-full text-xl font-bold text-gray-200 uppercase'>Deine Aufgaben</div>
          </div>

          <no-content v-if='taskGroup?.tasks.length === 0' class='mt-12' text='Keine Aufgaben vorhanden'></no-content>
          <div v-else class='flex flex-wrap my-8'>
            <div v-for='baseTask in taskGroup?.tasks' :key='baseTask.id' class='ml-4 mb-4'>
              <skeleton-card
                class='min-w-[15rem] cursor-pointer relative'
                @click="baseTask.task_count && baseTask.task_count > 0 && $router.push('/task/' + baseTask.short_name)"
              >
                <div class='flex justify-between'>
                  <div class='text-xl'>
                    {{ baseTask.name }}
                  </div>
                </div>

                <progress-bar
                  :id='baseTask.short_name'
                  :correctTasks='baseTask.correct_tasks'
                  :percentage='baseTask.percentage_solved'
                  :taskCount='baseTask.task_count'
                  :wrongTasks='baseTask.wrong_tasks'
                ></progress-bar>
                <task-count-badge :count='baseTask.task_count'></task-count-badge>
                <new-task-badge v-if='baseTask.new_tasks'></new-task-badge>
              </skeleton-card>
            </div>
          </div>
        </div>
      </div>
    </template>
  </content-container>
  <div class='w-full flex justify-center pt-8'>
    <div class='w-11/12'></div>
  </div>
</template>
