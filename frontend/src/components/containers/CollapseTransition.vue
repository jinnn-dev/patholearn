<template>
  <transition
    enter-active-class="enter-active"
    leave-active-class="leave-active"
    @before-enter="beforeEnter"
    @enter="enter"
    @after-enter="afterEnter"
    @before-leave="beforeLeave"
    @leave="leave"
    @after-leave="afterLeave"
  >
    <slot />
  </transition>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  props: {},
  setup() {
    /**
     * @param {HTMLElement} element
     */
    function beforeEnter(element) {
      requestAnimationFrame(() => {
        if (!element.style.height) {
          element.style.height = '0px';
        }

        element.style.display = null;
      });
    }
    /**
     * @param {HTMLElement} element
     */
    function enter(element) {
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          element.style.height = `${element.scrollHeight}px`;
        });
      });
    }
    /**
     * @param {HTMLElement} element
     */
    function afterEnter(element) {
      element.style.height = null;
    }
    /**
     * @param {HTMLElement} element
     */
    function beforeLeave(element) {
      requestAnimationFrame(() => {
        if (!element.style.height) {
          element.style.height = `${element.offsetHeight}px`;
        }
      });
    }
    /**
     * @param {HTMLElement} element
     */
    function leave(element) {
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          element.style.height = '0px';
        });
      });
    }
    /**
     * @param {HTMLElement} element
     */
    function afterLeave(element) {
      element.style.height = null;
    }

    return {
      beforeEnter,
      enter,
      afterEnter,
      beforeLeave,
      leave,
      afterLeave
    };
  }
});
</script>
<style>
.enter-active,
.leave-active {
  overflow: hidden;
  transition: height 0.15s linear;
}
</style>
