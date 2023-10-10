import { IconNames } from '../../../../icons';
import { NodeType } from './nodes/types';

export type EventName =
  | 'center'
  | 'save'
  | 'clear'
  | 'generate'
  | 'parse'
  | 'train'
  | 'abort'
  | 'downloadPython'
  | 'downloadJupyter'
  | NodeType;

interface EventSettingItem {
  icon: IconNames;
  label: string;
  divider?: boolean;
  header?: string;
  disableOnTraining?: boolean;
}

type EventSetting = Record<EventName, EventSettingItem>;

export const eventSettings: EventSetting = {
  center: { icon: 'arrow-counter-clockwise', label: 'Center' },
  save: { icon: 'floppy-disk', label: 'Save', disableOnTraining: true },
  clear: { icon: 'broom', label: 'Clear', disableOnTraining: true },
  generate: {
    icon: 'magic-stick',
    label: 'Generate',
    divider: true,
    header: 'Model Creation',
    disableOnTraining: true
  },
  train: { icon: 'barbell', label: 'Start', header: 'Training', divider: true, disableOnTraining: true },
  abort: { icon: 'stop', label: 'Reset / Stop' },
  parse: { icon: 'code', label: 'Show code', divider: true, header: 'Download' },
  downloadPython: { icon: 'code', label: 'Python' },
  downloadJupyter: { icon: 'notebook', label: 'Jupyter Notebook' },
  DatasetNode: { icon: 'images', label: 'Dataset', divider: true, disableOnTraining: true },
  Conv2DNode: { icon: 'stack', label: 'Conv2D', divider: true, disableOnTraining: true },
  LinearNode: { icon: 'cards', label: 'Linear', disableOnTraining: true },
  PoolingNode: { icon: 'arrows-in', label: 'Pooling', disableOnTraining: true },
  DropoutNode: { icon: 'drop-half', label: 'Dropout', divider: true, disableOnTraining: true },
  FlattenNode: { icon: 'dots-three-outline', label: 'Flatten', disableOnTraining: true },
  BatchNormNode: { icon: 'equalizer', label: 'BatchNorm', disableOnTraining: true },
  AddNode: { icon: 'arrows-merge', label: 'Add', divider: true, disableOnTraining: true },
  ConcatenateNode: { icon: 'plus-circle-new', label: 'Concatenate', disableOnTraining: true },
  OutputNode: { icon: 'flag', label: 'Output', divider: true, disableOnTraining: true },
  MetricNode: { icon: 'chart-line', label: 'Metric', divider: true, disableOnTraining: true },
  ResNetNode: { icon: 'image', label: 'ResNet', divider: true, disableOnTraining: true },
  GoogleNetNode: { icon: 'image', label: 'GoogLeNet', disableOnTraining: true },
  AlexnetNode: { icon: 'image', label: 'AlexNet',disableOnTraining: true },
  VggNode: { icon: 'image', label: 'Vgg',disableOnTraining: true },
  SegmentationNode: { icon: 'polygon-new', label: 'Segmentation', disableOnTraining: true }
};
