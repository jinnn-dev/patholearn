<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue';
import { Course } from '../model/course';
import { useRoute, useRouter } from 'vue-router';
import { CourseService } from '../services/course.service';
import ContentContainer from '../components/containers/ContentContainer.vue';
import NoContent from '../components/general/NoContent.vue';
import NewTaskBadge from '../components/task/NewTaskBadge.vue';
import SkeletonCard from '../components/containers/SkeletonCard.vue';
import TaskCountBadge from '../components/task/TaskCountBadge.vue';
import ProgressBar from '../components/task/ProgressBar.vue';
import DangerButton from '../components/general/DangerButton.vue';
import Subheader from '../components/general/Subheader.vue';
import NotCourseMember from '../components/course/NotCourseMember.vue';
import ContentHeader from '../components/general/ContentHeader.vue';

const course = ref<Course>();
const route = useRoute();

const isMember = ref<boolean>(true);

const loading = ref<boolean>(true);
const leaveCourseLoading = ref<boolean>(false);

const showModal = ref<boolean>(false);
const formData = reactive({
  name: '',
  slide_id: ''
});

const router = useRouter();

onMounted(() => {
  loadCourseDetails();
});

const loadCourseDetails = () => {
  CourseService.getCourseDetails(route.params.id as string)
    .then((res: Course) => {
      course.value = res;
      loading.value = false;
      isMember.value = true;
    })
    .catch((err) => {
      if (err.response) {
        if (err.response.status === 403) {
          isMember.value = false;
          loading.value = false;
          course.value = err.response.data.detail.course;
        }
      }
    });
};

const leaveGroup = () => {
  leaveCourseLoading.value = true;
  CourseService.leaveCourse(course.value?.short_name!)
    .then(() => {
      router.push('/home');
      leaveCourseLoading.value = false;
    })
    .catch((error) => {
      leaveCourseLoading.value = false;
      console.log(error);
    });
};
</script>
<template>
  <content-container>
    <template v-if="isMember" v-slot:header>
      <content-header
        :subText="`bei ${course?.owner.firstname} ${course?.owner.middlename ? course?.owner.middlename : ''} ${
          course?.owner.lastname
        }`"
        :text="course?.name"
        link="/home"
        linkText="Zurück zur Kursauswahl"
      ></content-header>
    </template>
    <template v-slot:content>
      <not-course-member v-if="!isMember" :course="course" @courseJoined="loadCourseDetails"></not-course-member>
      <div v-else>
        <div>
          <div class="flex">
            <subheader class="w-full" text="Aufgabengruppen"></subheader>
            <danger-button
              :loading="leaveCourseLoading"
              :show="showModal"
              buttonText="Kurs verlassen"
              customClasses="w-72"
              header="Möchtest du die Gruppe wirklich verlassen?"
              info="All dein Fortschritt wird gelöscht!"
              @confirmation="leaveGroup"
            >
            </danger-button>
          </div>

          <div class="my-8">
            <div v-if="loading" class="flex">
              <skeleton-card
                v-for="i in 4"
                :key="i"
                :loading="loading"
                skeletonClasses="h-24 w-44 ml-4"
              ></skeleton-card>
            </div>
            <div v-else class="flex flex-wrap">
              <div v-for="taskgroup in course?.task_groups" :key="taskgroup.short_name" class="ml-4 mb-4">
                <router-link :to="'/group/' + taskgroup.short_name">
                  <skeleton-card class="min-w-[15rem]">
                    <div class="text-xl">
                      {{ taskgroup.name }}
                    </div>
                    <progress-bar
                      :id="taskgroup.short_name"
                      :correctTasks="taskgroup.correct_tasks"
                      :percentage="taskgroup.percentage_solved"
                      :taskCount="taskgroup.task_count"
                      :wrongTasks="taskgroup.wrong_tasks"
                    ></progress-bar>

                    <task-count-badge :count="taskgroup.task_count"></task-count-badge>
                    <new-task-badge v-if="taskgroup.new_tasks"></new-task-badge>
                  </skeleton-card>
                </router-link>
              </div>
              <no-content v-if="course?.task_groups?.length === 0" text="Keine Aufgabengrupppen vorhanden"></no-content>
            </div>
          </div>
        </div>
      </div>
    </template>
  </content-container>
</template>
