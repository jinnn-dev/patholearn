<template>
  <router-link :to="'/task/' + baseTask.short_name + '/admin'">
    <skeleton-card class="min-w-40">
      <div class="text-xl flex justify-between items-center">
        <div>
          {{ baseTask.name }}
        </div>
        <div>
          <Icon
            name="trash"
            class="text-red-400 cursor-pointer ml-4 hover:text-red-500"
            weight="bold"
            @click.prevent="$emit('deleteBaseTask')"
          ></Icon>
        </div>
      </div>

      <task-count-badge :count="baseTask.task_count"></task-count-badge>
      <div class="flex mt-2 items-center">
        <div class="w-24 text-sm font-medium">
          <div v-if="baseTask.enabled" class="text-green-500">Aktiviert</div>
          <div v-else class="text-red-400">Deaktiviert</div>
        </div>
        <button
          @click.prevent="toggleEnabledState(baseTask)"
          type="button"
          class="
            bg-gray-300
            relative
            inline-flex
            flex-shrink-0
            h-6
            w-11
            border-2 border-transparent
            rounded-full
            cursor-pointer
            transition-colors
            ease-in-out
            duration-200
            focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500
          "
          role="switch"
          aria-checked="false"
          :class="baseTask.enabled ? 'bg-green-500' : 'bg-gray-400'"
        >
          <span
            aria-hidden="true"
            class="
              pointer-events-none
              inline-block
              h-5
              w-5
              rounded-full
              bg-gray-100
              shadow
              transform
              ring-0
              transition
              ease-in-out
              duration-200
            "
            :class="baseTask.enabled ? 'translate-x-5' : 'translate-x-0'"
          ></span>
        </button>
      </div>
      <div class="flex justify-between items-center text-right text-sm font-semibold mt-8">
        <save-button
          name="Zusammenfassung"
          bgColor="bg-gray-300"
          @click.prevent="loadSummary(baseTask.short_name)"
          :loading="summaryDataLoading"
        ></save-button>
      </div>
    </skeleton-card>
  </router-link>

  <modal-dialog :show="showSummaryModal" customClasses="w-2/3 max-h-[70vh]">
    <div class="flex justify-between items-center">
      <div class="text-xl mt-4 font-semibold">Zusammenfassung Aufgabenbearbeitung</div>
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
            <span :id="'task-' + index">{{ task.substring(0, 12) + '...' }}</span>
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
            {{ row.user.firstname }} {{ row.user.middlename }} {{ row.user.lastname }}
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

      <!-- <table class="table-fixed relative w-full">
        <thead class="relative block">
          <tr class="w-full">
            <th class="w-32">Name</th>
            <th class="w-auto" v-for="task of summaryData.tasks" :key="task">
              {{ task }}
            </th>
          </tr>
        </thead>
      </table> -->
    </div>

    <div v-else><no-content text="Keine Zusammenfassung verfügbar"></no-content></div>
  </modal-dialog>
</template>
<script lang="ts">
import { BaseTask } from '../model/baseTask';
import { defineComponent, nextTick, PropType, ref } from 'vue';
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

    const toggleEnabledState = async (baseTask: BaseTask) => {
      props.baseTask!.enabled = !props.baseTask!.enabled;

      await TaskService.updateBaseTask({ base_task_id: baseTask.id, enabled: baseTask.enabled });
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
    return { showSummaryModal, summaryData, summaryDataLoading, loadSummary, toggleEnabledState };
  }
});
</script>
<style></style>
