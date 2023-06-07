import { INode } from '../serializable';

import * as Nodes from '../nodes';
import { Presets } from 'rete-vue-render-plugin';
import { ClassicPreset } from 'rete';
import { NodeType } from '../nodes/types';
import { builderState, getLockedBy } from '../state';
import { NodeProps } from '../use-editor';

function getNodeClass(nodeType: NodeType) {
  const nodes = Object.entries(Nodes);
  const index = nodes.find((entry) => entry[0] === nodeType);
  if (index) {
    return index[1];
  }
  return undefined;
}

export function parseNode(nodeData: INode) {
  const nodeClass = getNodeClass(nodeData.type as NodeType);

  let node;
  if (nodeClass) {
    const socket = new ClassicPreset.Socket(nodeData.socket);
    node = new nodeClass(socket);
  } else {
    node = new Presets.classic.Node();
  }

  node.id = nodeData.id;
  const lockedBy = getLockedBy(node.id);
  const externalLock = lockedBy?.id !== builderState.me?.id;
  let lockedControl = undefined;
  if (builderState.task?.lockStatus) {
    for (const elementId of Object.keys(builderState.task.lockStatus)) {
      const control = node.getControl(elementId);
      if (control) {
        lockedControl = control.id;
      }
    }
  }
  node.parse(nodeData);

  cacheControlsMapping(node);

  if (lockedBy) {
    node.lock({
      lockedBy: lockedBy,
      externalLock: externalLock,
      controlId: lockedControl
    });
  }

  return node;
}

export function createNodeInstance(node: NodeType, socket: ClassicPreset.Socket) {
  const nodeClass = getNodeClass(node);
  if (!nodeClass) {
    return undefined;
  }
  const instance = new nodeClass(socket);
  instance.addElements();
  cacheControlsMapping(instance as NodeProps);
  return instance;
}

export function cacheControlsMapping(node: NodeProps) {
  for (const control of Object.values(node.controls)) {
    if (control) {
      builderState.controlToNode.set((control as any).id, node);
    }
  }
}
