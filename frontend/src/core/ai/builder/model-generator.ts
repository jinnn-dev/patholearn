import { ClassicPreset, NodeEditor } from 'rete';
import { NodeProps, Schemes } from './use-editor';
import { Dataset } from 'model/ai/datasets/dataset';
import { createNodeInstance } from './factories/node-factory';
import { ResnetVersions } from './nodes';
import { builderState } from './state';
import { omitSyncEvents } from './editor-utils';

export type ModelComplexity = 'low' | 'medium' | 'high';

const ComplexityToVersion: { [key in ModelComplexity]: string } = {
  low: 'resnet18',
  medium: 'resnet50',
  high: 'resnet101'
};

export async function generateModel(
  editor: NodeEditor<Schemes>,
  selectedDataset: Dataset,
  complexity: ModelComplexity
) {
  return await omitSyncEvents(generateNodes, editor, selectedDataset, complexity);
}

async function generateNodes(editor: NodeEditor<Schemes>, selectedDataset: Dataset, complexity: ModelComplexity) {
  const dataset = createNodeInstance('DatasetNode', selectedDataset);
  const resnetNode = createNodeInstance('ResNetNode', ComplexityToVersion[complexity]);
  const outputNode = createNodeInstance('OutputNode');

  await editor.addNode(dataset as NodeProps);
  await editor.addNode(resnetNode);
  await editor.addNode(outputNode);
  await editor.addConnection(new ClassicPreset.Connection(dataset, 'dataset', resnetNode, 'dataset'));
  await editor.addConnection(new ClassicPreset.Connection(resnetNode, 'fc', outputNode, 'in'));

  await builderState.area?.translate(dataset.id, { x: -400, y: 0 });
  await builderState.area?.translate(resnetNode.id, { x: 0, y: 0 });
  await builderState.area?.translate(outputNode.id, { x: 400, y: 0 });
}
