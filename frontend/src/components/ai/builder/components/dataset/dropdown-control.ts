import { ClassicPreset } from 'rete';

export class DropdownControl extends ClassicPreset.Control {
  constructor(public values: any[], public label: string) {
    super();
  }
}
