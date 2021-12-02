<template>
  <saving-info></saving-info>

  <div ref="viewerRef" id="viewerImage" class="h-screen bg-gray-900" @keyup="handleKeyup"></div>
</template>
<script lang="ts">
import { defineComponent, onMounted, PropType, ref, watch } from 'vue';
import { ImageSelectFeedback, TaskResult } from '../../../model/result';
import { Task } from '../../../model/task';
import { ANNOTATION_COLOR } from '../../../model/viewer/colors';
import { TaskService } from '../../../services/task.service';
import { isTaskSaving, userSolutionLocked } from '../../viewer/core/viewerState';
import { ImageSelectViewer } from './imageSelectViewer';

export default defineComponent({
  props: {
    task: Object as PropType<Task | undefined>,
    base_task_id: {
      type: Number,
      required: true
    },
    task_group_id: {
      type: Number,
      required: true
    },
    course_id: {
      type: Number
    },

    show_result: Boolean,
    solve_result: Object as PropType<TaskResult | undefined>,
    is_solving: Boolean,

    isAdmin: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const imageSelectViewer = ref<ImageSelectViewer>();

    const images = ref<string[]>([]);

    watch(
      () => images.value,
      async () => {
        isTaskSaving.value = true;
        if (props.isAdmin) {
          if (JSON.stringify(images.value) !== JSON.stringify(props.task?.solution)) {
            const newTask = await TaskService.updateTask({
              task_id: props.task!.id,
              solution: JSON.stringify(images.value)
            });

            props.task!.solution = newTask.solution;
          }
        } else {
          if (!props.task!.user_solution) {
            const userSolution = await TaskService.saveUserSolution({
              task_id: props.task!.id,
              base_task_id: props.base_task_id,
              task_group_id: props.task_group_id,
              course_id: props.course_id!,
              solution_data: JSON.stringify(images.value)
            });

            props.task!.user_solution = userSolution;
          } else {
            if (JSON.stringify(images.value) !== JSON.stringify(props.task?.user_solution.solution_data)) {
              const userSolution = await TaskService.updateUserSolution({
                task_id: props.task!.id,
                solution_data: JSON.stringify(images.value)
              });

              props.task!.user_solution = userSolution;
            }
          }
        }
        isTaskSaving.value = false;
      }
    );

    watch(
      () => props.solve_result,
      (newVal: TaskResult | undefined, oldVal: TaskResult | undefined) => {
        imageSelectViewer.value?.resetResultColors();

        if (newVal && props.show_result) {
          imageSelectViewer.value?.setResultColors(newVal.result_detail as ImageSelectFeedback[]);
        }
      }
    );

    watch(
      () => props.show_result,
      () => {
        if (imageSelectViewer.value) {
          imageSelectViewer.value.clickDisabled = props.show_result;
        }
      }
    );

    watch(
      () => props.task,
      (oldval, newval) => {
        if (oldval !== newval) {
          imageSelectViewer.value?.destroy();
          setImageSelectViewer();
          imageSelectViewer.value!.clickDisabled = props.show_result;
          if (props.solve_result && props.show_result) {
            userSolutionLocked.value = true;
            const resultDetail = props.solve_result.result_detail;
            imageSelectViewer.value?.setResultColors(resultDetail as ImageSelectFeedback[]);
          }
        }
      }
    );

    watch(
      () => imageSelectViewer.value,
      () => {
        if (images.value !== Array.from(imageSelectViewer.value?.selectedImagesRef as Set<string>)) {
          images.value = Array.from(imageSelectViewer.value?.selectedImagesRef as Set<string>);
        }
      },
      { deep: true }
    );

    const setImageSelectViewer = () => {
      const selectColor = props.isAdmin ? ANNOTATION_COLOR.SOLUTION_COLOR : ANNOTATION_COLOR.USER_SOLUTION_COLOR;
      const solution = props.isAdmin
        ? (props.task?.solution as string[])
        : (props.task?.user_solution?.solution_data as string[]);
      imageSelectViewer.value = new ImageSelectViewer(
        props.task?.task_data as string[],
        solution,
        selectColor,
        !props.isAdmin
      );
    };

    onMounted(() => {
      setImageSelectViewer();
      imageSelectViewer.value!.clickDisabled = props.show_result;

      if (props.solve_result && props.show_result) {
        userSolutionLocked.value = true;
        const resultDetail = props.solve_result.result_detail;
        imageSelectViewer.value?.setResultColors(resultDetail as ImageSelectFeedback[]);
      }
    });
  }
});
</script>
<style></style>
