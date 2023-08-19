import { ClassicPreset } from 'rete';
import { MetricControl, MetricDisplayName } from '../../controls';
import { INode } from '../../serializable';
import { Socket } from '../../sockets/socket';
import { Node } from '../node';
import { ConditionalDatasetMap } from '../../../../../model/ai/datasets/dataset';

export interface IMetricNode extends INode {}

export class MetricNode extends Node<IMetricNode, { in: Socket }, {}, { metric: MetricControl }> {
  width = 250;
  height = 250;

  constructor() {
    super('Metric', 'MetricNode', { input: 'Metric' });
  }

  public duplicate(): MetricNode {
    const node = new MetricNode();
    for (const [key, control] of Object.entries(this.controls)) {
      // @ts-ignore
      node.controls[key] = control.duplicate();
    }
    node.addInput('in', new ClassicPreset.Input(node.sockets.input!, 'in'));
    return node;
  }

  public addElements(...value: any[]): void {
    this.addInput('in', new ClassicPreset.Input(this.sockets.input!, 'in'));

    const metricMap: ConditionalDatasetMap<MetricDisplayName> = {
      classification: [
        'Epoch',
        'Loss',
        'Accuracy',
        'ROC AUC',
        'Average Precision',
        'Cohen Kappa',
        'F1 Score',
        'Precision'
      ],
      detection: ['Accuracy', 'F1 Score', 'IOU', 'Precision'],
      segmentation: ['Epoch', 'Loss', 'Accuracy', 'F1 Score', 'IOU', 'Precision', 'Epoch']
    };
    this.addControl('metric', new MetricControl('metric', metricMap, value[0] || undefined));
  }
}
