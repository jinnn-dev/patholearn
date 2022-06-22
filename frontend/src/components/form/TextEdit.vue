<script lang='ts' setup>
import { ref } from 'vue';
import RoleOnly from '../containers/RoleOnly.vue';
import InputField from './InputField.vue';
import Icon from '../general/Icon.vue';

const emit = defineEmits(['valueChanged']);

const props = defineProps({
  value: String
});

const activeEdit = ref<Boolean>(false);

const newValue = ref<String>(props.value!);

const saveValue = () => {
  emit('valueChanged', newValue.value);
  activeEdit.value = false;
};
</script>
<template>
  <div class='flex flex-center items-center group'>
    <div class='w-full'>
      <div v-if='!activeEdit'>
        {{ newValue }}
      </div>
      <role-only>
        <input-field v-if='activeEdit' v-model='newValue' marginHor='my-0' />
      </role-only>
    </div>
    <role-only>
      <Icon
        v-if='!activeEdit'
        :size='20'
        class='group-hover:block ml-2 cursor-pointer'
        name='pencil-simple'
        @click='activeEdit = true'
      />
      <Icon
        v-if='activeEdit'
        :size='20'
        class='cursor-pointer ml-2'
        name='floppy-disk'
        weight='bold'
        @click.stop='saveValue'
      />
    </role-only>
  </div>
</template>
