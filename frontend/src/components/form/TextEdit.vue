<template>
  <div class="flex flex-center items-center group">
    <div>
      <div v-if="!activeEdit">{{ newValue }}</div>
      <role-only>
        <input-field v-model="newValue" v-if="activeEdit" marginHor="my-0" />
      </role-only>
    </div>
    <role-only>
      <Icon
        name="pencil-simple"
        v-if="!activeEdit"
        :size="20"
        class="group-hover:block ml-2 cursor-pointer"
        @click="activeEdit = true"
      />
      <Icon
        name="floppy-disk"
        v-if="activeEdit"
        class="cursor-pointer ml-2"
        :size="20"
        weight="bold"
        @click="saveValue"
      />
    </role-only>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
export default defineComponent({
  props: {
    value: String
  },

  emits: ['valueChanged'],

  setup(props, { emit }) {
    const activeEdit = ref<Boolean>(false);

    const newValue = ref<String>(props.value!);

    const saveValue = () => {
      emit('valueChanged', newValue.value);
      activeEdit.value = false;
    };

    return { activeEdit, newValue, saveValue };
  }
});
</script>
<style></style>
