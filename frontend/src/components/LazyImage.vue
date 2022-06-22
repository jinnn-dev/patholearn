<script lang='ts' setup>
import { ref } from 'vue';
import Icon from './general/Icon.vue';

const props = defineProps({
  imageUrl: {
    type: String,
    required: true
  },
  alt: String,
  imageClasses: String
});

const emit = defineEmits(['imageLoaded']);

const loaded = ref<Boolean>(false);

const url = ref(props.imageUrl);
let tries = 0;

const onLoaded = () => {
  loaded.value = true;
  emit('imageLoaded');
};

const handleError = () => {
  if (tries > 1) {
    imageLoadError.value = true;
    loaded.value = true;
  }

  const splittedUrl = url.value.split('.');

  const fileEnding = splittedUrl[splittedUrl.length - 1];

  const newUrl = splittedUrl.slice(0, splittedUrl.length - 1);

  if (fileEnding === 'png') {
    newUrl.push('jpeg');
  } else if (fileEnding === 'jpeg') {
    newUrl.push('jpg');
  } else {
    newUrl.push('png');
  }
  tries++;
  url.value = newUrl.join('.');
  loaded.value = false;
};

const imageLoadError = ref(false);

</script>
<template>
  <div class='overflow-hidden w-full h-full flex justify-center items-center relative select-none'>
    <svg
      v-if='!loaded && !imageLoadError'
      class='absolute animate-spin h-5 w-5 text-white'
      xmlns='http://www.w3.org/2000/svg'
      fill='none'
      viewBox='0 0 24 24'
    >
      <circle class='opacity-25' cx='12' cy='12' r='10' stroke='currentColor' stroke-width='4'></circle>
      <path
        class='opacity-75'
        fill='currentColor'
        d='M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z'
      ></path>
    </svg>
    <div v-if='!imageLoadError' class='w-full h-full overflow-hidden flex justify-center items-center'>
      <img
        :src='url'
        @load='onLoaded'
        :class="loaded ? 'show ' + imageClasses : ''"
        class='rounded-lg'
        @error='handleError'
        alt='Lazy image' />
    </div>
    <div v-else class='bg-gray-300 p-2 rounded-lg'>
      <Icon name='filex' :width='32' :height='32' />
    </div>
  </div>
</template>
<style scoped>
img {
  opacity: 0;
  transition: 0.5s ease-in-out;
}

img.show {
  opacity: 1;
}
</style>
