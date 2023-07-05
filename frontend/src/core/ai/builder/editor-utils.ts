import { NodeEditor } from 'rete';
import { AreaExtra, NodeProps, Schemes } from './use-editor';
import { Position } from 'rete-area-plugin/_types/types';
import { AreaPlugin } from 'rete-area-plugin';
import { builderState } from './state';
import { OutputNode } from './nodes';
import { NodeType } from './nodes/types';

export async function omitReteEvents<T, A extends unknown[]>(func: (...data: A) => Promise<T>, ...data: A) {
  builderState.omitEvents = true;
  const result = await func(...data);
  builderState.omitEvents = false;
  return result;
}

export async function removeNodeAndConnections(editor: NodeEditor<Schemes>, nodeId: string) {
  const connections = editor.getConnections().filter((c) => {
    return c.source === nodeId || c.target === nodeId;
  });
  for (const connection of connections) {
    await editor.removeConnection(connection.id);
  }
  await editor.removeNode(nodeId);
}

export async function addNodeAtPosition(
  editor: NodeEditor<Schemes>,
  area: AreaPlugin<Schemes, AreaExtra>,
  node: NodeProps,
  position: Position
) {
  await editor.addNode(node);
  await area.translate(node.id, position);
}

export async function cloneNodeAndAdd(
  editor: NodeEditor<Schemes>,
  area: AreaPlugin<Schemes, AreaExtra>,
  nodeId: string
) {
  const node = editor.getNode(nodeId);
  const duplicatedNode = node.duplicate();
  const position = area.area.pointer;
  await addNodeAtPosition(editor, area, duplicatedNode, area.area.pointer);
  return {
    clonedNode: duplicatedNode,
    position
  };
}

export function getEpochs(editor: NodeEditor<Schemes>) {
  for (const node of editor.getNodes()) {
    if (node instanceof OutputNode) {
      return node.controls['epochs'].value;
    }
  }
  return undefined;
}

export function nodeTypeExists(nodeType: NodeType, editor: NodeEditor<Schemes>) {
  return editor.getNodes().find((node) => node.type === nodeType) !== undefined;
}
