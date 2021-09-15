import 'virtual:windi.css';
import { createApp } from 'vue';
import App from './App.vue';
import PrimaryButton from './components/base/PrimaryButton.vue';
import ModalDialog from './components/containers/ModalDialog.vue';
import RoleOnly from './components/containers/RoleOnly.vue';
import SkeletonCard from './components/containers/SkeletonCard.vue';
import FormField from './components/FormField.vue';
import {
  PhActivity,
  PhArrowLeft,
  PhAt,
  PhCaretLeft,
  PhCheckCircle,
  PhCircle,
  PhCloudArrowUp,
  PhEraser,
  PhEye,
  PhEyeSlash,
  PhFloppyDisk,
  PhHandGrabbing,
  PhHandPointing,
  PhKey,
  PhMagnifyingGlass,
  PhMinus,
  PhPencil,
  PhPencilSimple,
  PhPenNib,
  PhPlus,
  PhPushPin,
  PhTrash,
  PhTriangle,
  PhUpload,
  PhUser,
  PhXCircle
} from './components/icons/phosphor-vue/src/entry';
import InputField from './components/InputField.vue';
import SaveButton from './components/SaveButton.vue';
import TextEdit from './components/TextEdit.vue';
import router from './router';
import { ApiService } from './services/api.service';
import { TokenService } from './services/token.service';

if (TokenService.getToken()) {
  ApiService.setHeader();
  ApiService.mount401Interceptor();
}

const app = createApp(App);
app.use(router);

app.component('primary-button', PrimaryButton);
app.component('save-button', SaveButton);
app.component('role-only', RoleOnly);
app.component('skeleton-card', SkeletonCard);
app.component('input-field', InputField);
app.component('modal-dialog', ModalDialog);
app.component('text-edit', TextEdit);
app.component('form-field', FormField);
app.mount('#app');

// Init Icons
app.component('ph-arrow-left', PhArrowLeft);
app.component('ph-magnifying-glass', PhMagnifyingGlass);
app.component('ph-plus', PhPlus);
app.component('ph-cloud-arrow-up', PhCloudArrowUp);
app.component('ph-pencil-simple', PhPencilSimple);
app.component('ph-floppy-disk', PhFloppyDisk);
app.component('ph-caret-left', PhCaretLeft);
app.component('ph-circle', PhCircle);
app.component('ph-check-circle', PhCheckCircle);
app.component('ph-x-circle', PhXCircle);
app.component('ph-minus', PhMinus);
app.component('ph-push-pin', PhPushPin);
app.component('ph-activity', PhActivity);
app.component('ph-triangle', PhTriangle);
app.component('ph-eye', PhEye);
app.component('ph-hand-pointing', PhHandPointing);
app.component('ph-hand-grabbing', PhHandGrabbing);
app.component('ph-eraser', PhEraser);
app.component('ph-pen-nib', PhPenNib);
app.component('ph-pencil', PhPencil);
app.component('ph-upload', PhUpload);
app.component('ph-trash', PhTrash);
app.component('ph-user', PhUser);
app.component('ph-at', PhAt);
app.component('ph-key', PhKey);
app.component('ph-eye-slash', PhEyeSlash);
