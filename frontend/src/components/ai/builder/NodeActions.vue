<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue';
import Icon from '../../general/Icon.vue';
import { builderState, versionHasStatus } from '../../../core/ai/builder/state';
import ModalDialog from '../../../components/containers/ModalDialog.vue';
import InfoRenderer from './info/InfoRenderer.vue';
import { IconNames } from '../../../../icons';
import { TooltipGenerator } from '../../../utils/tooltips/tooltip-generator';

const showDescription = ref();

const props = defineProps({
  id: {
    type: String,
    required: true
  },
  label: {
    type: String,
    required: true
  },
  selected: Boolean
});

interface Item {
  id: string;
  icon: IconNames;
  action: Function;
  tooltip: string;
}

const items: Item[] = [
  {
    id: 'question',
    icon: 'question',
    action: () => (showDescription.value = true),
    tooltip: 'Show help'
  },
  {
    id: 'copy',
    icon: 'copy',
    action: () => builderState.syncPlugin?.cloneNode(props.id),
    tooltip: 'Duplicate the node'
  },
  {
    id: 'trash',
    icon: 'trash-new',
    action: () => builderState.syncPlugin?.removeNode(props.id),
    tooltip: 'Delete the node'
  }
];

onMounted(() => {
  for (const item of items) {
    TooltipGenerator.addGeneralTooltip({
      target: '#' + item.id,
      content: item.tooltip,
      placement: 'top',
      delay: 300
    });
  }
});

onUnmounted(() => {
  for (const item of items) {
    TooltipGenerator.removeTooltipByElementId('#' + item.id);
  }
});
</script>
<template>
  <modal-dialog :show="showDescription">
    <div class="relative w-full" v-if="showDescription">
      <div
        class="absolute right-0 p-1 hover:bg-gray-500 rounded-lg hover:cursor-pointer"
        @click="showDescription = false"
      >
        <icon name="x"></icon>
      </div>
    </div>
    <info-renderer :label="label"></info-renderer>
  </modal-dialog>
  <div
    v-if="selected && id && !versionHasStatus"
    class="absolute flex -top-12 rounded-lg left-0 overflow-hidden ring-1 ring-gray-500 bg-gray-700 shadow-md shadow-gray-900/50"
  >
    <div v-for="item in items" :id="item.id" class="hover:bg-gray-500 p-1" @click.stop="item.action()">
      <icon :name="item.icon" size="28" stroke-width="0"></icon>
    </div>
    <!-- <div class="hover:bg-gray-500 p-1">
      <icon name="question" size="28" stroke-width="0" @click.stop="showDescription = true"></icon>
    </div>
    <div class="hover:bg-gray-500 p-1" @click.stop="builderState.syncPlugin?.cloneNode(id)">
      <icon name="copy" size="28" stroke-width="0"></icon>
    </div>
    <div class="hover:bg-gray-500 p-1">
      <icon name="trash" size="28" @click.stop="builderState.syncPlugin?.removeNode(id)"></icon>
    </div> -->
  </div>
</template>
