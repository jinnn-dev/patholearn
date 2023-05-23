import { ClassicPreset } from 'rete';
import { INumberControl, NumberControl } from '../controls/number-control';
import { LayerType, NodeType } from '../types';
import { INode } from '../../../../core/ai/builder/serializable';
import { DimensionControl, IDimensionControl } from '../controls/dimension-control';
import { IDropdownControl } from '../controls/dropdown-control';
import { ActivationControl } from '../controls/activation-control';
import { Node } from './node';

export interface IConv2DNode extends INode {}

export class Conv2DNode extends Node<
  IConv2DNode,
  { in: ClassicPreset.Socket },
  { out: ClassicPreset.Socket },
  {
    filters: NumberControl;
    kernel: DimensionControl;
    stride: DimensionControl;
    activation: ActivationControl;
  }
> {
  width = 200;
  height = 310;

  constructor(socket: ClassicPreset.Socket, public type: NodeType = 'Layer', public layerType: LayerType = 'Conv2D') {
    super('Conv2D', socket);
  }

  static create(socket: ClassicPreset.Socket) {
    const layer = new Conv2DNode(socket);
    layer.addDefault();
    return layer;
  }

  public addDefault() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));

    this.addControl('filters', new NumberControl(0, 128, 'Filters', 'Filters'));
    this.addControl(
      'kernel',
      new DimensionControl('Kernel', { min: 0, max: 128, placeholder: 'x' }, { min: 0, max: 128, placeholder: 'y' })
    );
    this.addControl(
      'stride',
      new DimensionControl('Stride', { min: 0, max: 128, placeholder: 'x' }, { min: 0, max: 128, placeholder: 'y' })
    );
    this.addControl('activation', new ActivationControl());
  }

  public static parse(data: IConv2DNode): Conv2DNode {
    const socket = new ClassicPreset.Socket(data.socket);
    const node = new Conv2DNode(socket);
    for (const input of data.inputs) {
      node.addInput(input.key as 'in', new ClassicPreset.Input(socket, 'in'));
    }
    for (const output of data.outputs) {
      node.addOutput(output.key as 'out', new ClassicPreset.Output(socket, 'out'));
    }

    for (const control of data.controls) {
      let controlInstance: DimensionControl | NumberControl | ActivationControl;

      if ('xOptions' in control) {
        let data = control as IDimensionControl;
        controlInstance = DimensionControl.parse(data);
      } else if (control._type === ActivationControl.name) {
        controlInstance = ActivationControl.parse(control as IDropdownControl);
      } else {
        let data = control as INumberControl;
        controlInstance = NumberControl.parse(data);
      }
      node.addControl(control.key as 'filters' | 'kernel' | 'stride' | 'activation', controlInstance);
    }

    return node;
  }
}
