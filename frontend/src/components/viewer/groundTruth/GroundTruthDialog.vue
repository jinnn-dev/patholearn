<script lang="ts" setup>
import { onMounted, PropType, ref } from 'vue';
import { AnnotationViewer } from '../../../core/viewer/annotationViewer';
import { AnnotationParser, ParseResult } from '../../../utils/annotation-parser';
import { TempUploadImage } from '../../../model/tempUploadImage';
import { SlideService } from '../../../services/slide.service';
import { ANNOTATION_TYPE } from '../../../core/viewer/types/annotationType';
import ModalDialog from '../../containers/ModalDialog.vue';
import TextEdit from '../../form/TextEdit.vue';
import FormField from '../../form/FormField.vue';
import Icon from '../../general/Icon.vue';
import ConfirmButtons from '../../general/ConfirmButtons.vue';

const props = defineProps({
  showDialog: Boolean,
  drawingViewer: Object as PropType<AnnotationViewer>,
  loading: Boolean,
  isUserSolution: {
    type: Boolean,
    default: false
  },
  slideId: {
    type: String,
    required: true
  }
});

const file = ref();

const convertResult = ref<ParseResult[]>();
const conversionLoading = ref<boolean>();

const isWrongFormat = ref<boolean>(false);

const selectedImages = ref<TempUploadImage[]>();

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

const emit = defineEmits(['applyAnnotations', 'closeDialog']);
</script>
<template>
  <modal-dialog :show="showDialog">
    <h1 class="text-2xl">Musterlösung hinzufügen</h1>
    <div class="my-2">
      <form-field label="Ground Thruth" tip="Wähle eine XML- oder PNG-Datei mit der Musterlösung aus">
        <div class="flex items-center">
          <label
            class="transition cursor-pointer flex justify-center bg-gray-500 hover:bg-gray-300 px-2 w-full rounded-lg py-1"
            for="slide-upload"
          >
            <Icon class="mr-2" name="cloud-arrow-up" />
            <span>Musterlösung auswählen</span>
          </label>
          <div v-if="file" class="ml-4">
            {{ file.name }}
          </div>
        </div>
        <input id="slide-upload" class="hidden" type="file" @change="onFileSelected" />
      </form-field>
    </div>
    <div v-if="isWrongFormat" class="text-red-400">Wähle eine XML- oder PNG-Datei aus</div>
    <div v-if="conversionLoading && !isWrongFormat">Konvertiere...</div>
    <div v-else>
      <div v-if="convertResult">
        <div v-if="convertResult?.length === 0">Keine Annotationen gefunden</div>
        <div v-else>
          <div>Gefundene Annotationen:</div>
          <div v-for="group in convertResult" :key="group.name || ''" class="flex justify-between my-2">
            <div class="w-6 h-6 overflow-hidden rounded-full">
              <input id="body" v-model="group.color" class="w-20" name="body" type="color" />
            </div>
            <!-- <div class="rounded-full w-6 h-6" :style="`background-color:${group.color}`"></div> -->
            <text-edit :value="group.name || ''" @valueChanged="updateName($event, group)"></text-edit>
            <div>{{ group.polygons.length }}x</div>
          </div>
        </div>
      </div>
    </div>

    <confirm-buttons
      :confirm-text="loading ? 'Wird verarbeitet...' : 'Hinzufügen'"
      :loading="loading"
      class="mt-8"
      reject-text="Abbrechen"
      @confirm="applyAnnotations"
      @reject="$emit('closeDialog')"
    >
    </confirm-buttons>
  </modal-dialog>
</template>
