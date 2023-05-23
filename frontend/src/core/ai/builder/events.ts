import { IconNames } from '../../../../icons';
import { NodeType } from './nodes/types';

export type EventName = 'arrange' | 'center' | 'save' | NodeType;

interface EventSettingItem {
  icon: IconNames;
  label: string;
}

type EventSetting = Record<EventName, EventSettingItem>;

export const eventSettings: EventSetting = {
  arrange: { icon: 'layout', label: 'Arrange' },
  center: { icon: 'arrow-counter-clockwise', label: 'Center' },
  save: { icon: 'floppy-disk', label: 'Save' },
  DatasetNode: { icon: 'images', label: 'Dataset' },
  Conv2DNode: { icon: 'stack', label: 'Conv2D' },
  LinearNode: { icon: 'cards', label: 'Linear' },
  DropoutNode: { icon: 'drop-half', label: 'Dropout' },
  FlattenNode: { icon: 'dots-three-outline', label: 'Flatten' },
  BatchNormNode: { icon: 'equalizer', label: 'BatchNorm' },
  PoolingNode: { icon: 'arrows-in', label: 'Pooling' },
  OutputNode: { icon: 'flag', label: 'Output' }
};
