import { INode } from './serializable';

import * as Nodes from './nodes';
import { Presets } from 'rete-vue-render-plugin';

export function parseNode(nodeData: INode) {
  const nodes = Object.entries(Nodes);
  const index = nodes.find((entry) => entry[0] === nodeData._type);
  let node;
  if (index) {
    node = index[1].parse(nodeData);
  } else {
    node = new Presets.classic.Node();
  }
  node.id = nodeData.id;
  return node;
}
