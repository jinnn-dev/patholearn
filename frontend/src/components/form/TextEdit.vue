<script lang='ts' setup>
import { ref } from 'vue';

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
        <input-field v-model='newValue' v-if='activeEdit' marginHor='my-0' />
      </role-only>
    </div>
    <role-only>
      <Icon
        name='pencil-simple'
        v-if='!activeEdit'
        :size='20'
        class='group-hover:block ml-2 cursor-pointer'
        @click='activeEdit = true'
      />
      <Icon
        name='floppy-disk'
        v-if='activeEdit'
        class='cursor-pointer ml-2'
        :size='20'
        weight='bold'
        @click.stop='saveValue'
      />
    </role-only>
  </div>
</template>
