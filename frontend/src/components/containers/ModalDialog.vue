<script lang="ts" setup>
import { ref, watch } from 'vue';

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  customClasses: String
});

const showModal = ref<boolean>(false);

watch(
  () => props.show,
  (show) => {
    showModal.value = show;
  }
);
</script>
<template>
  <teleport to="body">
    <transition
      enter-active-class="transition ease-out duration-200 transform"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-200 transform"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-show="showModal" ref="modal-backdrop" class="fixed z-[99] inset-0 overflow-y-auto bg-black bg-opacity-50">
        <div class="flex items-center justify-center min-h-screen text-center text-gray-100">
          <transition
            enter-active-class="transition ease-out duration-300 transform "
            enter-from-class="opacity-0 translate-y-10 scale-95"
            enter-to-class="opacity-100 translate-y-0 scale-100"
            leave-active-class="ease-in duration-200"
            leave-from-class="opacity-100 translate-y-0 scale-100"
            leave-to-class="opacity-0 translate-y-10 translate-y-0 scale-95"
          >
            <div
              v-show="showModal"
              ref="modal"
              :class="customClasses"
              araia-modal="true"
              aria-labelledby="modal-headline"
              class="bg-gray-800 tex-gray-100 rounded-lg text-left shadow-xl p-4 top-1/2"
              role="dialog"
            >
              <transition
                enter-active-class="transition ease-out duration-200 transform"
                enter-from-class="opacity-0"
                enter-to-class="opacity-100"
                leave-active-class="transition ease-in duration-200 transform"
                leave-from-class="opacity-100"
                leave-to-class="opacity-0"
              >
                <div v-if="showModal">
                  <slot>Kein Inhalt</slot>
                </div>
              </transition>
            </div>
          </transition>
        </div>
      </div>
    </transition>
  </teleport>
</template>
