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
  height = 405;

  constructor(socket: ClassicPreset.Socket) {
    super('Output', socket);
  }

  public addElements(): void {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addControl('optimizer', new DropdownControl(['SGD', 'RMSprop', 'Adagrad', 'Adam'], 'Optimizer', 'optimizer'));
    this.addControl(
      'loss',
      new DropdownControl(['Cross-Entropy', 'MAE (L1)', 'MSE', 'Hinge', 'Adam', 'NLL'], 'Loss Function', 'loss')
    );
    this.addControl('learningRate', new NumberControl(0, 10, 'Learning Rate', '0,00', 0.01));
    this.addControl('epochs', new NumberControl(0, 10000, 'Epochs', '10', 10));
    this.addControl('batchSize', new NumberControl(0, 10000, 'Batch Size', '32', 32));
  }
}