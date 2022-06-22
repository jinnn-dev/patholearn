<script lang='ts' setup>
import { onClickOutside } from '@vueuse/core';
import { nextTick, PropType, ref } from 'vue';
import { SLIDE_IMAGE_URL } from '../config';
import { BaseTask, UpdateBaseTask } from '../model/baseTask';
import { ImageSelectStatistic } from '../model/imageSelectStatistic';
import { MembersolutionSummary } from '../model/membersolutionSummary';
import { TaskService } from '../services/task.service';
import { TooltipGenerator } from '../utils/tooltips/tooltip-generator';
import ModalDialog from './containers/ModalDialog.vue';
import SaveButton from './general/SaveButton.vue';
import PrimaryButton from './general/PrimaryButton.vue';
import InputField from './form/InputField.vue';
import NoContent from './NoContent.vue';
import LazyImage from './LazyImage.vue';
import Icon from './general/Icon.vue';
import SkeletonCard from './containers/SkeletonCard.vue';
import Spinner from './Spinner.vue';
import ToggleButton from './form/ToggleButton.vue';
import TaskCountBadge from './TaskCountBadge.vue';
import DotMenu from './DotMenu.vue';

const props = defineProps({
  baseTask: Object as PropType<BaseTask>
});

const emit = defineEmits(['deleteBaseTask', 'editBaseTask']);

const openDotMenu = ref(false);
const showEditTask = ref(false);
const editTaskLoading = ref(false);
const newTaskName = ref(props.baseTask!.name);

const showSummaryModal = ref<Boolean>(false);
const summaryData = ref<MembersolutionSummary>();
const summaryDataLoading = ref<Boolean>(false);
const downloadUserSolutionsLoading = ref(false);
const showStatisticSummary = ref(false);
const imageSelectStatistic = ref<ImageSelectStatistic>();
const statisticDataLoading = ref(false);
const taskDetailLoading = ref(false);
const toggleEnabledState = async (baseTask: BaseTask) => {
  props.baseTask!.enabled = !props.baseTask!.enabled;
  await TaskService.updateBaseTask({
    base_task_id: baseTask.id,
    enabled: baseTask.enabled
  });
};
const downloadUserSolutions = async (short_name: string) => {
  downloadUserSolutionsLoading.value = true;
  const data = await TaskService.downloadUserSolutionsToBaseTask(short_name);
  const a = document.createElement('a');
  const blob = new Blob([data], {
    type: 'application/xlsx'
  });
  downloadUserSolutionsLoading.value = false;
  a.href = window.URL.createObjectURL(blob);
  a.download = short_name + '.xlsx';
  a.style.display = 'none';
  document.body.appendChild(a);
  a.click();
};
const loadSummary = async (short_name: string) => {
  summaryDataLoading.value = true;
  summaryData.value = await TaskService.getMembersolutionSummary(short_name);
  summaryDataLoading.value = false;
  showSummaryModal.value = true;
  nextTick(() => {
    if (summaryData.value) {
      for (const [index, task] of summaryData.value.tasks.entries()) {
        TooltipGenerator.addGeneralTooltip({
          target: '#task-' + index,
          content: task,
          placement: 'top'
        });
      }
    }
  });
};
const loadTaskDetails = async (short_name: string) => {
  statisticDataLoading.value = true;
  showStatisticSummary.value = true;
  taskDetailLoading.value = true;
  imageSelectStatistic.value = await TaskService.getBaseTaskStatistics(short_name);
  taskDetailLoading.value = false;
};

const closeStatisticModal = () => {
  showStatisticSummary.value = false;
};

const editBaseTask = async () => {
  editTaskLoading.value = true;

  const updateBaseTask: UpdateBaseTask = {
    base_task_id: props.baseTask!.id,
    name: newTaskName.value
  };

  if (updateBaseTask.name !== props.baseTask?.name) {
    await TaskService.updateBaseTask(updateBaseTask);
  }
  props.baseTask!.name = newTaskName.value;
  emit('editBaseTask', props.baseTask);
  showEditTask.value = false;
  editTaskLoading.value = false;
  openDotMenu.value = false;
};

const target = ref(null);

onClickOutside(target, () => (openDotMenu.value = false));
</script>
<template>
  <skeleton-card :shouldHover='false' class='min-w-40 relative'>
    <div class='flex items-center'>
      <div class='flex-1 text-xl'>
        {{ baseTask.name }}
      </div>
      <div class='flex justify-end ml-5'>
        <Icon
          class='ring-white hover:ring-2 rounded-md transition-all cursor-pointer'
          name='dots-three-vertical'
          @click.stop='openDotMenu = !openDotMenu'
        ></Icon>
      </div>
      <dot-menu ref='target' :optionsOpen='openDotMenu' @delete="$emit('deleteBaseTask')" @edit='showEditTask = true' />
    </div>

    <task-count-badge :count='baseTask.task_count'></task-count-badge>
    <div class='flex mt-2 items-center'>
      <div class='flex w-full items-center'>
        <div class='text-sm font-medium mr-4 w-20'>
          <div v-if='baseTask.enabled' class='text-green-500 inline-block'>Aktiviert</div>
          <div v-else class='text-red-400'>Deaktiviert</div>
        </div>

        <toggle-button :enabled='baseTask.enabled' @changed='toggleEnabledState(baseTask)'></toggle-button>
      </div>
    </div>

    <div class='flex justify-between items-center text-right text-sm font-semibold gap-4 mt-6'>
      <save-button
        :loading='summaryDataLoading'
        bgColor='bg-gray-300 w-48'
        name='Zusammenfassung'
        @click.stop='loadSummary(baseTask.short_name)'
      ></save-button>

      <div
        class='transition hover:ring-2 ring-white bg-gray-500 hover:bg-gray-400 p-2 rounded-lg cursor-pointer inline-block'
        @click.stop='downloadUserSolutions(baseTask.short_name)'
      >
        <Icon v-if='!downloadUserSolutionsLoading' name='download-simple' />
        <spinner v-else></spinner>
      </div>

      <div
        class='transition hover:ring-2 ring-white bg-gray-500 hover:bg-gray-400 p-2 rounded-lg cursor-pointer inline-block'
        @click.stop='loadTaskDetails(baseTask?.short_name)'
      >
        <Icon v-if='!taskDetailLoading' name='chart-bar' />
        <spinner v-else></spinner>
      </div>
      <primary-button
        bgColor='bg-gray-400'
        class='text-sm w-24'
        name='Öffnen'
        @click="$router.push('/task/' + baseTask.short_name + '/admin')"
      >
        <template v-slot:rightIcon>
          <Icon name='caret-right' strokeWidth='24'></Icon>
        </template>
      </primary-button>
    </div>
  </skeleton-card>

  <modal-dialog :show='showSummaryModal' customClasses='w-2/3 max-h-[70vh]'>
    <div class='flex justify-between items-center'>
      <div class='text-3xl mt-4 font-semibold'>Zusammenfassung Aufgabenbearbeitung</div>
      <primary-button bgColor='self-end bg-gray-500' class='w-12' @click='showSummaryModal = false'>
        <Icon name='x'></Icon>
      </primary-button>
    </div>

    <div v-if='summaryData?.tasks.length !== 0' class='mt-8 max-h-[50vh]'>
      <div class='w-full overflow-auto max-h-[50vh] pb-4'>
        <div
          class='flex items-center justify-between text-center sticky top-0 z-20 font-bold text-lg text-gray-200 bg-gray-800 flex-1 min-w-full w-fit-content'
        >
          <div class='w-48 flex-shrink-0 sticky left-0 top-0 z-10 p-4 bg-gray-800'>Name</div>
          <div
            v-for='(task, index) of summaryData?.tasks'
            :key='task'
            class='w-full flex justify-center sticky top-0 min-w-[200px] p-4'
          >
            <span :id="'task-' + index">{{ task.substring(0, 12) + (task.length > 12 ? '...' : '') }}</span>
          </div>
        </div>

        <div
          v-for='(row, index) in summaryData?.rows'
          :key='index'
          :class="index % 2 === 0 ? 'bg-gray-700' : 'bg-gray-800'"
          class='flex justify-between items-center text-center rounded-lg min-w-full w-fit-content'
        >
          <div
            :class="index % 2 === 0 ? 'bg-gray-700' : 'bg-gray-800'"
            class='w-48 flex-shrink-0 sticky left-0 py-2 z-10 font-semibold'
          >
            {{ row.user.lastname }},
            {{ row.user.firstname }}
            {{ row.user.middlename }}
          </div>
          <div
            v-for='(taskvalue, index) of row.summary'
            :key='index'
            class='w-full flex justify-center items-center my-2 min-w-[200px]'
          >
            <Icon v-if='taskvalue === 1' class='text-green-400' height='34' name='check-circle' width='34'></Icon>
            <Icon v-else-if='taskvalue === -1' class='text-red-500' height='34' name='x-circle' width='34'></Icon>
            <Icon v-else class='text-gray-500' height='34' name='circle' width='34'></Icon>
          </div>
        </div>
      </div>
    </div>
    <div v-else class='mt-12'>
      <no-content text='Keine Zusammenfassung verfügbar'></no-content>
    </div>
  </modal-dialog>

  <modal-dialog :show='showStatisticSummary' customClasses='max-w-[50%]'>
    <div
      v-if='
        imageSelectStatistic &&
        (imageSelectStatistic?.wrong_image_statistics?.length !== 0 ||
          imageSelectStatistic?.wrong_label_statistics?.length !== 0)
      '
      class='mb-6 w-full'
    >
      <div>
        <div class='text-lg font-semibold mb-4'>Die Top 5 der am meisten falsch klassifizierten Bilder:</div>

        <div class='flex justify-center items-center gap-4 w-full flex-wrap'>
          <div
            v-for='statistic in imageSelectStatistic?.wrong_image_statistics'
            :key='statistic.task_image_id'
            class='flex flex-col justify-center items-center gap-2'
          >
            <lazy-image
              :imageUrl="SLIDE_IMAGE_URL + '/task-images/' + statistic.task_image_id + '.png'"
              class='w-32'
            ></lazy-image>
            <div class='text-center'>
              <div class='text-lg font-bold'>{{ statistic.amount }}x</div>
              <div>
                {{ statistic.name }}
              </div>
              <div class='font-semibold text-gray-300'>
                {{ statistic.label }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class='mt-8'>
        <div class='text-lg font-semibold mb-4'>Die Top 5 der am meisten falsch erkannten Klassen:</div>

        <div v-if='Object.keys(imageSelectStatistic?.wrong_label_statistics).length !== 0'>
          <div class='flex justify-center gap-4 w-full flex-wrap'>
            <div
              v-for='statistic in imageSelectStatistic?.wrong_label_statistics'
              :key='statistic.label'
              class='flex flex-col items-center gap-2 bg-gray-700 p-2 rounded-lg'
            >
              <div class='font-semibold text-lg'>
                {{ statistic.label }}
              </div>
              <div class='w-full'>
                <div v-for='detail in statistic.detail' :key='detail.label' class='flex justify-between'>
                  <div class='mr-2'>
                    {{ detail.label }}
                  </div>
                  <div>{{ detail.amount }}x</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else>
          <no-content text='Keine Statistik vorhanden'></no-content>
        </div>
      </div>
    </div>

    <div v-else class='mb-6'>
      <no-content text='Keine Statistik vorhanden'></no-content>
    </div>

    <div class='flex justify-end'>
      <primary-button
        bgColor='bg-gray-500'
        bgHoverColor='bg-gray-700'
        class='mr-2 w-28'
        fontWeight='font-normal'
        name='Schließen'
        @click.stop='closeStatisticModal'
      ></primary-button>
    </div>
  </modal-dialog>
  <modal-dialog :show='showEditTask'>
    <div class='relative min-w-[20rem]'>
      <h1 class='text-2xl'>Aufgaben bearbeiten</h1>
      <InputField v-model='newTaskName' label='Neuer Name'></InputField>
      <div class='flex justify-end'>
        <primary-button
          bgColor='bg-gray-500'
          bgHoverColor='bg-gray-700'
          class='mr-2 w-28'
          fontWeight='font-normal'
          name='Abbrechen'
          @click.prevent='showEditTask = false'
        ></primary-button>
        <save-button
          :loading='editTaskLoading'
          class='w-32'
          name='Speichern'
          type='submit'
          @click='editBaseTask'
        ></save-button>
      </div>
    </div>
  </modal-dialog>
</template>
