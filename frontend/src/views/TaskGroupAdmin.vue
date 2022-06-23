<script lang='ts' setup>
import { onMounted, reactive, ref } from 'vue';
import { BaseTask } from '../model/task/baseTask';
import { TaskGroup } from '../model/task/taskGroup';
import { useRoute } from 'vue-router';
import { TaskGroupService } from '../services/task-group.service';
import { Slide } from '../model/slide';
import { TaskService } from '../services/task.service';
import router from '../router';
import { TaskImageService } from '../services/task-image.service';
import RoleOnly from '../components/containers/RoleOnly.vue';
import ModalDialog from '../components/containers/ModalDialog.vue';
import PrimaryButton from '../components/general/PrimaryButton.vue';
import MultiImageUpload from '../components/form/MultiImageUpload.vue';
import Icon from '../components/general/Icon.vue';
import SlideSelect from '../components/slide/SlideSelect.vue';
import InputField from '../components/form/InputField.vue';
import ContentContainer from '../components/containers/ContentContainer.vue';
import TaskGroupAdminCard from '../components/TaskGroupAdminCard.vue';
import NoContent from '../components/NoContent.vue';
import ContentHeader from '../components/ContentHeader.vue';
import ConfirmButtons from '../components/general/ConfirmButtons.vue';

const uploadImages = ref<{ fileUrl: string; file: File }[]>([]);

const showDeleteBaseTask = ref<Boolean>(false);
const deleteBaseLoading = ref<Boolean>(false);
const deleteBaseTaskItem = ref<BaseTask>();

const showModal = ref<Boolean>(false);

const taskGroup = ref<TaskGroup>();

const route = useRoute();

const formData = reactive<{
  name: string;
  slide_id: string;
  csv_file: File | undefined;
}>({
  name: '',
  slide_id: '',
  csv_file: undefined
});

const uploadProgress = ref(0.0);

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

const onFileUpload = (event: any) => {
  formData.csv_file = event.target.files[0];
};

const onSubmit = async () => {
  taskLoading.value = true;

  if (formData.csv_file && uploadImages.value.length !== 0) {
    const images = await uploadMultipleImages(uploadImages.value);

    try {
      const response = await TaskService.createBaseTaskFromCsv(
        {
          name: formData.name,
          slide_id: formData.slide_id,
          course_id: taskGroup.value?.course_id as number,
          task_group_id: taskGroup.value?.id
        },
        formData.csv_file,
        images
      );

      taskGroup.value?.tasks.push(response);

      taskLoading.value = false;
      showModal.value = false;
    } catch (e) {
      // for await (const img of images) {
      //   await TaskService.deleteTaskImage(img.path.split('/')[1]);
      // }
      taskLoading.value = false;
    }
  } else {
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
  }
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

const setUploadImages = (images: { fileUrl: string; file: File }[]) => {
  uploadImages.value = images;
};

const uploadMultipleImages = async (images: { fileUrl: string; file: File }[]) => {
  const formData = new FormData();
  for (const image of images) {
    formData.append('images', image.file);
    formData.append('names', image.file.name);
  }
  return await TaskImageService.uploadMultipleTaskImages(formData, (event) => {
    uploadProgress.value = Math.round((100 * event.loaded) / event.total);
  });
};

const editTask = (task: BaseTask) => {
  taskGroup.value!.tasks = taskGroup.value!.tasks.map((baseTask) => {
    if (baseTask.id === task.id) {
      baseTask.name = task.name;
    }
    return baseTask;
  });
};
</script>
<template class='relative'>
  <content-container>
    <template v-slot:header>
      <content-header
        :link='`/course/${taskGroup?.course_short_name}/admin`'
        :text='taskGroup?.name'
        linkText='Zurück zum Kurs'
      ></content-header>
    </template>
    <template v-slot:content>
      <div class='flex justify-between items-center'>
        <div class='w-full text-xl font-bold text-gray-200 uppercase'>Deine Aufgaben</div>
      </div>
      <div class='my-4 flex justify-between'>
        <primary-button bgColor='bg-gray-400' class='w-48 h-10' name='Neue Aufgabe' @click='showModal = !showModal'>
          <Icon class='mr-2' name='plus' weight='bold' />
        </primary-button>
        <primary-button
          bgColor='bg-gray-700'
          class='w-56'
          fontWeight='font-medium'
          name='Aufgabengruppe löschen'
          textColor='text-red-400'
          @click='showTaskgroupDelete = true'
        ></primary-button>
      </div>

      <div class='flex flex-wrap my-8'>
        <no-content v-if='taskGroup?.tasks.length === 0' text='Noch keine Aufgaben erstellt'></no-content>
        <div v-for='baseTask in taskGroup?.tasks' :key='baseTask.id' class='ml-4 mb-4'>
          <task-group-admin-card
            :baseTask='baseTask'
            @deleteBaseTask='
              showDeleteBaseTask = true;
              deleteBaseTaskItem = baseTask;
            '
            @editBaseTask='editTask'
          ></task-group-admin-card>
        </div>
      </div>
    </template>
  </content-container>

  <modal-dialog :show='showModal' customClasses='max-w-[50%] min-w-[30rem]'>
    <div class='relative'>
      <h1 class='text-2xl text-center'>Erstelle eine neue Aufgabe</h1>
      <form class='w-full' @submit.prevent='onSubmit'>
        <input-field
          v-model='formData.name'
          :errorMessage="taskError ? 'Es gibt bereits eine Aufgabe mit diesem Namen' : ''"
          :required='true'
          class='w-full'
          label='Aufgabenname'
          placeholder='Markiere alle ...'
          tip='Gebe der Aufgabe einen eindeutigen Namen'
          type='text'
        >
        </input-field>
        <slide-select @slideChanged='setSlide($event)'></slide-select>

        <div>
          <div>
            <div>Aufgaben aus einer CSV-Datei generieren (optional):</div>
            <div class='flex items-center my-4'>
              <label class='cursor-pointer flex justify-center bg-gray-500 w-56 rounded-lg py-1' for='slide-upload'>
                <Icon class='mr-2' name='cloud-arrow-up' />
                <span>CSV-Datei auswählen</span>
              </label>
              <div v-if='formData.csv_file' class='ml-4'>
                {{ formData.csv_file.name }}
              </div>
            </div>
            <input id='slide-upload' accept='.csv' class='hidden' type='file' @change='onFileUpload' />
          </div>

          <div v-if='formData.csv_file'>
            <MultiImageUpload
              label='Füge die entsprechenden Bilder der CSV-Datei hinzu:'
              @images-dropped='setUploadImages'
            >
            </MultiImageUpload>
          </div>
        </div>
        <div v-if='taskLoading'>
          <div class='flex gap-3 mb-3 items-center'>
            <div class='flex-1'>
              <div
                :style="{
                  width: uploadProgress + '%'
                }"
                class='animate-pulse bg-green-500 my-2 rounded-lg transition duration-10 h-3'
              ></div>
            </div>
            <div>{{ uploadProgress }}%</div>
          </div>
          <div v-if='uploadProgress === 100.0' class='font-semibold'>Aufgaben werden erstellt...</div>
        </div>

        <confirm-buttons :loading='taskLoading' reject-text='Abbrechen' @reject='onTaskClose'
                         confirm-text='Speichern'></confirm-buttons>
      </form>
    </div>
  </modal-dialog>

  <modal-dialog :show='showTaskgroupDelete'>
    <div class='relative'>
      <h1 class='text-2xl'>Möchtest du die Aufgabengruppe löschen?</h1>
      <div class='my-4'>Alle zugehörigen Aufgaben und Lösungen werden gelöscht.</div>
      <confirm-buttons :loading='deleteLoading' @reject='showTaskgroupDelete = false'
                       @confirm='deleteTaskGroup'></confirm-buttons>
    </div>
  </modal-dialog>

  <role-only>
    <modal-dialog :show='showDeleteBaseTask'>
      <div class='relative'>
        <h1 class='text-2xl'>Möchtest du die Aufgabe löschen?</h1>
        <div class='my-4'>Alle Aufgaben und Lösungen werden gelöscht.</div>
        <confirm-buttons :loading='deleteBaseLoading' @reject='showDeleteBaseTask = false' @confirm='deleteBaseTask'>
        </confirm-buttons>
      </div>
    </modal-dialog>
  </role-only>
</template>
