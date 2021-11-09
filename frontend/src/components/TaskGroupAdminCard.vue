<template>
  <skeleton-card class="min-w-40" :shouldHover="false">
    <div class="flex justify-end">
      <primary-button
        name="Öffnen"
        class="text-sm w-24"
        bgColor="bg-gray-400"
        @click="$router.push('/task/' + baseTask.short_name + '/admin')"
      >
        <template v-slot:rightIcon>
          <Icon name="caret-right" strokeWidth="24"></Icon>
        </template>
      </primary-button>
    </div>
    <div class="text-xl flex justify-between items-center">
      <div>
        {{ baseTask.name }}
      </div>
    </div>

    <task-count-badge :count="baseTask.task_count"></task-count-badge>
    <div class="flex mt-2 items-center">
      <div class="flex w-full">
        <div class="text-sm font-medium mr-4 w-20">
          <div v-if="baseTask.enabled" class="text-green-500 inline-block">Aktiviert</div>
          <div v-else class="text-red-400">Deaktiviert</div>
        </div>

        <toggle-button @changed="toggleEnabledState(baseTask)" :enabled="baseTask.enabled"> </toggle-button>
      </div>

      <div>
        <Icon
          name="trash"
          class="text-red-400 cursor-pointer ml-4 hover:text-red-500"
          weight="bold"
          @click.stop="$emit('deleteBaseTask')"
        ></Icon>
      </div>
    </div>

    <div class="flex justify-between items-center text-right text-sm font-semibold gap-4 mt-6">
      <save-button
        name="Zusammenfassung"
        bgColor="bg-gray-300"
        @click.stop="loadSummary(baseTask.short_name)"
        :loading="summaryDataLoading"
      ></save-button>

      <div
        class="
          transition
          hover:ring-2
          ring-white
          bg-gray-500
          hover:bg-gray-400
          p-2
          rounded-lg
          cursor-pointer
          inline-block
        "
        @click.stop="downloadUserSolutions(baseTask.short_name)"
      >
        <Icon name="download-simple" v-if="!downloadUserSolutionsLoading" />
        <spinner v-else></spinner>
      </div>
    </div>
  </skeleton-card>

  <modal-dialog :show="showSummaryModal" customClasses="w-2/3 max-h-[70vh]">
    <div class="flex justify-between items-center">
      <div class="text-3xl mt-4 font-semibold">Zusammenfassung Aufgabenbearbeitung</div>
      <primary-button class="w-12" bgColor="self-end bg-gray-500" @click="showSummaryModal = false">
        <Icon name="x"></Icon>
      </primary-button>
    </div>

    <div class="mt-8 max-h-[50vh]" v-if="summaryData?.tasks.length !== 0">
      <div class="w-full overflow-auto max-h-[50vh] pb-4">
        <div
          class="
            flex
            items-center
            justify-between
            text-center
            sticky
            top-0
            z-20
            font-bold
            text-lg text-gray-200
            bg-gray-800
            flex-1
            min-w-full
            w-fit-content
          "
        >
          <div class="w-48 flex-shrink-0 sticky left-0 top-0 z-10 p-4 bg-gray-800">Name</div>
          <div
            class="w-full flex justify-center sticky top-0 min-w-[200px] p-4"
            v-for="(task, index) of summaryData?.tasks"
            :key="task"
          >
            <span :id="'task-' + index">{{ task.substring(0, 12) + (task.length > 12 ? '...' : '') }}</span>
          </div>
        </div>

        <div
          class="flex justify-between items-center text-center rounded-lg min-w-full w-fit-content"
          v-for="(row, index) in summaryData?.rows"
          :key="index"
          :class="index % 2 == 0 ? 'bg-gray-700' : 'bg-gray-800'"
        >
          <div
            class="w-48 flex-shrink-0 sticky left-0 py-2 z-10 font-semibold"
            :class="index % 2 == 0 ? 'bg-gray-700' : 'bg-gray-800'"
          >
            {{ row.user.lastname }}, {{ row.user.firstname }} {{ row.user.middlename }}
          </div>
          <div
            class="w-full flex justify-center items-center my-2 min-w-[200px]"
            v-for="(taskvalue, index) of row.summary"
            :key="index"
          >
            <Icon name="check-circle" width="34" height="34" class="text-green-400" v-if="taskvalue == 1"></Icon>
            <Icon name="x-circle" width="34" height="34" class="text-red-500" v-else-if="taskvalue == -1"></Icon>
            <Icon name="circle" width="34" height="34" class="text-gray-500" v-else></Icon>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="mt-12"><no-content text="Keine Zusammenfassung verfügbar"></no-content></div>
  </modal-dialog>
</template>
<script lang="ts">
import { BaseTask } from '../model/baseTask';
import { defineComponent, nextTick, onUnmounted, PropType, ref } from 'vue';
import { MembersolutionSummary } from '../model/membersolutionSummary';
import { TooltipGenerator } from '../utils/tooltip-generator';
import { TaskService } from '../services/task.service';

export default defineComponent({
  props: {
    baseTask: Object as PropType<BaseTask>
  },

  emits: ['deleteBaseTask'],

  setup(props) {
    const showSummaryModal = ref<Boolean>(false);
    const summaryData = ref<MembersolutionSummary>();
    const summaryDataLoading = ref<Boolean>(false);

    const downloadUserSolutionsLoading = ref(false);

    const toggleEnabledState = async (baseTask: BaseTask) => {
      props.baseTask!.enabled = !props.baseTask!.enabled;

      await TaskService.updateBaseTask({ base_task_id: baseTask.id, enabled: baseTask.enabled });
    };

    const downloadUserSolutions = async (short_name: string) => {
      downloadUserSolutionsLoading.value = true;
      const data = await TaskService.downloadUserSolutionsToBaseTask(short_name);
      const a = document.createElement('a');

      const blob = new Blob([data], { type: 'application/xlsx' });

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

    return {
      showSummaryModal,
      summaryData,
      summaryDataLoading,
      loadSummary,
      toggleEnabledState,
      downloadUserSolutions,
      downloadUserSolutionsLoading
    };
  }
});
</script>
<style></style>
