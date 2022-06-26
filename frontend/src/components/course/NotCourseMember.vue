<script lang='ts' setup>
import { PropType, ref } from 'vue';
import { Course } from '../../model/course';
import { CourseService } from '../../services/course.service';
import SaveButton from '../general/SaveButton.vue';

const props = defineProps({
  course: Object as PropType<Course>
});

const emit = defineEmits(['courseJoined']);

const joinLoading = ref<Boolean>(false);

const joinCourse = () => {
  if (props.course?.short_name) {
    joinLoading.value = true;
    CourseService.joinCourse(props.course.short_name).then((res) => {
      joinLoading.value = false;
      emit('courseJoined', res);
    });
  }
};
</script>
<template>
  <div class='text-center'>
    <div class='text-5xl mb-4'>
      {{ course?.name || 'Name' }}
    </div>
    <div class='text-2xl'>bei {{ course?.owner.firstname }}</div>
  </div>
  <div class='flex flex-col items-center'>
    <div class='text-4xl text-center mt-14 mb-8'>Du bist nicht Teil dieses Kurses</div>
    <save-button :loading='joinLoading' class='w-42' label='Beitreten' @click='joinCourse'></save-button>
  </div>
</template>
