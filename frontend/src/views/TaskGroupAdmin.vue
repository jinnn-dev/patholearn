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
          <task-group-admin-card
            :baseTask="baseTask"
            @deleteBaseTask="
              showDeleteBaseTask = true;
              deleteBaseTaskItem = baseTask;
            "
          ></task-group-admin-card>
        </div>
      </div>
    </template>
  </content-container>

  <modal-dialog :show="showModal" customClasses="max-w-[50%]">
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
          class="w-full"
          :errorMessage="taskError ? 'Es gibt bereits eine Aufgabe mit diesem Namen' : ''"
        >
        </input-field>
        <slide-select @slideChanged="setSlide($event)"></slide-select>

        <div>
          <div>
            <div>Aufgaben aus einer CSV-Datei generieren (optional):</div>
            <div class="flex items-center my-4">
              <label for="slide-upload" class="cursor-pointer flex justify-center bg-gray-500 w-56 rounded-lg py-1">
                <Icon name="cloud-arrow-up" class="mr-2" />
                <span>CSV-Datei auswählen</span>
              </label>
              <div v-if="formData.csv_file" class="ml-4">{{ formData.csv_file.name }}</div>
            </div>
            <input class="hidden" id="slide-upload" type="file" accept=".csv" @change="onFileUpload" />
          </div>

          <div v-if="formData.csv_file">
            <div>Füge die entsprechenden Bilder der CSV-Datei hinzu:</div>

            <div class="max-h-[300px] overflow-auto mb-4">
              <div
                class="h-20 w-20 bg-gray-500 rounded-lg inline-block mx-2 my-2"
                v-for="(image, index) in tempPreviewImages"
                :key="image"
              >
                <HintImage :imgSrc="image" @click="deleteImage(index)" />
              </div>
              <div
                class="
                  h-20
                  w-20
                  mx-2
                  my-2
                  bg-highlight-900
                  rounded-lg
                  flex
                  items-center
                  justify-center
                  cursor-pointer
                  hover:bg-highlight-800
                  transition
                "
                @click="fileRef?.click()"
              >
                <Icon name="plus" width="30" height="30" stroke-width="25" />
              </div>
            </div>
          </div>
          <input type="file" ref="fileRef" v-show="false" @change="onFileChange($event)" multiple="multiple" />
        </div>
        <div class="flex justify-end w-full">
          <primary-button
            @click.prevent="onTaskClose"
            class="mr-2 w-32"
            name="Abbrechen"
            bgColor="bg-gray-500"
            bgHoverColor="bg-gray-700"
            fontWeight="font-normal"
          ></primary-button>
          <save-button class="w-48" name="Speichern" type="submit" :loading="taskLoading"></save-button>
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
import { defineComponent, nextTick, onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';
import { TaskGroup } from '../model/taskGroup';
import { Slide } from '../model/slide';
import { BaseTask } from '../model/baseTask';
import { TaskService } from '../services/task.service';
import { TaskGroupService } from '../services/task-group.service';
import router from '../router';
import { showSolution } from 'components/viewer/core/viewerState';

export default defineComponent({
  setup() {
    const fileRef = ref<HTMLInputElement>();
    const tempPreviewImages = ref<string[]>([]);
    const tempImages = ref<File[]>([]);
    const noImageSelectedError = ref(false);

    const showDeleteBaseTask = ref<Boolean>(false);
    const deleteBaseLoading = ref<Boolean>(false);
    const deleteBaseTaskItem = ref<BaseTask>();

    const showModal = ref<Boolean>(false);

    const taskGroup = ref<TaskGroup>();

    const route = useRoute();

    const formData = reactive<{ name: string; slide_id: string; csv_file: File | undefined }>({
      name: '',
      slide_id: '',
      csv_file: undefined
    });

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

    const onFileUpload = (event) => {
      console.log(event.target.files[0]);

      formData.csv_file = event.target.files[0];
    };

    const onSubmit = async () => {
      taskLoading.value = true;
      if (formData.csv_file && tempImages.value.length !== 0) {
        const images = await uploadMultipleImages(tempImages.value);

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

    function deleteImage(imageIndex: number) {
      tempPreviewImages.value.splice(imageIndex, 1);
      tempImages.value.splice(imageIndex, 1);
    }

    function onFileChange(e: any) {
      const files = e.target.files || e.dataTransfer.files;
      noImageSelectedError.value = false;

      if (!files.length) return;
      const names = [];
      for (const file of files) {
        tempPreviewImages.value.push(URL.createObjectURL(file));
        tempImages.value.push(file);
        names.push(file.name);
      }
      console.log(names.sort());
    }

    const uploadImage = async (image: Blob) => {
      const formData = new FormData();
      formData.append('image', image);
      return await TaskService.uploadTaskImage(formData);
    };

    const uploadMultipleImages = async (images: Blob[]) => {
      const formData = new FormData();
      for (const image of images) {
        formData.append('images', image);
      }
      return await TaskService.uploadMultipleTaskImages(formData);
    };

    return {
      taskGroup,
      showModal,
      formData,
      taskLoading,
      fileRef,
      taskError,
      showTaskgroupDelete,
      deleteLoading,
      deleteImage,
      tempPreviewImages,
      onTaskClose,
      deleteTaskGroup,
      onSubmit,
      onFileChange,
      tempImages,
      setSlide,
      showDeleteBaseTask,
      deleteBaseLoading,
      deleteBaseTaskItem,
      onFileUpload,
      deleteBaseTask
    };
  }
});
</script>

<style></style>
