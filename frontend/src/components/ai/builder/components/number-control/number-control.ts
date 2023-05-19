import { ClassicPreset } from 'rete';

export class NumberControl extends ClassicPreset.Control {
  constructor(
    public value: number,
    public min: number,
    public max: number,
    public placeholder: string,
    public onChange = (value: number) => {
      this.value = value;
    }
  ) {
    super();
  }
}
