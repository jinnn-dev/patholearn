<template>
  <content-container>
    <template v-slot:header>
      <!-- <div class="text-7xl font-bold mb-4">PATHOLEARN</div> -->
      <div class="text-7xl">Willkommen zurück {{ appState.user?.firstname }}</div></template
    >
    <template v-slot:content>
      <div class="flex justify-center items-center mb-8">
        <course-search class="w-2/3" @joined="onCourseJoin"> </course-search>
      </div>
      <role-only>
        <div class="flex justify-between items-center">
          <div class="w-full text-xl font-bold text-gray-200 uppercase">Deine Kurse</div>
          <primary-button bgColor="bg-gray-400" class="w-46 h-10" name="Neuer Kurs" @click="showModal = !showModal">
            <ph-plus class="mr-2" :size="24" weight="bold" />
          </primary-button>
        </div>
        <div class="my-8">
          <div v-if="loading" class="flex">
            <skeleton-card
              v-for="i in 4"
              :loading="loading"
              :key="i"
              skeletonClasses="h-24 w-46 ml-4 mb-4"
            ></skeleton-card>
          </div>
          <div v-else class="flex flex-wrap">
            <div v-for="course in ownerCourses" :key="course.id" class="ml-4 mb-4">
              <router-link :to="'/course/' + course.short_name + '/admin'">
                <skeleton-card>
                  <div class="text-xl">{{ course.name }}</div>
                  <task-count-badge :count="course.task_count"></task-count-badge>
                </skeleton-card>
              </router-link>
            </div>
            <no-content v-if="ownerCourses.length === 0" text="Noch keinen Kurs erstellt"></no-content>
          </div>
        </div>
      </role-only>

      <div>
        <div class="text-xl font-bold text-gray-200 uppercase">
          Deine {{ appState.user?.is_superuser ? 'beigetrenen' : '' }} Kurse
        </div>
        <div class="my-8">
          <div v-if="loading" class="flex">
            <skeleton-card v-for="i in 4" :loading="loading" :key="i" skeletonClasses="h-24 w-46 ml-4"></skeleton-card>
          </div>
          <div v-else class="flex flex-wrap">
            <div v-for="course in courses" :key="course.id" class="ml-4">
              <router-link :to="'/course/' + course.short_name">
                <skeleton-card>
                  <div class="text-xl">{{ course.name }}</div>
                  <div class="text-gray-200">bei {{ course.owner.firstname }} {{ course.owner.lastname }}</div>
                  <progress-bar
                    :id="course.short_name"
                    :percentage="course.percentage_solved"
                    :wrongTasks="course.wrong_tasks"
                    :correctTasks="course.correct_tasks"
                    :taskCount="course.task_count"
                  ></progress-bar>
                  <task-count-badge :count="course.task_count"></task-count-badge>
                  <new-task-badge v-if="course.new_tasks"></new-task-badge>
                </skeleton-card>
              </router-link>
            </div>
            <no-content v-if="courses.length === 0" text="Noch keinem Kurs beigetreten"></no-content>
          </div>
        </div>
      </div>
    </template>
  </content-container>

  <modal-dialog :show="showModal">
    <div>
      <h1 class="text-2xl text-center">Erstelle einen neuen Kurs</h1>
      <form @submit.prevent="onSubmit" class="w-full">
        <input-field
          v-model="formData.name"
          label="Kursname"
          placeholder="Pathologie"
          type="text"
          tip="Gebe dem Kurs einen eindeutigen Namen."
          :required="true"
          :errorMessage="courseAlreadyExists ? 'Es gibt bereits einen Kurs mit diesem Namen.' : ''"
        >
        </input-field>
        <!-- <div v-if="courseAlreadyExists" class="text-red-500">Es gibt bereits einen Kurs mit diesem Namen.</div> -->
        <div class="flex flex-end">
          <primary-button
            @click.prevent="hideModal"
            class="mr-2"
            name="Abbrechen"
            bgColor="bg-gray-500"
            fontWeight="font-normal"
          ></primary-button>
          <save-button name="Speichern" type="submit" :loading="courseIsCreating"></save-button>
        </div>
      </form>
    </div>
  </modal-dialog>
</template>

<script lang="ts">
import { defineComponent, onMounted, reactive, ref } from 'vue';
import { CourseService } from '../services/course.service';
import { Course } from '../model/course';
import { AuthService } from '../services/auth.service';
import router from '../router';

import ModalDialog from '../components/containers/ModalDialog.vue';
import CourseSearch from '../components/CourseSearch.vue';
import ProgressBar from '../components/ProgressBar.vue';
import ContentContainer from '../components/containers/ContentContainer.vue';
import { appState } from '../utils/app.state';
import TaskCountBadge from '../components/TaskCountBadge.vue';
import NoContent from '../components/NoContent.vue';
import NewTaskBadge from '../components/NewTaskBadge.vue';

export default defineComponent({
  name: 'Home',
  components: { ModalDialog, CourseSearch, ProgressBar, ContentContainer, TaskCountBadge, NoContent, NewTaskBadge },

  setup() {
    const courses = ref<Course[]>([]);
    const ownerCourses = ref<Course[]>([]);
    const loading = ref<Boolean>(true);

    const showModal = ref<Boolean>(false);

    const courseIsCreating = ref<boolean>(false);
    const courseAlreadyExists = ref<boolean>(false);

    const formData = reactive({
      name: ''
    });

    onMounted(async () => {
      courses.value = await CourseService.getMemberCourses();
      if (appState.user?.is_superuser) {
        ownerCourses.value = await CourseService.getMyCourses();
      }
      loading.value = false;
    });

    const onLogout = () => {
      AuthService.logout();
      router.go(0);
    };

    const onSubmit = () => {
      courseIsCreating.value = true;
      CourseService.createCourse({ name: formData.name })
        .then((res) => {
          res.task_count = 0;
          ownerCourses.value.push(res);
          courseIsCreating.value = false;
          showModal.value = false;
        })
        .catch((error) => {
          courseIsCreating.value = false;
          if (error.response) {
            if (error.response.status === 400) {
              courseAlreadyExists.value = true;
            }
          }
        });
    };

    const hideModal = () => {
      showModal.value = false;
      courseAlreadyExists.value = false;
      formData.name = '';
    };

    const onCourseJoin = (course: Course) => {
      courses.value.push(course);
    };

    return {
      appState,
      courses,
      onLogout,
      ownerCourses,
      loading,
      showModal,
      onSubmit,
      formData,
      onCourseJoin,
      courseIsCreating,
      hideModal,
      courseAlreadyExists
    };
  }
});
</script>

<style></style>
