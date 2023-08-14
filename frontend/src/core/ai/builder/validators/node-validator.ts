import { NodeEditor } from 'rete';
import { NodeClassesType, NodeType } from '../nodes/types';
import { Schemes } from '../use-editor';
import { getNodeByType, nodeTypeExists } from '../editor-utils';
import { addNotification } from '../../../../utils/notification-state';
import { NodeValidation, ValidationItems } from './validation-settings';

export function nodeCanBeCreated(node: NodeClassesType, editor: NodeEditor<Schemes>) {
  const validationElement = NodeValidation[node.type];
  if (!validationElement) {
    return true;
  }
  return checkNodeIsUnique(node, validationElement, editor);
}

function checkNodeIsUnique(node: NodeClassesType, validationElement: ValidationItems, editor: NodeEditor<Schemes>) {
  const nodeExits = nodeTypeExists(node.type, editor);

  if (validationElement.unique && nodeExits) {
    addNotification({
      header: 'Not possible',
      detail: `Only one ${node.label} node can exist!`,
      level: 'warning',
      showDate: false,
      timeout: 10000
    });
    return false;
  }

  return true;
}

export function validateMustExist(nodeType: NodeType, editor: NodeEditor<Schemes>) {
  const nodeExists = getNodeByType('OutputNode', editor);
  if (!nodeExists) {
    addNotification({
      header: 'Node missing!',
      detail: `${nodeType} node must exist!`,
      level: 'error',
      showDate: false,
      timeout: 10000
    });
    return false;
  }
  return true;
}

export function graphHasValidDatasetNode(editor: NodeEditor<Schemes>) {
  const datasetNode = getNodeByType('DatasetNode', editor);
  if (!datasetNode) {
    return false;
  }
  const selectedValue = (datasetNode.controls as any)['dataset'].value;

  return selectedValue !== undefined && selectedValue !== null;
}

export function validateNodes(editor: NodeEditor<Schemes>) {
  return graphHasValidDatasetNode(editor) && validateMustExist('OutputNode', editor);
}
