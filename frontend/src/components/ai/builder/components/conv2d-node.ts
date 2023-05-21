import { ClassicPreset } from 'rete';
import { INumberControl, NumberControl } from './number-control/number-control';
import { LayerType, NodeType } from './types';
import { IInputControl, INode, Serializable, serializeControl, serializePort } from '../serializable';
import { DimensionControl, IDimensionControl } from './dimension-control/dimension-control';
import { DropdownControl, IDropdownControl } from './dropdown-control/dropdown-control';
import { ActivationControl } from './activation-control';

export interface IConv2DNode extends INode {}

export class Conv2DNode
  extends ClassicPreset.Node<
    { in: ClassicPreset.Socket },
    { out: ClassicPreset.Socket },
    {
      filters: NumberControl;
      kernel: DimensionControl;
      stride: DimensionControl;
      activation: ActivationControl;
    }
  >
  implements Serializable<Conv2DNode, IConv2DNode>
{
  width = 200;
  height = 310;

  private socket: ClassicPreset.Socket;
  constructor(socket: ClassicPreset.Socket, public type: NodeType = 'Layer', public layerType: LayerType = 'Conv2D') {
    super('Conv2D');
    this.socket = socket;
  }

  static create(socket: ClassicPreset.Socket) {
    const layer = new Conv2DNode(socket);
    layer.addDefault();
    return layer;
  }

  public addDefault() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));

    this.addControl('filters', new NumberControl(0, 128, 'Filters'));
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

  public serialize(): IConv2DNode {
    const inputs = Object.entries(this.inputs).map(([key, input]) => serializePort(key, input));
    const outputs = Object.entries(this.outputs).map(([key, input]) => serializePort(key, input));
    const controls = Object.entries(this.controls).map(([key, input]) => input.serialize(key));

    return {
      id: this.id,
      _type: Conv2DNode.name,
      label: this.label,
      inputs: inputs,
      outputs: outputs,
      controls: controls,
      socket: this.socket.name
    };
  }
}
