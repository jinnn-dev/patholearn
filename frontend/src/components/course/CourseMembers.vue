<script lang="ts" setup>
import { PropType } from 'vue';
import { User } from '../../model/user';
import NoContent from '../general/NoContent.vue';

defineProps({
  members: Array as PropType<User[]>
});
</script>
<template>
  <div class="bg-gray-700 rounded-lg min-w-56 px-2 max-w-64 max-h-[50vh] overflow-auto">
    <h2 class="sticky top-0 text-xl font-medium mb-4 py-2 bg-gray-700">Mitglieder</h2>
    <no-content
      v-if="members?.length === 0"
      class="mt-10"
      iconSize="w-12"
      text="Keine Mitglieder"
      textSize="text-lg"
    ></no-content>
    <div class="overflow-y-auto">
      <div v-for="member of members" :key="member.id" class="bg-gray-500 w-full rounded-lg p-1 px-2 my-2 min-h-8">
        {{ member.firstname }}
        {{ member.lastname }}
      </div>
    </div>
  </div>
</template>
