import { ClassicPreset } from 'rete';
import { INumberControl, NumberControl } from './number-control/number-control';
import { LayerType, NodeType } from './types';
import { IInputControl, INode, Serializable, serializeControl, serializePort } from '../serializable';
import { DimensionControl, IDimensionControl } from './dimension-control/dimension-control';
import { DropdownControl, IDropdownControl } from './dropdown-control/dropdown-control';

export interface IPoolingNode extends INode {}

export class PoolingNode
  extends ClassicPreset.Node<
    { in: ClassicPreset.Socket },
    { out: ClassicPreset.Socket },
    {
      kernel: DimensionControl;
      stride: DimensionControl;
      type: DropdownControl;
    }
  >
  implements Serializable<PoolingNode, IPoolingNode>
{
  width = 200;
  height = 265;

  private socket: ClassicPreset.Socket;
  constructor(
    socket: ClassicPreset.Socket,
    public type: NodeType = 'Transform',
    public layerType: LayerType = 'Pooling'
  ) {
    super('Pooling');
    this.socket = socket;
  }

  static create(socket: ClassicPreset.Socket) {
    const layer = new PoolingNode(socket);
    layer.addDefault();
    return layer;
  }

  public addDefault() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));

    this.addControl(
      'kernel',
      new DimensionControl('Kernel', { min: 0, max: 128, placeholder: 'x' }, { min: 0, max: 128, placeholder: 'y' })
    );
    this.addControl(
      'stride',
      new DimensionControl('Stride', { min: 0, max: 128, placeholder: 'x' }, { min: 0, max: 128, placeholder: 'y' })
    );
    this.addControl('type', new DropdownControl(['max', 'average'], 'Type', 'type'));
  }

  public static parse(data: IPoolingNode): PoolingNode {
    const socket = new ClassicPreset.Socket(data.socket);
    const node = new PoolingNode(socket);
    for (const input of data.inputs) {
      node.addInput(input.key as 'in', new ClassicPreset.Input(socket, 'in'));
    }
    for (const output of data.outputs) {
      node.addOutput(output.key as 'out', new ClassicPreset.Output(socket, 'out'));
    }

    for (const control of data.controls) {
      let controlInstance: DimensionControl | NumberControl | DropdownControl;

      if ('xOptions' in control) {
        let data = control as IDimensionControl;
        controlInstance = DimensionControl.parse(data);
      } else {
        controlInstance = DropdownControl.parse(control as IDropdownControl);
      }
      node.addControl(control.key as 'kernel' | 'stride' | 'type', controlInstance);
    }

    return node;
  }

  public serialize(): IPoolingNode {
    const inputs = Object.entries(this.inputs).map(([key, input]) => serializePort(key, input));
    const outputs = Object.entries(this.outputs).map(([key, input]) => serializePort(key, input));
    const controls = Object.entries(this.controls).map(([key, input]) => input.serialize(key));

    return {
      id: this.id,
      _type: PoolingNode.name,
      label: this.label,
      inputs: inputs,
      outputs: outputs,
      controls: controls,
      socket: this.socket.name
    };
  }
}
