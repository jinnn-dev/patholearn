<script lang='ts' setup>
import SkeletonCard from '../containers/SkeletonCard.vue';
import NewTaskBadge from '../task/NewTaskBadge.vue';
import TaskCountBadge from '../task/TaskCountBadge.vue';
import ProgressBar from '../task/ProgressBar.vue';
import { PropType } from 'vue';
import { Course } from '../../model/course';

defineProps({
  course: {
    type: Object as PropType<Course>,
    required: true
  },
  isCourseOwner: {
    type: Boolean,
    required: true
  }
});
</script>
<template>
  <router-link :to="'/course/' + course.short_name + (isCourseOwner ? '/admin' : '')">
    <skeleton-card>
      <div class='max-h-60 w-96'>
        <div class='text-xl truncated-lines-2'>
          {{ course.name }}
        </div>
        <div v-if='!isCourseOwner' class='text-gray-200'>
          bei
          {{ course.owner.firstname }}
          {{ course.owner.lastname }}
        </div>
        <progress-bar
          v-if='!isCourseOwner'
          :id='course.short_name'
          :correctTasks='course.correct_tasks'
          :percentage='course.percentage_solved'
          :taskCount='course.task_count'
          :wrongTasks='course.wrong_tasks'
        ></progress-bar>
        <task-count-badge :count='course.task_count'></task-count-badge>
        <new-task-badge v-if='course.new_tasks'></new-task-badge>
        <div class='mt-4'>
          <div v-if='course.description' class='truncated-lines-4'>
            {{ course.description }}
          </div>
          <div v-else class='text-gray-300 font-semibold'>Keine Beschreibung</div>
        </div>
      </div>
    </skeleton-card>
  </router-link>
</template>
<style>
.truncated-lines-4 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 4;
}

.truncated-lines-2 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}
</style>
