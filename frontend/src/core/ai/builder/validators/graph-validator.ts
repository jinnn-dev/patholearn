import { NodeEditor } from 'rete';
import { Schemes } from '../use-editor';
import { getNodeByType } from '../editor-utils';

export function validateEditor(editor: NodeEditor<Schemes>) {
  return validConnections(editor);
}

export function validConnections(editor: NodeEditor<Schemes>) {
  const datasetNode = getNodeByType('DatasetNode', editor);

  console.log(editor.getConnections());
  return false;
}
