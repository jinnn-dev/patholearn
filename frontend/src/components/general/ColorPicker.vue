<script lang='ts' setup>
import FormField from '../form/FormField.vue';

defineEmits(['isReleased', 'changed']);

defineProps({
  label: String,
  initialColor: {
    type: String,
    default: '#000'
  }
});
</script>
<template>
  <form-field :label='label'>
    <div class='rounded-lg w-full overflow-hidden'>
      <input
        id='body'
        :value='initialColor'
        class='h-6 w-full cursor-pointer'
        name='body'
        type='color'
        @change="$emit('isReleased', $event.target.value)"
        @input="$emit('changed', $event.target.value)"
      />
    </div>
  </form-field>
</template>
