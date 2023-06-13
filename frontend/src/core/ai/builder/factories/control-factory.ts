import { IControl } from '../serializable';
import * as Controls from '../controls';
import { ClassicPreset } from 'rete';

export function parseControl<T>(controlData: T extends IControl ? any : any) {
  const nodes = Object.entries(Controls);
  const index = nodes.find((entry) => entry[0] === controlData.type);

  let control;
  if (index) {
    control = index[1].parse(controlData);
  } else {
    control = new ClassicPreset.Control();
  }

  control!.id = controlData.id;
  return control;
}
