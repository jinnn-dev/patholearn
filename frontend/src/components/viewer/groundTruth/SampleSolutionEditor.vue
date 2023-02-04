<script lang="ts" setup>
import { ref } from 'vue';
import { TempUploadImage } from '../../../model/tempUploadImage';
import { useService } from '../../../composables/useService';
import { ImageService } from '../../../services/image.service';
import { AnnotationGroup } from '../../../model/task/annotationGroup';
import ModalDialog from '../../containers/ModalDialog.vue';
import BlurredContainer from '../../general/BlurredContainer.vue';
import MultiImageUpload from '../../form/MultiImageUpload.vue';
import PrimaryButton from '../../general/PrimaryButton.vue';
import TextEdit from '../../form/TextEdit.vue';
import Accordion from '../../containers/Accordion.vue';
import AccordionItem from '../../containers/AccordionItem.vue';
import AnnotationSlide from './AnnotationSlide.vue';
import ConfirmButtons from '../../general/ConfirmButtons.vue';

defineProps({
  showDialog: Boolean,
  slideId: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['close', 'applyAnnotations']);

const containsWrongFormat = ref(false);

const selectedSampleSolutionImages = ref<TempUploadImage[]>();

const { loading, result, run, reset } = useService(ImageService.convertImagesToAnnotations);

const annotationsGroups = ref<AnnotationGroup[]>();

const convertImages = async () => {
  const formData = new FormData();
  selectedSampleSolutionImages.value?.forEach((image) => {
    formData.append('images', image.file);
  });

  await run(formData);

  if (result.value) {
    annotationsGroups.value = result.value!.summary.map((item) => item.annotation_group);
  }
};

const onImagesDropped = (images: TempUploadImage[]) => {
  containsWrongFormat.value = false;
  for (const image of images) {
    if (image.file.type !== 'image/png') {
      containsWrongFormat.value = true;
      return;
    }
  }
  selectedSampleSolutionImages.value = images;
};

const updateName = (newName: string, group: AnnotationGroup) => {
  for (const summary of result.value!.summary) {
    if (summary.annotation_group.name === group.name) {
      summary.annotation_group.name = group.name;
    }
  }

  for (const item of result.value!.results) {
    for (const resultGroup of item.grey_groups) {
      if (resultGroup.annotation_group.name === group.name) {
        resultGroup.annotation_group.name = newName;
      }
    }
  }

  group.name = newName;
};

const updateColor = (newColor: any, group: AnnotationGroup) => {
  for (const item of result.value!.results) {
    for (const resultGroup of item.grey_groups) {
      if (resultGroup.annotation_group.name === group.name) {
        resultGroup.annotation_group.color = group.color;
      }
    }
  }
};

const apply = () => {
  emit('applyAnnotations', result.value);
  closeDialog();
};

const resetDialog = () => {
  reset();
  selectedSampleSolutionImages.value = undefined;
  annotationsGroups.value = undefined;
};

const closeDialog = () => {
  resetDialog();
  emit('close');
};
</script>
<template>
  <!--  TODO: Allow incremental solution addition. If already a solution exists add new one. Store grey values in key in annotation group. So the new image can than be mapped to the corresponding annotation group-->
  <modal-dialog :show="showDialog" custom-classes="w-full h-screen m-0 p-0 ">
    <BlurredContainer :bg-opacity="95" blur-amount="md" class="absolute w-full h-screen z-10 overflow-y-auto">
      <div class="relative w-full h-full flex flex-col justify-center items-center">
        <div v-if="!result" class="flex flex-col items-center justify-center w-full">
          <h1 class="text-3xl">Es ist noch keine Musterlösung hinzugefügt worden</h1>
          <MultiImageUpload
            class="w-2/3 h-96"
            label="Dateien mit Musterlösungen"
            tip="Füge eine Reihe von Dateien mit Musterlösungen hinzu. Entweder PNG- oder XML-Dateien"
            @imagesDropped="onImagesDropped"
          >
          </MultiImageUpload>
          <div v-if="containsWrongFormat" class="text-red-500 font-semibold">
            Es sind nur Dateien im PNG-Format erlaubt
          </div>
          <confirm-buttons
            :loading="loading"
            class="w-1/2 flex justify-end"
            confirm-text="Hochladen"
            reject-text="Abbrechen"
            @confirm="convertImages"
            @reject="closeDialog"
          ></confirm-buttons>
        </div>

        <div v-else class="flex flex-col justify-center items-center w-2/3 overflow-y-auto">
          <div v-if="result.summary.length === 0">
            <h2>Es wurden keine Annotationen gefunden</h2>
          </div>

          <div class="mb-8">
            <div class="text-2xl font-bold mb-8">Gefundene Annotationsgruppen</div>
            <div class="flex flex-col gap-4">
              <div v-for="group of annotationsGroups" class="flex justify-between gap-4 bg-gray-500 p-2 rounded-lg">
                <div class="w-6 h-6 flex-none ring-2 ring-gray-900 overflow-hidden rounded-full">
                  <input
                    id="body"
                    v-model="group.color"
                    class="w-20"
                    name="body"
                    type="color"
                    @input="updateColor($event, group)"
                  />
                </div>
                <text-edit :value="group.name" class="w-full" @valueChanged="updateName($event, group)"></text-edit>
              </div>
            </div>
          </div>

          <div>
            <div class="text-2xl font-bold mb-8 text-center">Gefundene Annotationen</div>
            <Accordion :collapse="false">
              <div class="w-full grid grid-cols-2 gap-4">
                <AccordionItem v-for="item of result?.results" class="rounded-lg w-full">
                  <template v-slot:header>
                    <div class="text-lg">
                      In der Datei <span class="font-bold">{{ item.file_name }}</span> wurden
                      <span class="font-bold">{{ item.annotation_count }}</span> Annotationen in
                      <span class="font-bold">{{ item.grey_groups.length }}</span> Annotationsgruppen gefunden
                    </div>
                  </template>

                  <div class="flex flex-col gap-2">
                    <div v-for="greyGroup of item.grey_groups" class="flex gap-3">
                      <div
                        :style="`background-color: ${greyGroup.annotation_group.color}`"
                        class="w-6 h-6 rounded-full flex-shrink-0"
                      ></div>
                      <div class="w-full">{{ greyGroup.annotation_group.name }}</div>
                      <div class="w-full text-right">{{ greyGroup.annotations.length }}x</div>
                    </div>
                  </div>
                </AccordionItem>
              </div>
            </Accordion>
          </div>
        </div>
        <div v-if="result" class="w-2/3 flex justify-end gap-4 mt-8">
          <PrimaryButton bg-color="bg-gray-400" class="w-32" name="Abbrechen" @click="closeDialog"></PrimaryButton>
          <PrimaryButton
            bg-color="bg-gray-400"
            class="w-56"
            name="Neue Bilder auswählen"
            @click="resetDialog"
          ></PrimaryButton>
          <PrimaryButton class="w-64" name="Als Musterlösung festlegen" @click="apply"></PrimaryButton>
        </div>
      </div>
    </BlurredContainer>

    <div class="h-full">
      <AnnotationSlide :slide-id="slideId"></AnnotationSlide>
    </div>
  </modal-dialog>
</template>
