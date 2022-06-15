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
          <div class='mr-2' :title="!isHidden(group) ? 'Klasse einblenden' : 'Klasse ausblenden'">
            <Icon
              name='eye'
              v-if='!isHidden(group)'
              class='cursor-pointer'
              @click.stop='toggleAnnotationGroup(group)'
            />
            <Icon name='eye-slash' v-else class='cursor-pointer' @click.stop='toggleAnnotationGroup(group)' />
          </div>
          <!-- <div class="w-4 h-4 mr-3 flex-shrink-0 rounded-full" :style="`background-color:${group.color}`"></div> -->
          <color-picker
            v-if='isSuperUser() && isAdmin'
            class='w-4 h-4 mr-3 flex-shrink-0'
            @isReleased='updateGroup(group.name, groupUpdateColor, group)'
            @changed='groupUpdateColor = $event'
            :initialColor='group.color'
          ></color-picker>
          <div v-else class='w-4 h-4 mr-3 flex-shrink-0 rounded-full' :style='`background-color: ${group.color}`'></div>
          <text-edit
            v-if='isSuperUser() && isAdmin'
            :value='group.name'
            @valueChanged='updateGroup($event, group.color, group)'
            class='w-full items-center'
          ></text-edit>
          <div v-else class='w-full items-center'>{{ group.name }}</div>
        </div>
      </div>
    </div>
    <role-only class='pt-2'>
      <primary-button
        v-if='isAdmin'
        name='Neue Klasse'
        class='py-1'
        bgColor='bg-gray-400'
        @click='showGroupCreation = true'
      ></primary-button>
    </role-only>
  </div>

  <role-only>
    <modal-dialog :show='showGroupCreation'>
      <h1 class='text-2xl text-center'>Neue Annotationsklasse</h1>

      <form @submit.prevent='onSubmit' class='w-full'>
        <input-field
          v-model='groupCreationForm.name'
          label='Klassenname'
          tip='Gib der Annotationsklasse einen Namen'
          placeholder='Classis...'
          class='mb-2'
          :required='true'
        ></input-field>

        <div class='flex flex-col mb-4'>
          <label for='body' class='text-gray-200'>Klassenfarbe:</label>
          <div class='rounded-lg overflow-hidden h-8'>
            <input type='color' id='body' name='body' v-model='groupCreationForm.color' />
          </div>
        </div>
        <div class='flex justify-end w-full'>
          <primary-button
            @click.prevent='showGroupCreation = false'
            class='mr-2 w-32'
            name='Abbrechen'
            bgColor='bg-gray-500'
            bgHoverColor='bg-gray-700'
            fontWeight='font-normal'
          ></primary-button>
          <save-button name='Speichern' type='submit' class='w-32' :loading='groupCreationLoading'></save-button>
        </div>
      </form>
    </modal-dialog>
  </role-only>
</template>

<script lang='ts'>
import { defineComponent, PropType, reactive, ref } from 'vue';
import { AnnotationGroup } from '../../model/task';
import { TaskService } from '../../services/task.service';
import { isSuperUser } from '../../utils/app.state';
import { isTaskSaving } from './core/viewerState';

export default defineComponent({
  props: {
    annotationGroups: {
      type: Object as PropType<AnnotationGroup[]>,
      default: []
    },

    isAdmin: {
      type: Boolean,
      default: false
    },

    taskId: Number
  },

  emits: ['showGroup', 'hideGroup', 'groupCreated', 'groupUpdated'],

  setup(props, { emit }) {
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
    return {
      toggleAnnotationGroup,
      isHidden,
      onSubmit,
      updateGroup,
      isSuperUser,
      showGroupCreation,
      groupCreationForm,
      groupCreationLoading,
      groupUpdateColor
    };
  }
});
</script>
<style></style>
