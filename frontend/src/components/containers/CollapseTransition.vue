<script lang='ts' setup>
function beforeEnter(element: HTMLElement) {
  requestAnimationFrame(() => {
    if (!element.style.height) {
      element.style.height = '0px';
    }

    element.style.display = 'null';
  });
}

function enter(element: HTMLElement) {
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      element.style.height = `${element.scrollHeight}px`;
    });
  });
}

function afterEnter(element: HTMLElement) {
  element.style.height = 'null';
}

function beforeLeave(element: HTMLElement) {
  requestAnimationFrame(() => {
    if (!element.style.height) {
      element.style.height = `${element.offsetHeight}px`;
    }
  });
}

function leave(element: HTMLElement) {
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      element.style.height = '0px';
    });
  });
}

function afterLeave(element: HTMLElement) {
  element.style.height = 'null';
}
</script>

<template>
  <transition
    enter-active-class='enter-active'
    leave-active-class='leave-active'
    @before-enter='beforeEnter'
    @enter='enter'
    @after-enter='afterEnter'
    @before-leave='beforeLeave'
    @leave='leave'
    @after-leave='afterLeave'
  >
    <slot />
  </transition>
</template>
<style>
.enter-active,
.leave-active {
  overflow: hidden;
  transition: height 0.15s linear;
}
</style>
