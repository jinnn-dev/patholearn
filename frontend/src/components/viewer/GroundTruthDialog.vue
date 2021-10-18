<template>
  <modal-dialog :show="showDialog">
    <h1 class="text-2xl">Musterlösung hinzufügen</h1>
    <div class="my-2">
      <form-field label="Ground Thruth" tip="Wähle eine XML- oder PNG-Datei mit der Musterlösung aus">
        <div class="flex items-center">
          <label
            for="slide-upload"
            class="
              transition
              cursor-pointer
              flex
              justify-center
              bg-gray-500
              hover:bg-gray-300
              px-2
              w-full
              rounded-lg
              py-1
            "
          >
            <Icon name="cloud-arrow-up" class="mr-2" />
            <span>Musterlösung auswählen</span>
          </label>
          <div v-if="file" class="ml-4">{{ file.name }}</div>
        </div>
        <input class="hidden" id="slide-upload" type="file" @change="onFileSelected" />
      </form-field>
    </div>
    <div v-if="isWrongFormat" class="text-red-400">Wähle eine XML- oder PNG-Datei aus</div>
    <div v-if="conversionLoading && !isWrongFormat">Konvertiere...</div>
    <div v-else>
      <div v-if="convertResult">
        <div v-if="convertResult?.length === 0">Keine Annotationen gefunden</div>
        <div v-else>
          <div>Gefundene Annotationen:</div>
          <div v-for="group in convertResult" :key="group.name" class="flex justify-between my-2">
            <div class="w-6 h-6 overflow-hidden rounded-full">
              <input type="color" id="body" name="body" v-model="group.color" class="w-20" />
            </div>
            <!-- <div class="rounded-full w-6 h-6" :style="`background-color:${group.color}`"></div> -->
            <text-edit :value="group.name" @valueChanged="updateName($event, group)"></text-edit>
            <div>{{ group.polygons.length }}x</div>
          </div>
        </div>
      </div>
    </div>
    <div class="flex justify-end mt-8">
      <primary-button
        @click.prevent="$emit('closeDialog')"
        class="mr-2 w-28"
        name="Abbrechen"
        bgColor="bg-gray-500"
        bgHoverColor="bg-gray-700"
        fontWeight="font-normal"
      ></primary-button>
      <save-button
        v-if="convertResult"
        :loading="loading"
        :label="loading ? 'Wird verarbeitet...' : 'Hinzufügen'"
        @click="applyAnnotations"
        class="max-w-50"
      ></save-button>
    </div>
  </modal-dialog>
</template>
<script lang="ts">
import { SlideService } from '../../services/slide.service';
import { AnnotationParser, ParseResult } from '../../utils/annotation-parser';
import { defineComponent, onMounted, PropType, ref } from 'vue';
import { AnnotationViewer } from './core/annotationViewer';
import { ANNOTATION_TYPE } from '../../model/viewer/annotationType';

export default defineComponent({
  props: {
    showDialog: Boolean,
    drawingViewer: Object as PropType<AnnotationViewer>,
    loading: Boolean,
    isUserSolution: {
      type: Boolean,
      default: false
    }
  },
  emits: ['applyAnnotations', 'closeDialog'],
  setup(props, { emit }) {
    const file = ref();

    const convertResult = ref<ParseResult[]>();
    const conversionLoading = ref<Boolean>();

    const isWrongFormat = ref<Boolean>(false);

    onMounted(() => {
      file.value = undefined;
      convertResult.value = undefined;
      conversionLoading.value = false;
      isWrongFormat.value = false;
    });

    const updateName = (name: string, group: ParseResult) => {
      group.name = name;
    };

    const applyAnnotations = () => {
      for (const group of convertResult.value!) {
        for (const annotation of group.polygons) {
          annotation.color = group.color!;
          annotation.name = group.name!;
        }
      }

      emit('applyAnnotations', convertResult.value);
    };

    const onFileSelected = async (event: any) => {
      conversionLoading.value = true;
      isWrongFormat.value = false;

      file.value = event?.target.files[0];

      if (file.value.type === 'text/xml') {
        props.drawingViewer?.convertToAnnotations(file.value, (data: ParseResult[]) => {
          convertResult.value = data;

          conversionLoading.value = false;
        });
      } else if (file.value.type === 'image/png') {
        const formData = new FormData();
        formData.set('file', file.value);
        const res = await SlideService.convertImage(formData);

        convertResult.value = AnnotationParser.convertImageToAnnotations(
          res,
          props.drawingViewer!.viewer,
          props.isUserSolution ? ANNOTATION_TYPE.USER_SOLUTION : ANNOTATION_TYPE.SOLUTION
        );
        conversionLoading.value = false;
      } else {
        isWrongFormat.value = true;
      }
    };

    return {
      onFileSelected,
      updateName,
      applyAnnotations,
      file,
      convertResult,
      isWrongFormat,
      conversionLoading
    };
  }
});
</script>
<style></style>
