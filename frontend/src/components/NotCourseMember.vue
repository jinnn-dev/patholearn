<template>
  <div class="text-center">
    <div class="text-5xl mb-4">{{ course?.name || 'Name' }}</div>
    <div class="text-2xl">bei {{ course?.owner.firstname }}</div>
  </div>
  <div class="flex flex-col items-center">
    <div class="text-4xl text-center mt-14 mb-8">Du bist nicht Teil dieses Kurses</div>
    <save-button label="Beitreten" class="w-42" @click="joinCourse" :loading="joinLoading"></save-button>
  </div>
</template>
<script lang="ts">
import { defineComponent, PropType, ref } from 'vue';
import { CourseService } from '../services/course.service';
import { Course } from '../model/course';

export default defineComponent({
  props: {
    course: Object as PropType<Course>
  },

  emits: ['courseJoined'],

  setup(props, { emit }) {
    const joinLoading = ref<Boolean>(false);
    const leaveCourseLoading = ref<Boolean>(false);

    const joinCourse = () => {
      if (props.course?.short_name) {
        joinLoading.value = true;
        CourseService.joinCourse(props.course.short_name).then((res) => {
          joinLoading.value = false;
          emit('courseJoined', res);
        });
      }
    };

    return { joinCourse, joinLoading, leaveCourseLoading };
  }
});
</script>
<style></style>
