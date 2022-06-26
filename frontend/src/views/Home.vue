<script lang='ts' setup>
import { onMounted, reactive, ref } from 'vue';
import { Course, CreateCourse } from '../model/course';
import { CourseService } from '../services/course.service';
import { appState } from '../utils/app.state';
import ModalDialog from '../components/containers/ModalDialog.vue';
import PrimaryButton from '../components/general/PrimaryButton.vue';
import InputArea from '../components/form/InputArea.vue';
import InputField from '../components/form/InputField.vue';
import NoContent from '../components/general/NoContent.vue';
import CourseCard from '../components/course/CourseCard.vue';
import ContentContainer from '../components/containers/ContentContainer.vue';
import SkeletonCard from '../components/containers/SkeletonCard.vue';
import RoleOnly from '../components/containers/RoleOnly.vue';
import Icon from '../components/general/Icon.vue';
import CourseSearch from '../components/course/CourseSearch.vue';
import ConfirmButtons from '../components/general/ConfirmButtons.vue';

const courses = ref<Course[]>([]);
const ownerCourses = ref<Course[]>([]);
const loading = ref<Boolean>(true);

const showModal = ref<Boolean>(false);

const courseIsCreating = ref<boolean>(false);
const courseAlreadyExists = ref<boolean>(false);

const formData = reactive<{
  name: string;
  description: string | undefined;
}>({
  name: '',
  description: undefined
});

onMounted(async () => {
  courses.value = await CourseService.getMemberCourses();
  if (appState.user?.is_superuser) {
    ownerCourses.value = await CourseService.getMyCourses();
  }
  loading.value = false;
});

const onSubmit = () => {
  courseIsCreating.value = true;

  const createCourse: CreateCourse = {
    name: formData.name,
    ...(formData.description && {
      description: formData.description
    })
  };

  CourseService.createCourse(createCourse)
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
  resetFormData();
};

const resetFormData = () => {
  formData.name = '';
  formData.description = '';
};

const onCourseJoin = (course: Course) => {
  courses.value.push(course);
};
</script>
<template>
  <content-container>
    <template v-slot:header>
      <div class='flex justify-center w-full text-5xl font-semibold'>
        <div class=''>
          Willkommen zurück
          {{ appState.user?.firstname }}
        </div>
      </div>
    </template>
    <template v-slot:content>
      <div class='flex justify-center items-center mb-8'>
        <course-search class='w-2/3' @joined='onCourseJoin'></course-search>
      </div>
      <role-only>
        <div class='flex justify-between items-center'>
          <div class='w-full text-xl font-bold text-gray-200 uppercase'>Deine Kurse</div>
          <primary-button bgColor='bg-gray-400' class='w-48 h-10' name='Neuer Kurs' @click='showModal = !showModal'>
            <Icon class='mr-2' name='plus' weight='bold' />
          </primary-button>
        </div>
        <div class='my-8'>
          <div v-if='loading' class='flex'>
            <skeleton-card
              v-for='i in 4'
              :key='i'
              :loading='loading'
              skeletonClasses='h-24 w-44 ml-4 mb-4'
            ></skeleton-card>
          </div>
          <div v-else class='flex flex-wrap'>
            <div v-for='course in ownerCourses' :key='course.id' class='ml-4 mb-4'>
              <course-card :course='course' :isCourseOwner='appState.user?.is_superuser' />
            </div>
            <no-content v-if='ownerCourses.length === 0' text='Noch keinen Kurs erstellt'></no-content>
          </div>
        </div>
      </role-only>
      <div>
        <div class='text-xl font-bold text-gray-200 uppercase'>
          Deine
          {{ appState.user?.is_superuser ? 'beigetretenen' : '' }}
          Kurse
        </div>
        <div class='my-8'>
          <div v-if='loading' class='flex'>
            <skeleton-card v-for='i in 4' :key='i' :loading='loading' skeletonClasses='h-24 w-44 ml-4'></skeleton-card>
          </div>
          <div v-else class='flex flex-wrap gap-4'>
            <div v-for='course in courses' :key='course.id'>
              <course-card :course='course' :isCourseOwner='false' />
            </div>
            <no-content v-if='courses.length === 0' text='Noch keinem Kurs beigetreten'></no-content>
          </div>
        </div>
      </div>
    </template>
  </content-container>

  <modal-dialog :show='showModal' customClasses='w-[700px] h-1/2'>
    <div>
      <h1 class='text-2xl text-center'>Erstelle einen neuen Kurs</h1>
      <form class='w-full' @submit.prevent='onSubmit'>
        <input-field
          v-model='formData.name'
          :errorMessage="courseAlreadyExists ? 'Es gibt bereits einen Kurs mit diesem Namen.' : ''"
          :required='true'
          label='Kursname'
          placeholder='Kursname'
          tip='Gebe dem Kurs einen eindeutigen Namen.'
          type='text'
        >
        </input-field>
        <!-- <div v-if="courseAlreadyExists" class="text-red-500">Es gibt bereits einen Kurs mit diesem Namen.</div> -->

        <input-area
          v-model='formData.description'
          class='h-72'
          label='Kursbeschreibung'
          placeholder='Das ist der tollste Kurs'
          tip='Gebe deinem Kurs eine optionale Beschreibung'
        ></input-area>
        <confirm-buttons :loading='courseIsCreating'
                         reject-text='Abbrechen' confirm-text='Speichern'
                         @reject='hideModal'>
        </confirm-buttons>
      </form>
    </div>
  </modal-dialog>
</template>
