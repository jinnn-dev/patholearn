import { IconNames } from '../../../../icons';
import { NodeType } from './nodes/types';

export type EventName = 'arrange' | 'center' | 'save' | 'clear' | 'parse' | NodeType;

interface EventSettingItem {
  icon: IconNames;
  label: string;
  divider?: boolean;
}

type EventSetting = Record<EventName, EventSettingItem>;

export const eventSettings: EventSetting = {
  arrange: { icon: 'layout', label: 'Arrange', divider: true },
  parse: { icon: 'brain', label: 'parse' },
  center: { icon: 'arrow-counter-clockwise', label: 'Center' },
  save: { icon: 'floppy-disk', label: 'Save' },
  clear: { icon: 'broom', label: 'Clear' },
  DatasetNode: { icon: 'images', label: 'Dataset', divider: true },
  Conv2DNode: { icon: 'stack', label: 'Conv2D', divider: true },
  LinearNode: { icon: 'cards', label: 'Linear' },
  PoolingNode: { icon: 'arrows-in', label: 'Pooling' },
  DropoutNode: { icon: 'drop-half', label: 'Dropout', divider: true },
  FlattenNode: { icon: 'dots-three-outline', label: 'Flatten' },
  BatchNormNode: { icon: 'equalizer', label: 'BatchNorm' },
  AddNode: { icon: 'arrows-merge', label: 'Add', divider: true },
  CombineNode: { icon: 'plus-circle-new', label: 'Combine' },
  OutputNode: { icon: 'flag', label: 'Output', divider: true }
};
