<script lang="ts" setup>
import { debounceRef } from '../../utils/debounceRef';
import { ref, watch } from 'vue';
import { Course } from '../../model/course';
import { CourseService } from '../../services/course.service';
import { onClickOutside } from '@vueuse/core';
import InputField from '../form/InputField.vue';
import Icon from '../general/Icon.vue';
import SaveButton from '../general/SaveButton.vue';

const emit = defineEmits(['joined']);

const searchString = debounceRef<string>('');
const foundCourses = ref<Course[]>([]);
const loading = ref<boolean>(false);
const joinCourseLoading = ref<boolean>(false);

const target = ref(null);
const isFocus = ref<boolean>(false);
watch(
  () => searchString.value,
  (newVal, _) => {
    if (newVal.length !== 0) {
      loading.value = true;
      CourseService.getCourses(newVal as string).then((res: Course[]) => {
        foundCourses.value = res;
        loading.value = false;
      });
    }
  }
);

onClickOutside(target, () => {
  isFocus.value = false;
});
const joinCourse = (course: Course) => {
  joinCourseLoading.value = true;
  CourseService.joinCourse(course.short_name)
    .then((res: Course) => {
      emit('joined', res);
      isFocus.value = false;
      searchString.value = '';
    })
    .finally(() => {
      joinCourseLoading.value = false;
    });
};
</script>
<template>
  <div ref="target" class="relative">
    <input-field
      v-model="searchString"
      paddingLeft="pl-10"
      placeholder="Tippe, um nach einem Kurs zu suchen..."
      @click="isFocus = true"
    >
      <template v-slot:firstIcon>
        <Icon class="text-gray-200" name="magnifying-glass" />
      </template>
    </input-field>

    <div v-if="searchString.length !== 0 && isFocus" class="absolute w-full bg-gray-700 rounded-lg px-2 shadow-2xl">
      <div v-if="!loading && foundCourses.length === 0" class="p-2">Keine Kurse gefunden</div>
      <div v-else-if="loading && foundCourses.length === 0" class="p-2">Suche Kurse...</div>
      <div v-else>
        <div
          v-for="course in foundCourses"
          :key="course.id"
          class="flex transition justify-start items-center hover:bg-gray-500 bg-gray-500 my-4 p-2 rounded-md cursor-pointer h-14"
          @click="course.is_member ? $router.push('/course/' + course.short_name) : ''"
        >
          <div class="w-full">
            {{ course.name }}
          </div>
          <save-button
            v-if="!course.is_member"
            :loading="joinCourseLoading"
            class="w-24"
            fontWeight="font-semibold"
            name="Beitreten"
            @click.stop="joinCourse(course)"
          ></save-button>
        </div>
      </div>
    </div>
  </div>
</template>
