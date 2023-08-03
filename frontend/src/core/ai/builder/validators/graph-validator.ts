import { NodeEditor } from 'rete';
import { Schemes } from '../use-editor';
import { getNodeByType } from '../editor-utils';
import { structures } from 'rete-structures';

export function validateEditor(editor: NodeEditor<Schemes>) {
  return validConnections(editor);
}

export function validConnections(editor: NodeEditor<Schemes>) {
  const datasetNode = getNodeByType('DatasetNode', editor);
  if (!datasetNode) {
    return false;
  }
  const graph = structures(editor);
  graph.traverse.outgoers(datasetNode.id).nodes();
  console.log(graph.traverse.outgoers(datasetNode.id).nodes());
  return false;
}
