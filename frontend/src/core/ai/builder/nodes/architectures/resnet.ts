import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { Socket } from '../../sockets/socket';
import { Node } from '../node';
import { DropdownControl } from '../../controls';

export const ResnetVersions = ['resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152'];

export interface IResnetNode extends INode {}

export class ResNetNode extends Node<
  IResnetNode,
  { dataset: Socket },
  { fc: Socket },
  { version: DropdownControl; pretrained: DropdownControl }
> {
  width = 180;

  constructor() {
    super('ResNet', 'ResNetNode', { input: '2D', output: 'Linear' });
  }

  public duplicate(): ResNetNode {
    const node = new ResNetNode();
    for (const [key, control] of Object.entries(this.controls)) {
      // @ts-ignore
      node.controls[key] = control.duplicate();
    }
    node.sockets = this.sockets;
    node.addInput('dataset', new ClassicPreset.Input(node.sockets.input!, 'in'));
    node.addOutput('fc', new ClassicPreset.Output(node.sockets.output!, 'fc'));
    return node;
  }

  public addElements(value?: any): void {
    this.addInput('dataset', new ClassicPreset.Input(this.sockets.input!, 'dataset'));
    this.addOutput('fc', new ClassicPreset.Output(this.sockets.output!, 'fc'));
    this.addControl('version', new DropdownControl(ResnetVersions, 'Version', 'version', value || 'resnet18'));
    this.addControl(
      'pretrained',
      new DropdownControl(['General', 'Medical', 'No'], 'Pretrained', 'pretrained', 'General')
    );
  }
}
