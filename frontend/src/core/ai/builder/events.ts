import { IconNames } from '../../../../icons';
import { NodeType } from './nodes/types';

export type EventName = 'arrange' | 'center' | 'save' | 'clear' | NodeType;

interface EventSettingItem {
  icon: IconNames;
  label: string;
  divider?: boolean;
}

type EventSetting = Record<EventName, EventSettingItem>;

export const eventSettings: EventSetting = {
  arrange: { icon: 'layout', label: 'Arrange' },
  center: { icon: 'arrow-counter-clockwise', label: 'Center' },
  save: { icon: 'floppy-disk', label: 'Save' },
  clear: { icon: 'broom', label: 'Clear', divider: true },
  DatasetNode: { icon: 'images', label: 'Dataset', divider: true },
  Conv2DNode: { icon: 'stack', label: 'Conv2D' },
  LinearNode: { icon: 'cards', label: 'Linear' },
  PoolingNode: { icon: 'arrows-in', label: 'Pooling', divider: true },
  DropoutNode: { icon: 'drop-half', label: 'Dropout' },
  FlattenNode: { icon: 'dots-three-outline', label: 'Flatten' },
  BatchNormNode: { icon: 'equalizer', label: 'BatchNorm', divider: true },
  OutputNode: { icon: 'flag', label: 'Output' }
};
