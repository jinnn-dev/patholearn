<template>
  <router-link :to="'/course/' + course.short_name">
    <skeleton-card>
      <div class="max-h-60 w-96">
        <div class="text-xl truncated-lines-2">{{ course.name }}</div>
        <div class="text-gray-200" v-if="!isCourseOwner">
          bei {{ course.owner.firstname }} {{ course.owner.lastname }}
        </div>
        <progress-bar
          v-if="!isCourseOwner"
          :id="course.short_name"
          :percentage="course.percentage_solved"
          :wrongTasks="course.wrong_tasks"
          :correctTasks="course.correct_tasks"
          :taskCount="course.task_count"
        ></progress-bar>
        <task-count-badge :count="course.task_count"></task-count-badge>
        <new-task-badge v-if="course.new_tasks"></new-task-badge>
        <div class="mt-4">
          <div v-if="course.description" class="truncated-lines-4">
            {{ course.description }}
          </div>
          <div v-else class="text-gray-300 font-semibold">Keine Beschreibung</div>
        </div>
      </div>
    </skeleton-card>
  </router-link>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
export default defineComponent({
  props: {
    course: {
      type: Object,
      required: true
    },
    isCourseOwner: {
      type: Boolean,
      required: true
    }
  },
  setup() {}
});
</script>
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
