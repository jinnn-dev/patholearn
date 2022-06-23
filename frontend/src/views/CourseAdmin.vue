<script lang='ts' setup>
import { onMounted, reactive, ref, watchEffect } from 'vue';
import { Course, UpdateCourse } from '../model/course';
import { useRoute } from 'vue-router';
import { TaskGroup } from '../model/task/taskGroup';
import { CourseService } from '../services/course.service';
import { TaskService } from '../services/task.service';
import { TaskGroupService } from '../services/task-group.service';
import router from '../router';
import ModalDialog from '../components/containers/ModalDialog.vue';
import SaveButton from '../components/general/SaveButton.vue';
import PrimaryButton from '../components/general/PrimaryButton.vue';
import InputField from '../components/form/InputField.vue';
import ContentContainer from '../components/containers/ContentContainer.vue';
import CourseMembers from '../components/CourseMembers.vue';
import NoContent from '../components/NoContent.vue';
import CourseAdminCard from '../components/CourseAdminCard.vue';
import SkeletonCard from '../components/containers/SkeletonCard.vue';
import Icon from '../components/general/Icon.vue';
import Subheader from '../components/Subheader.vue';
import ContentHeader from '../components/ContentHeader.vue';
import ConfirmButtons from '../components/general/ConfirmButtons.vue';

const course = ref<Course>();
const route = useRoute();

const newCourseName = ref(course.value?.name);

watchEffect(() => {
  newCourseName.value = course.value?.name;
});

const loading = ref<Boolean>(true);

const showModal = ref<Boolean>(false);
const formData = reactive({
  name: '',
  slide_id: '',
  task_group_id: -1
});
const taskLoading = ref<boolean>(false);
const taskError = ref<boolean>(false);

const fromGroupData = reactive({
  name: ''
});
const taskGroupExists = ref<boolean>(false);
const taskGroupLoading = ref<boolean>(false);
const showGroupModal = ref<Boolean>(false);

const showDeleteCourse = ref<Boolean>(false);
const deleteLoading = ref<Boolean>(false);

const editCourseLoading = ref(false);

const showEditCourse = ref<Boolean>(false);

const deleteCourseVerification = ref('');

onMounted(async () => {
  course.value = await CourseService.getCourseDetails(route.params.id as string);
  loading.value = false;
});

const onSubmit = () => {
  taskLoading.value = true;
  TaskService.createBaseTask({
    name: formData.name,
    slide_id: formData.slide_id,
    ...(formData.task_group_id !== -1 && {
      task_group_id: formData.task_group_id
    }),
    course_id: course.value?.id as number
  })
    .then(() => {
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

const deleteCourse = () => {
  if (deleteCourseVerification.value === course.value?.name) {
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
  }
};

const deleteTaskgroup = (taskgroup: TaskGroup) => {
  course.value!.task_groups = course.value?.task_groups.filter((item) => item.short_name != taskgroup.short_name)!;
};

const editTaskgroup = (taskGroup: TaskGroup) => {
  course.value!.task_groups = course.value!.task_groups.map((tg) => {
    if (tg.id === taskGroup.id) {
      tg.name = taskGroup.name;
    }
    return tg;
  });
};

const editCourse = async () => {
  editCourseLoading.value = true;

  const courseUpdate: UpdateCourse = {
    course_id: course.value!.id,
    name: newCourseName.value
  };
  await CourseService.updateCourse(courseUpdate).catch((err: any) => {
    console.log(err);
    deleteLoading.value = false;
    showDeleteCourse.value = false;
  });
  course.value!.name = newCourseName.value!;

  editCourseLoading.value = false;
  showEditCourse.value = false;
};
</script>
<template>
  <content-container>
    <template v-slot:header>
      <content-header :text='course?.name' link='/home' linkText='Zurück zur Kursauswahl'></content-header>
    </template>
    <template v-slot:content>
      <div class='flex gap-10 flex-1'>
        <div class='flex-1'>
          <subheader text='Aufgabengruppen'></subheader>
          <div class='flex justify-between gap-4 my-4'>
            <div class='flex gap-4'>
              <primary-button
                bgColor='bg-gray-400'
                class='w-64 h-10'
                name='Neue Aufgabengruppe'
                @click='showGroupModal = !showGroupModal'
              >
                <Icon class='mr-2' name='plus' weight='bold' />
              </primary-button>
            </div>
            <primary-button bgColor='bg-gray-600' class='w-52' fontWeight='font-medium' @click='showEditCourse = true'>
              <div class='flex items-center justify-center'>
                <Icon class='mr-1' height='18' name='pencil' width='18'></Icon>
                <div>Kurs bearbeiten</div>
              </div>
            </primary-button>
          </div>
          <div class='my-8'>
            <div v-if='loading' class='flex'>
              <skeleton-card
                v-for='i in 4'
                :key='i'
                :loading='loading'
                skeletonClasses='h-24 w-44 ml-4'
              ></skeleton-card>
            </div>
            <div v-else class='flex flex-wrap'>
              <div v-for='taskgroup in course?.task_groups' :key='taskgroup.short_name' class='ml-4 mb-4'>
                <course-admin-card
                  :taskgroup='taskgroup'
                  @deleteTaskgroup='deleteTaskgroup'
                  @editTaskgroup='editTaskgroup'
                ></course-admin-card>
              </div>
              <no-content v-if='course?.task_groups?.length === 0' text='Keine Aufgabengrupppen erstellt'></no-content>
            </div>
          </div>
        </div>
        <div class='flex flex-col'>
          <course-members :members='course?.members' class='pb-10' />
        </div>
      </div>
    </template>
  </content-container>

  <modal-dialog :show='showGroupModal'>
    <div class='relative'>
      <h1 class='text-2xl text-center'>Erstelle eine neue Aufgabengruppe</h1>
      <form class='w-full' @submit.prevent='onGroupSubmit'>
        <input-field
          v-model='fromGroupData.name'
          :errorMessage="taskGroupExists ? 'Es existiert bereits eine Gruppe mit diesem Namen' : ''"
          :required='true'
          class='w-96'
          label='Gruppenname'
          placeholder='Aufgabengruppe'
          tip='Gebe der Gruppe einen eindeutigen Namen'
          type='text'
        >
        </input-field>

        <confirm-buttons :loading='taskGroupLoading' reject-text='Abbrechen' @reject='onTaskGroupClose'
                         confirm-text='Speichern'></confirm-buttons>
      </form>
    </div>
  </modal-dialog>

  <modal-dialog :show='showEditCourse'>
    <div class='relative'>
      <h1 class='text-2xl'>Kurs bearbeiten</h1>

      <input-field v-model='newCourseName' label='Kursname' />

      <div class='border-2 m-2 px-4 rounded-lg border-red-800'>
        <div class='my-4 text-gray-200 font-bold text-red-400'>
          ACHTUNG - Alle zugehörigen Aufgabengruppen, Aufgaben und Lösungen werden gelöscht.
        </div>
        <input-field v-model='deleteCourseVerification' tip='Bitte den Namen des Kurses eingeben um ihn zu löschen' />

        <primary-button
          bgColor='bg-red-500'
          bgHoverColor='bg-red-700'
          class='mr-2 w-full my-5'
          fontWeight='font-normal'
          name='Kurs Löschen'
          @click.prevent='deleteCourse'
        ></primary-button>
      </div>
      <confirm-buttons :loading='editCourseLoading' reject-text='Abbrechen' @reject='showEditCourse = false'
                       confirm-text='Speichern' @confirm='editCourse'></confirm-buttons>
    </div>
  </modal-dialog>
  <!-- <modal-dialog :show="showEditCourse">
    <div class="relative">
      <h1 class="text-2xl">Möchtest du den Kurs wirklich löschen?</h1>
      <div class="my-4">
        Alle zugehörigen Aufgabengruppen, Aufgaben und Lösungen werden gelöscht.
      </div>

      <primary-button
        @click.prevent="showEditCourse = false"
        class="mr-2 w-full my-5"
        name="Kurs Löschen"
        bgColor="bg-red-500"
        bgHoverColor="bg-red-700"
        fontWeight="font-normal"
      ></primary-button>
      <div class="flex justify-end">
        <primary-button
          @click.prevent="showEditCourse = false"
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
          @click="deleteCourse"
          class="w-28"
        ></save-button>
      </div>
    </div>
  </modal-dialog> -->
</template>
