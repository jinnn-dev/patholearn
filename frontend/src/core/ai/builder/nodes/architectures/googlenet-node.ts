import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { Socket } from '../../sockets/socket';
import { DropdownControl } from '../../controls';
import { VggVersions } from './versions';
import { ArchitectureNode } from './architecture-node';

export interface IGoogleNetNode extends INode {}

export class GoogleNetNode extends ArchitectureNode<
  IGoogleNetNode,
  { dataset: Socket },
  { fc: Socket },
  { pretrained: DropdownControl }
> {
  width = 180;

  constructor() {
    super('GoogLeNet', 'GoogleNetNode', { input: '2D', output: 'Linear' });
  }

  public duplicate(): GoogleNetNode {
    const node = new GoogleNetNode();
    for (const [key, control] of Object.entries(this.controls)) {
      // @ts-ignore
      node.controls[key] = control.duplicate();
    }
    node.sockets = this.sockets;
    node.addInput('dataset', new ClassicPreset.Input(node.sockets.input!, 'in'));
    node.addOutput('fc', new ClassicPreset.Output(node.sockets.output!, 'fc'));
    return node;
  }

  public addElements(...value: any[]): void {
    this.addInput('dataset', new ClassicPreset.Input(this.sockets.input!, 'dataset'));
    this.addOutput('fc', new ClassicPreset.Output(this.sockets.output!, 'fc'));
    this.addControl('pretrained', new DropdownControl(['General', 'No'], 'Pretrained', 'pretrained', 'General'));
  }
}
