import { ClassicPreset } from 'rete';
import { INumberControl, NumberControl } from '../controls/number-control';
import { INode } from '../../../../core/ai/builder/serializable';
import { LayerType, NodeType } from '../types';
import { DropdownControl, IDropdownControl } from '../controls/dropdown-control';
import { ActivationControl } from '../controls/activation-control';
import { Node } from './node';

export interface ILinearNode extends INode {}

export class LinearNode extends Node<
  ILinearNode,
  { in: ClassicPreset.Socket },
  { out: ClassicPreset.Socket },
  {
    neurons: NumberControl;
    activation: DropdownControl;
  }
> {
  width = 200;
  height = 220;

  constructor(socket: ClassicPreset.Socket, public type: NodeType = 'Layer', public layerType: LayerType = 'Linear') {
    super('Linear', socket);
  }

  static create(socket: ClassicPreset.Socket) {
    const layer = new LinearNode(socket);
    layer.addDefault();
    return layer;
  }

  public addDefault() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));
    this.addControl('neurons', new NumberControl(0, 2048, 'Neurons', 'neurons'));
    this.addControl('activation', new ActivationControl());
  }

  public static parse(data: ILinearNode): LinearNode {
    const socket = new ClassicPreset.Socket(data.socket);
    const node = new LinearNode(socket);
    for (const input of data.inputs) {
      node.addInput(input.key as 'in', new ClassicPreset.Input(socket, 'in'));
    }
    for (const output of data.outputs) {
      console.log(Object.keys(ClassicPreset));

      node.addOutput(output.key as 'out', new ClassicPreset.Output(socket, 'out'));
    }

    for (const control of data.controls) {
      let controlInstance: NumberControl | ActivationControl;
      if (control._type === ActivationControl.name) {
        controlInstance = ActivationControl.parse(control as IDropdownControl);
      } else {
        controlInstance = NumberControl.parse(control as INumberControl);
      }

      node.addControl(control.key as 'neurons' | 'activation', controlInstance);
    }

    return node;
  }

  // public serialize(key?: string | undefined): ILinearNode {
  //   const inputs = Object.entries(this.inputs).map(([key, input]) => serializePort(key, input));
  //   const outputs = Object.entries(this.outputs).map(([key, input]) => serializePort(key, input));
  //   const controls = Object.entries(this.controls).map(([key, input]) => input.serialize(key));

  //   return {
  //     id: this.id,
  //     _type: LinearNode.name,
  //     label: this.label,
  //     inputs: inputs,
  //     outputs: outputs,
  //     controls: controls,
  //     socket: this.socket.name
  //   };
  // }
}
