<script lang='ts' setup>
import { PropType, reactive, ref } from 'vue';
import { AnnotationGroup } from '../../model/task/annotationGroup';
import { TaskService } from '../../services/task.service';
import { isSuperUser } from '../../utils/app.state';
import { isTaskSaving } from './core/viewerState';
import Icon from '../general/Icon.vue';
import ColorPicker from '../general/ColorPicker.vue';
import TextEdit from '../form/TextEdit.vue';
import RoleOnly from '../containers/RoleOnly.vue';
import PrimaryButton from '../general/PrimaryButton.vue';
import ModalDialog from '../containers/ModalDialog.vue';
import InputField from '../form/InputField.vue';
import SaveButton from '../general/SaveButton.vue';

const props = defineProps({
  annotationGroups: {
    type: Object as PropType<AnnotationGroup[]>,
    default: []
  },

  isAdmin: {
    type: Boolean,
    default: false
  },

  taskId: Number
});

const emit = defineEmits(['showGroup', 'hideGroup', 'groupCreated', 'groupUpdated']);

const showGroupCreation = ref<Boolean>(false);

const hiddenElements = ref<AnnotationGroup[]>([]);

const groupUpdateColor = ref('');

const groupCreationForm = reactive({
  name: '',
  color: '#FF00FF'
});

const groupCreationLoading = ref<Boolean>(false);

const isHidden = (group: AnnotationGroup) => {
  return hiddenElements.value?.includes(group);
};

const toggleAnnotationGroup = (group: AnnotationGroup) => {
  if (!hiddenElements.value?.includes(group)) {
    hiddenElements.value?.push(group);
    emit('hideGroup', group);
  } else {
    const index = hiddenElements.value.findIndex((item) => item.name === group.name);
    if (index !== -1) {
      hiddenElements.value.splice(index, 1);
      emit('showGroup', group);
    }
  }
};

const updateGroup = async (newName: string, newColor: string, group: AnnotationGroup) => {
  if (newName !== group.name || newColor !== group.color) {
    isTaskSaving.value = true;

    TaskService.updateAnnotationGroup(props.taskId!, group.name, newName, newColor).then(() => {
      emit('groupUpdated', {
        group,
        newName,
        newColor
      });
      isTaskSaving.value = false;
    });
  }
};

const onSubmit = () => {
  groupCreationLoading.value = true;
  TaskService.createAnnotationGroup(props.taskId!, groupCreationForm.name, groupCreationForm.color)
    .then((annotationGroup: AnnotationGroup) => {
      emit('groupCreated', annotationGroup);

      props.annotationGroups?.push(annotationGroup);
    })
    .catch((e) => {
      console.log(e);
    })
    .finally(() => {
      groupCreationLoading.value = false;
      showGroupCreation.value = false;
    });
};
</script>
<template>
  <div class='fixed right-0 top-6 z-10 bg-gray-700/70 backdrop-blur-md rounded-l-lg p-2 w-80'>
    <div v-if='!annotationGroups || annotationGroups.length === 0' class='my-2'>Keine Klassen vorhanden</div>
    <div v-else>
      <h3 class='text-xl'>Vorhandene Klassen</h3>
      <div class='max-h-[11rem] max-full overflow-auto'>
        <div
          v-for='group in annotationGroups'
          :key='group.name + group.color'
          class='bg-gray-500 rounded-lg px-2 py-1 flex items-center my-2'
        >
          <div :title="!isHidden(group) ? 'Klasse einblenden' : 'Klasse ausblenden'" class='mr-2'>
            <Icon
              v-if='!isHidden(group)'
              class='cursor-pointer'
              name='eye'
              @click.stop='toggleAnnotationGroup(group)'
            />
            <Icon v-else class='cursor-pointer' name='eye-slash' @click.stop='toggleAnnotationGroup(group)' />
          </div>
          <!-- <div class="w-4 h-4 mr-3 flex-shrink-0 rounded-full" :style="`background-color:${group.color}`"></div> -->
          <color-picker
            v-if='isSuperUser() && isAdmin'
            :initialColor='group.color'
            class='w-4 h-4 mr-3 flex-shrink-0'
            @changed='groupUpdateColor = $event'
            @isReleased='updateGroup(group.name, groupUpdateColor, group)'
          ></color-picker>
          <div v-else :style='`background-color: ${group.color}`' class='w-4 h-4 mr-3 flex-shrink-0 rounded-full'></div>
          <text-edit
            v-if='isSuperUser() && isAdmin'
            :value='group.name'
            class='w-full items-center'
            @valueChanged='updateGroup($event, group.color, group)'
          ></text-edit>
          <div v-else class='w-full items-center'>{{ group.name }}</div>
        </div>
      </div>
    </div>
    <role-only>
      <primary-button
        v-if='isAdmin'
        bgColor='bg-gray-400'
        class='py-2'
        name='Neue Klasse'
        @click='showGroupCreation = true'
      ></primary-button>
    </role-only>
  </div>

  <role-only>
    <modal-dialog :show='showGroupCreation'>
      <h1 class='text-2xl text-center'>Neue Annotationsklasse</h1>

      <form class='w-full' @submit.prevent='onSubmit'>
        <input-field
          v-model='groupCreationForm.name'
          :required='true'
          class='mb-2'
          label='Klassenname'
          placeholder='Classis...'
          tip='Gib der Annotationsklasse einen Namen'
        ></input-field>

        <div class='flex flex-col mb-4'>
          <label class='text-gray-200' for='body'>Klassenfarbe:</label>
          <div class='rounded-lg overflow-hidden h-8'>
            <input id='body' v-model='groupCreationForm.color' name='body' type='color' />
          </div>
        </div>
        <div class='flex justify-end w-full'>
          <primary-button
            bgColor='bg-gray-500'
            bgHoverColor='bg-gray-700'
            class='mr-2 w-32'
            fontWeight='font-normal'
            name='Abbrechen'
            @click.prevent='showGroupCreation = false'
          ></primary-button>
          <save-button :loading='groupCreationLoading' class='w-32' name='Speichern' type='submit'></save-button>
        </div>
      </form>
    </modal-dialog>
  </role-only>
</template>
