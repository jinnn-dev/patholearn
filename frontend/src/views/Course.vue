<template>
  <content-container>
    <template v-slot:header v-if="isMember">
      <content-header
        link="/home"
        linkText="Zurück zur Kursauswahl"
        :text="course?.name"
        :subText="`bei ${course?.owner.firstname} ${course?.owner.middlename ? course?.owner.middlename : ''} ${
          course?.owner.lastname
        }`"
      ></content-header>
    </template>
    <template v-slot:content>
      <not-course-member v-if="!isMember" :course="course" @courseJoined="loadCourseDetails"></not-course-member>
      <div v-else>
        <div>
          <div class="flex justify-between items-center">
            <subheader text="Aufgabengruppen"></subheader>

            <danger-button
              buttonText="Kurs verlassen"
              @confirmation="leaveGroup"
              :show="showModal"
              :loading="leaveCourseLoading"
              header="Möchtest du die Gruppe wirklich verlassen?"
              info="All dein Fortschritt wird gelöscht!"
            >
            </danger-button>
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
                <router-link :to="'/group/' + taskgroup.short_name">
                  <skeleton-card>
                    <div class="text-xl">{{ taskgroup.name }}</div>
                    <progress-bar
                      :id="taskgroup.short_name"
                      :correctTasks="taskgroup.correct_tasks"
                      :wrongTasks="taskgroup.wrong_tasks"
                      :taskCount="taskgroup.task_count"
                      :percentage="taskgroup.percentage_solved"
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

<script lang="ts">
import ProgressBar from '../components/ProgressBar.vue';
import { defineComponent, onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Course } from '../model/course';
import { CourseService } from '../services/course.service';
import NotCourseMember from '../components/NotCourseMember.vue';
import ContentContainer from '../components/containers/ContentContainer.vue';
import Subheader from '../components/Subheader.vue';
import DangerButton from '../components/base/DangerButton.vue';
import TaskCountBadge from '../components/TaskCountBadge.vue';
import NewTaskBadge from '../components/NewTaskBadge.vue';
import NoContent from '../components/NoContent.vue';
import ContentHeader from '../components/ContentHeader.vue';

export default defineComponent({
  components: {
    ProgressBar,
    NotCourseMember,
    ContentContainer,
    Subheader,
    DangerButton,
    TaskCountBadge,
    NewTaskBadge,
    NoContent,
    ContentHeader
  },

  setup(props) {
    const course = ref<Course>();
    const route = useRoute();

    const isMember = ref<Boolean>(true);

    const loading = ref<Boolean>(true);
    const joinLoading = ref<Boolean>(false);
    const leaveCourseLoading = ref<Boolean>(false);

    const showModal = ref<Boolean>(false);
    const formData = reactive({ name: '', slide_id: '' });

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

    const joinCourse = () => {
      joinLoading.value = true;
      CourseService.joinCourse(course.value?.short_name!).then((res) => {
        joinLoading.value = false;
        loadCourseDetails();
      });
    };

    const leaveGroup = () => {
      leaveCourseLoading.value = true;
      CourseService.leaveCourse(course.value?.short_name!)
        .then((res) => {
          router.push('/home');
          leaveCourseLoading.value = false;
        })
        .catch((error) => {
          leaveCourseLoading.value = false;
          console.log(error);
        });
    };

    return {
      course,
      loading,
      showModal,
      formData,
      isMember,
      joinLoading,
      leaveCourseLoading,
      joinCourse,
      leaveGroup,
      loadCourseDetails
    };
  }
});
</script>

<style></style>
