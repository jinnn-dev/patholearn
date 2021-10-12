<template>
  <div class="bg-gray-700 rounded-lg min-w-56 px-2 max-w-64 max-h-150 overflow-auto">
    <h2 class="sticky top-0 text-xl font-medium mb-4 py-2 bg-gray-700">Mitglieder</h2>
    <no-content class="mt-10" v-if="members?.length === 0" text="Keine Mitglieder" iconSize="w-20"></no-content>

    <div class="overflow-y-auto">
      <div v-for="member of members" :key="member.id" class="bg-gray-500 w-full rounded-lg p-1 px-2 my-2 min-h-8">
        {{ member.firstname }} {{ member.middlename }} {{ member.lastname }}
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { User } from '../model/user';
import { defineComponent, PropType } from 'vue';
export default defineComponent({
  props: {
    members: Array as PropType<User[]>
  },
  setup() {
    return {};
  }
});
</script>
<style></style>
