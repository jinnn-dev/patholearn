import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { Node } from '../node';
import { DropdownControl, NumberControl } from '../../controls';

export interface IOutputNode extends INode {}

export class OutputNode extends Node<
  IOutputNode,
  { in: ClassicPreset.Socket },
  {},
  {
    optimizer: DropdownControl;
    loss: DropdownControl;
    learningRate: NumberControl;
    epochs: NumberControl;
    batchSize: NumberControl;
  }
> {
  width = 250;
  height = 350;

  constructor(socket: ClassicPreset.Socket) {
    super('Output', socket,  "OutputNode");
  }

  public duplicate(): OutputNode {
    const node = new OutputNode(this.socket);
    for (const [key, control] of Object.entries(this.controls)) {
      // @ts-ignore
      node.controls[key] = control.duplicate();
    }
    node.addInput('in', new ClassicPreset.Input(node.socket, 'in'));
    return node;
  }

  public addElements(): void {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addControl(
      'optimizer',
      new DropdownControl(['SGD', 'RMSprop', 'Adagrad', 'Adam'], 'Optimizer', 'optimizer', 'Adam')
    );
    this.addControl(
      'loss',
      new DropdownControl(
        ['Cross-Entropy', 'MAE (L1)', 'MSE', 'Hinge', 'Adam', 'NLL'],
        'Loss Function',
        'loss',
        'Cross-Entropy'
      )
    );
    this.addControl('learningRate', new NumberControl(0, 10, 'Learning Rate', '0,00', 0.01));
    this.addControl('epochs', new NumberControl(0, 10000, 'Epochs', '10', 10));
    this.addControl('batchSize', new NumberControl(0, 10000, 'Batch Size', '32', 32));
  }
}
