import { ClassicPreset } from 'rete';
import { DropdownControl } from '../../controls';
import { INode } from '../../serializable';
import { Socket } from '../../sockets/socket';
import { Node } from '../node';
import { SegmentationEcoderVersions, SegmentationModelVersions } from './versions';

export interface ISegmentationNode extends INode {}

export class SegmentationNode extends Node<
  ISegmentationNode,
  { dataset: Socket },
  { output: Socket },
  { model: DropdownControl; encoder: DropdownControl }
> {
  width = 220;

  constructor() {
    super('Segmentation', 'SegmentationNode', { input: '2D', output: 'Output' });
  }

  public duplicate(): SegmentationNode {
    const node = new SegmentationNode();
    for (const [key, control] of Object.entries(this.controls)) {
      // @ts-ignore
      node.controls[key] = control.duplicate();
    }
    node.sockets = this.sockets;
    node.addInput('dataset', new ClassicPreset.Input(node.sockets.input!, 'dataset'));
    node.addOutput('output', new ClassicPreset.Output(node.sockets.output!, 'output'));
    return node;
  }

  public addElements(value?: any): void {
    this.addInput('dataset', new ClassicPreset.Input(this.sockets.input!, 'dataset'));
    this.addOutput('output', new ClassicPreset.Output(this.sockets.output!, 'output'));
    this.addControl('model', new DropdownControl(SegmentationModelVersions, 'Model', 'model', value || 'UNet'));
    this.addControl(
      'encoder',
      new DropdownControl(SegmentationEcoderVersions, 'Encoder', 'encoder', value || 'resnet18')
    );
  }
}
