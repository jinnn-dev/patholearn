import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { Node } from '../node';
import { ConditionalDropdownControl, DropdownControl, NumberControl } from '../../controls';
import { Socket } from '../../sockets/socket';
import { ConditionalDatasetMap } from '../../../../../model/ai/datasets/dataset';

export interface IOutputNode extends INode {}

export class OutputNode extends Node<
  IOutputNode,
  { in: Socket },
  { metrics: Socket },
  {
    optimizer: ConditionalDropdownControl;
    loss: ConditionalDropdownControl;
    learningRate: NumberControl;
    epochs: NumberControl;
    batchSize: NumberControl;
  }
> {
  width = 250;

  constructor() {
    super('Output', 'OutputNode', { input: 'All', output: 'Metric' });
  }

  public duplicate(): OutputNode {
    const node = new OutputNode();
    for (const [key, control] of Object.entries(this.controls)) {
      // @ts-ignore
      node.controls[key] = control.duplicate();
    }
    node.addInput('in', new ClassicPreset.Input(node.sockets.input!, 'in'));
    node.addOutput('metrics', new ClassicPreset.Output(node.sockets.output!, 'metrics'));
    return node;
  }

  public addElements(): void {
    this.addInput('in', new ClassicPreset.Input(this.sockets.input!, 'in'));
    this.addOutput('metrics', new ClassicPreset.Output(this.sockets.output!, 'metrics'));

    const optimizerMap: ConditionalDatasetMap<string> = {
      classification: ['Adam', 'SGD', 'RMSprop', 'Adagrad'],
      detection: ['SGD'],
      segmentation: ['SGD']
    };

    this.addControl('optimizer', new ConditionalDropdownControl('Optimizer', 'optimizer', optimizerMap));

    const lossMap: ConditionalDatasetMap<string> = {
      classification: ['Cross-Entropy'],
      detection: ['Jaccard', 'Dice'],
      segmentation: ['Jaccard', 'Dice']
    };

    this.addControl('loss', new ConditionalDropdownControl('Loss Function', 'loss', lossMap));
    this.addControl('learningRate', new NumberControl(0, 10, 'Learning Rate', '0,00', 0.001));
    this.addControl('epochs', new NumberControl(0, 10000, 'Epochs', '10', 30));
    this.addControl('batchSize', new NumberControl(0, 10000, 'Batch Size', '32', 16));
  }
}
