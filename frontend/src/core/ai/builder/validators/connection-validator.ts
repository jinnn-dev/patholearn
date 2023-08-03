import { NodeEditor } from 'rete';
import { Schemes } from '../use-editor';
import { getNodeByType } from '../editor-utils';
import { structures } from 'rete-structures';
import { addNotification } from '../../../../utils/notification-state';

export function validateConnections(editor: NodeEditor<Schemes>) {
  return validTraversal(editor);
}

export function validTraversal(editor: NodeEditor<Schemes>) {
  const datasetNode = getNodeByType('DatasetNode', editor);
  if (!datasetNode) {
    return false;
  }
  const graph = structures(editor);

  const datasetNodeOutgoers = graph.traverse.outgoers(datasetNode.id);
  const nodesConnectedToDataset = datasetNodeOutgoers.nodes();

  if (nodesConnectedToDataset.length === 0) {
    addMessage('Dataset Node must be connected to a layer or architecture!');
    return false;
  }
  const outputNode = getNodeByType('OutputNode', editor);
  if (!outputNode) {
    return false;
  }

  const outputNodeIncomers = graph.traverse.incomers(outputNode.id);
  console.log(outputNodeIncomers.nodes());

  if (outputNodeIncomers.nodes().length === 0) {
    addMessage('Output Node must be connected!');
    return false;
  }

  return true;
}

function addMessage(warningMessage: string) {
  addNotification({
    header: 'Invalid!',
    detail: warningMessage,
    level: 'error',
    showDate: false,
    timeout: 10000
  });
}
