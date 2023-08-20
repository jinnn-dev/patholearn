import { Node } from '../nodes/node';
import { NodeClassesType } from '../nodes/types';
import { addNotification } from '../../../../utils/notification-state';
import { ConnectionMatrix } from '../sockets/socket';
import { DatasetNode } from '../nodes';
import { Dataset } from 'model/ai/datasets/dataset';
import { NodeValidation } from './validation-settings';

export function nodesCanConnect(source: NodeClassesType, target: NodeClassesType): boolean {
  if (target.type === 'ResNetNode' && source.type !== 'DatasetNode') {
    newSocketNotification(`Only a dataset node can be connected with a ${target.label} node`);
    return false;
  }

  if (source.type === 'DatasetNode') {
    const datasetNode = source as DatasetNode;
    const selectedDataset = datasetNode.controls.dataset.value as Dataset | undefined;
    if (!selectedDataset) {
      newSocketNotification('You must select a dataset first');
      return false;
    }

    const nodeInputDatasetType = NodeValidation[target.type]?.datasetType;
    if (selectedDataset.dataset_type !== nodeInputDatasetType) {
      newSocketNotification(
        `You can only connect ${nodeInputDatasetType} datasets to a ${target.label} Node. The selected dataset is a ${selectedDataset.dataset_type} dataset`
      );
      return false;
    }
  }

  if (target.type === 'OutputNode' && source.type === 'DatasetNode') {
    newSocketNotification('A dataset node can not be connected to an output node. Add layers in between.');
    return false;
  }

  if (source.sockets.output && target.sockets.input) {
    const possibleConnections = ConnectionMatrix[source.sockets.output.type];
    if (!possibleConnections) return false;
    if (!possibleConnections.includes(target.sockets.input.type)) {
      newSocketNotification(getWarningMessage(source, target));
      return false;
    }
    return true;
  }
  return false;
}

function newSocketNotification(warningMessage: string) {
  addNotification({
    header: 'Not possible!',
    detail: warningMessage,
    level: 'warning',
    showDate: false,
    timeout: 10000
  });
}

export function getWarningMessage(sourceNode: NodeClassesType, targetNode: NodeClassesType) {
  const sourceType = sourceNode.sockets.output?.type;
  const targetType = targetNode.sockets.input?.type;

  if (sourceType === '2D' && targetType === 'Linear') {
    return `A ${targetNode.label} node can only process linear data. A Flatten node has to be added.`;
  }

  if (sourceType === 'Linear' && targetType === '2D') {
    return `A ${sourceNode.label} node outputs linear data. The ${targetNode.label} node only processes 2D data.`;
  }

  return `A connection between a ${sourceNode.label} node and a ${targetNode.label} node is not possible.`;
}
