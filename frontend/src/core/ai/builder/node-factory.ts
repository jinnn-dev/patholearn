import { INode } from './serializable';

import * as Nodes from './nodes';
import { Presets } from 'rete-vue-render-plugin';
import { ClassicPreset } from 'rete';
import { Node } from './nodes/node';
import { NodeType } from './nodes/types';

function getNodeClass(nodeType: NodeType) {
  const nodes = Object.entries(Nodes);
  const index = nodes.find((entry) => entry[0] === nodeType);
  if (index) {
    return index[1];
  }
  return undefined;
}

export function parseNode(nodeData: INode) {
  const nodeClass = getNodeClass(nodeData._type as NodeType);

  let node;
  if (nodeClass) {
    const socket = new ClassicPreset.Socket(nodeData.socket);
    node = new nodeClass(socket);
  } else {
    node = new Presets.classic.Node();
  }

  node.id = nodeData.id;
  node.parse(nodeData);

  return node;
}

export function createNodeInstance(node: NodeType, socket: ClassicPreset.Socket) {
  const nodeClass = getNodeClass(node);
  if (!nodeClass) {
    return undefined;
  }
  const instance = new nodeClass(socket);
  instance.addElements();
  return instance;
}
