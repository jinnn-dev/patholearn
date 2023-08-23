<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useService } from '../../../composables/useService';
import { CourseService } from '../../../services/course.service';
import { TaskGroupService } from '../../../services/task-group.service';
import { TaskService } from '../../../services/task.service';
import Icon from '../../../components/general/Icon.vue';
import { Course } from '../../../model/course';
import { TaskGroup } from '../../../model/task/taskGroup';
import { BaseTask } from '../../../model/task/baseTask';
import { Task } from '../../../model/task/task';
import Spinner from '../../../components/general/Spinner.vue';
import { PatchSize, PatchMagnification } from '../../../model/ai/datasets/dataset';
const { result, loading: coursesLoading, run: getCourses } = useService(CourseService.getAllCoursesToUser, true);
const {
  result: taskGroups,
  loading: taskGroupsLoading,
  run: getTaskGroups
} = useService(TaskGroupService.getTaskGroups);
const { result: taskGroup, loading: taskGroupLoading, run: getTaskGroup } = useService(TaskGroupService.getTaskGroup);
const { result: baseTask, loading: baseTaskLoading, run: getBaseTask } = useService(TaskService.getBaseTask);

const selectedPatchSize = ref<PatchSize>(256);
const selectedPatchMagnification = ref<PatchMagnification>(1.0);

const selectedTasks = ref<{ course: Course; taskGroup: TaskGroup; baseTask: BaseTask; task: Task }[]>([]);

const selectedCourse = ref<Course>();
const selectedTaskGroup = ref<TaskGroup>();
const selectedBaseTask = ref<BaseTask>();

const emit = defineEmits(['tasksChanged', 'patchSizeChanged', 'patchMagnificationChanged']);

const patchSizeChanged = (size: PatchSize) => {
  emit('patchSizeChanged', size);
  selectedPatchSize.value = size;
};

const patchMagnificationChanged = (magnification: PatchMagnification) => {
  emit('patchMagnificationChanged', magnification);
  selectedPatchMagnification.value = magnification;
};

const goToCourse = async (course: Course) => {
  selectedCourse.value = course;
  await getTaskGroups(selectedCourse.value.id);
};

const goToTaskGroup = async (taskGroup: TaskGroup) => {
  selectedTaskGroup.value = taskGroup;
  await getTaskGroup(taskGroup.short_name);
};

const goToBaseTask = async (baseTask: BaseTask) => {
  selectedBaseTask.value = baseTask;
  await getBaseTask(baseTask.short_name);
};

const taskSelected = async (task: Task) => {
  const taskIndex = selectedTasks.value.findIndex((selectedTask) => selectedTask.task.id === task.id);
  if (taskIndex > -1) {
    selectedTasks.value.splice(taskIndex, 1);
  } else {
    selectedTasks.value.push({
      course: selectedCourse.value!,
      taskGroup: selectedTaskGroup.value!,
      baseTask: selectedBaseTask.value!,
      task: task
    });
  }
  emit('tasksChanged', selectedTasks.value);
};

const isSelected = (task: Task) => {
  return selectedTasks.value.find((selectedTask) => selectedTask.task.id === task.id) !== undefined;
};

const goBackToCourses = async () => {
  await getCourses();
  selectedCourse.value = undefined;
  selectedTaskGroup.value = undefined;
  selectedBaseTask.value = undefined;
};

const goBackToTaskGroups = async () => {
  await getTaskGroups(selectedCourse.value!.id);
  selectedTaskGroup.value = undefined;
  selectedBaseTask.value = undefined;
};

const goBackToBaseTask = async () => {
  await getTaskGroup(selectedTaskGroup.value!.short_name);
  selectedBaseTask.value = undefined;
};

const removeSelectedTask = (index: number) => {
  selectedTasks.value.splice(index, 1);
};

// const annotationGroupsEqual = computed(() => {
//   let isEqual = true;
//   for (const selectedTask of selectedTasks.value) {
//     for (const selectedTaskTwo of selectedTasks.value) {
//       if (!_.isEqual(selectedTask.task.annotation_groups, selectedTaskTwo.task.annotation_groups)) {
//         isEqual = false;
//       }
//     }
//   }
//   return isEqual;
// });
</script>
<template>
  <div>
    <div class="text-xl mb-4">3. Create a dataset from tasks in PathoLearn</div>
    <div>
      <div class="text-lg">Selected tasks:</div>
      <div class="text-gray-300" v-if="selectedTasks.length === 0">No tasks selected</div>
      <div v-else>
        <div class="flex flex-wrap gap-4 mt-4">
          <div
            v-for="(selectedTask, index) in selectedTasks"
            class="flex items-center gap-2 bg-gray-700 ring-1 ring-gray-500 rounded-md px-4 py-2"
          >
            <div>{{ selectedTask.course.name }}</div>
            <icon name="caret-right" size="16"></icon>
            <div>{{ selectedTask.taskGroup.name }}</div>
            <icon name="caret-right" size="16"></icon>
            <div>{{ selectedTask.baseTask.name }}</div>
            <icon name="caret-right" size="16"></icon>
            <div>{{ selectedTask.task.task_question }}</div>
            <icon class="cursor-pointer text-red-500" name="trash" @click.stop="removeSelectedTask(index)"></icon>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-4">
      <div class="text-lg">Tasks:</div>

      <div class="flex items-center gap-2 mt-4">
        <div @click="goBackToCourses()" class="cursor-pointer">Courses</div>
        <div v-if="selectedCourse" class="flex items-center gap-2">
          <icon name="caret-right" size="16"></icon>
          <div @click="goBackToTaskGroups" class="cursor-pointer">{{ selectedCourse.name }}</div>
        </div>
        <div v-if="selectedTaskGroup" class="flex items-center gap-2">
          <icon name="caret-right" size="16"></icon>
          <div @click="goBackToBaseTask()" class="cursor-pointer">{{ selectedTaskGroup.name }}</div>
        </div>
        <div v-if="selectedBaseTask" class="flex items-center gap-2">
          <icon name="caret-right" size="16"></icon>
          <div>{{ selectedBaseTask.name }}</div>
        </div>
      </div>
      <div class="flex gap-2 mt-2" v-if="coursesLoading || taskGroupsLoading || taskGroupLoading || baseTaskLoading">
        <Spinner></Spinner>
        <div>Loading...</div>
      </div>
      <div v-else>
        <div class="flex gap-2 mt-2" v-if="!selectedCourse">
          <div
            class="bg-gray-700 px-4 py-2 rounded-lg cursor-pointer ring-1 ring-gray-500"
            v-for="course in result"
            @click="goToCourse(course)"
          >
            {{ course.name }}
          </div>
        </div>
        <div class="flex gap-2 mt-2" v-if="taskGroups && !selectedTaskGroup && selectedCourse">
          <div
            class="bg-gray-700 px-4 py-2 rounded-lg cursor-pointer ring-1 ring-gray-500"
            v-for="group in taskGroups"
            @click="goToTaskGroup(group)"
          >
            {{ group.name }}
          </div>
        </div>
        <div class="flex gap-2 mt-2" v-if="taskGroup && selectedTaskGroup && !selectedBaseTask">
          <div
            class="bg-gray-700 px-4 py-2 rounded-lg cursor-pointer ring-1 ring-gray-500"
            v-for="baseTask in taskGroup.tasks"
            @click.stop="goToBaseTask(baseTask)"
          >
            {{ baseTask.name }}
          </div>
        </div>
        <div class="flex gap-2 mt-2" v-if="selectedBaseTask && baseTask">
          <div
            class="bg-gray-700 px-4 py-2 rounded-lg cursor-pointer ring-1"
            :class="isSelected(task) ? ' ring-highlight-500' : 'bg-gray-700 ring-gray-500'"
            v-for="task in baseTask?.tasks"
            @click="taskSelected(task)"
          >
            {{ task.task_question }}
          </div>
        </div>
      </div>
    </div>
    <div class="mt-4 text-xl">To which magnification should the slide be scaled to?</div>
    <div class="flex w-full justify-evenly items-center mt-4">
      <div class="flex items-center ring-2 ring-gray-500 rounded-lg h-10 overflow-hidden">
        <div
          class="flex items-center justify-center px-4 h-16 ring-3 hover:cursor-pointer"
          :class="selectedPatchMagnification === 0.1 ? 'bg-gray-500' : 'bg-gray-700'"
          @click="patchMagnificationChanged(0.1)"
        >
          0.1x
        </div>
        <div
          class="flex items-center justify-center px-4 h-16 ring-3 hover:cursor-pointer"
          :class="selectedPatchMagnification === 0.2 ? 'bg-gray-500' : 'bg-gray-700'"
          @click="patchMagnificationChanged(0.2)"
        >
          0.2x
        </div>
        <div
          class="flex items-center justify-center px-4 h-16 ring-3 hover:cursor-pointer"
          :class="selectedPatchMagnification === 0.5 ? 'bg-gray-500' : 'bg-gray-700'"
          @click="patchMagnificationChanged(0.5)"
        >
          0.5x
        </div>
        <div
          class="flex items-center justify-center px-4 h-16 ring-3 hover:cursor-pointer"
          :class="selectedPatchMagnification === 1.0 ? 'bg-gray-500' : 'bg-gray-700'"
          @click="patchMagnificationChanged(1.0)"
        >
          1.0x
        </div>
      </div>
    </div>
    <div class="mt-4 text-xl">How large should each image tile be?</div>
    <div class="flex w-full justify-evenly items-center mt-4">
      <div class="flex items-center ring-2 ring-gray-500 rounded-lg h-10 overflow-hidden">
        <div
          class="flex items-center justify-center px-4 h-16 ring-3 hover:cursor-pointer"
          :class="selectedPatchSize === 128 ? 'bg-gray-500' : 'bg-gray-700'"
          @click="patchSizeChanged(128)"
        >
          128
        </div>
        <div
          class="flex items-center justify-center px-4 h-16 ring-3 hover:cursor-pointer"
          :class="selectedPatchSize === 256 ? 'bg-gray-500' : 'bg-gray-700'"
          @click="patchSizeChanged(256)"
        >
          256
        </div>
        <div
          class="flex items-center justify-center px-4 h-16 ring-3 hover:cursor-pointer"
          :class="selectedPatchSize === 512 ? 'bg-gray-500' : 'bg-gray-700'"
          @click="patchSizeChanged(512)"
        >
          512
        </div>
      </div>
    </div>
  </div>
</template>
