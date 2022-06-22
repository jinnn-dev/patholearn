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
        type='color'
        :value='initialColor'
        id='body'
        name='body'
        @change="$emit('isReleased', $event.target.value)"
        @input="$emit('changed', $event.target.value)"
        class='h-6 w-full cursor-pointer'
      />
    </div>
  </form-field>
</template>
