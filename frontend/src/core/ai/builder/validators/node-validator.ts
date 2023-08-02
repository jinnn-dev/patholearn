import { NodeEditor } from 'rete';
import { NodeClassesType, NodeType } from '../nodes/types';
import { Schemes } from '../use-editor';
import { nodeTypeExists } from '../editor-utils';
import { addNotification } from '../../../../utils/notification-state';

interface ValidationItems {
  unique?: boolean;
}

const NodeValidation: { [type in NodeType]?: ValidationItems } = {
  DatasetNode: {
    unique: true
  },
  OutputNode: {
    unique: true
  },
  ResNetNode: {
    unique: true
  }
};

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
      header: 'Nicht möglich',
      detail: `Es kann nur einen ${node.label} Node geben!`,
      level: 'warning',
      showDate: false,
      timeout: 10000
    });
    return false;
  }

  return true;
}

export function graphHasValidDatasetNode(editor: NodeEditor<Schemes>) {
  const datasetNode = editor.getNodes().find((node) => node.type === 'DatasetNode');
  const selectedValue = (datasetNode?.controls as any)['dataset'].value;

  return selectedValue !== undefined && selectedValue !== null;
}

export function validateNodes(editor: NodeEditor<Schemes>) {
  return graphHasValidDatasetNode(editor);
}
