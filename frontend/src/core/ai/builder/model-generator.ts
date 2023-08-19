import { ClassicPreset, NodeEditor } from 'rete';
import { ConnProps, NodeProps, Schemes } from './use-editor';
import { Dataset } from 'model/ai/datasets/dataset';
import { createNodeInstance } from './factories/node-factory';
import { builderState } from './state';
import { omitSyncEvents } from './editor-utils';
import { DatasetNode, MetricNode, OutputNode, ResNetNode, SegmentationNode } from './nodes';
import { MetricDisplayName } from './controls';
export type ModelComplexity = 'low' | 'medium' | 'high';

const ComplexityToVersion: { [key in ModelComplexity]: string } = {
  low: 'resnet18',
  medium: 'resnet50',
  high: 'resnet101'
};

const SegmentationComplexityToVersion: { [key in ModelComplexity]: string } = {
  low: 'timm-efficientnet-b3',
  medium: 'resnet34',
  high: 'timm-efficientnet-b8'
};

export async function generateModel(
  editor: NodeEditor<Schemes>,
  selectedDataset: Dataset,
  complexity: ModelComplexity
) {
  return await omitSyncEvents(generateNodes, editor, selectedDataset, complexity);
}

async function generateNodes(editor: NodeEditor<Schemes>, selectedDataset: Dataset, complexity: ModelComplexity) {
  const dataset = createNodeInstance('DatasetNode', selectedDataset) as DatasetNode;
  await editor.addNode(dataset);
  builderState.selectedDatasset = dataset.controls.dataset.value;

  const outputNode = createNodeInstance('OutputNode') as OutputNode;
  await editor.addNode(outputNode);

  let architectureNode: ResNetNode | SegmentationNode;
  let outputConnectionKey: 'fc' | 'output';

  let metrics: MetricDisplayName[] = ['Epoch', 'Loss'];
  if (selectedDataset.dataset_type === 'classification') {
    architectureNode = createNodeInstance('ResNetNode', ComplexityToVersion[complexity]) as ResNetNode;
    outputConnectionKey = 'fc';
    metrics.push('Accuracy');
  } else {
    architectureNode = createNodeInstance(
      'SegmentationNode',
      'Unet++',
      SegmentationComplexityToVersion[complexity]
    ) as SegmentationNode;
    outputConnectionKey = 'output';
    metrics.push('IOU');
  }

  await editor.addNode(architectureNode);

  await editor.addConnection(
    new ClassicPreset.Connection(dataset, 'dataset', architectureNode, 'dataset') as ConnProps
  );

  await editor.addConnection(
    new ClassicPreset.Connection(architectureNode, outputConnectionKey as never, outputNode, 'in') as ConnProps
  );
  await builderState.area?.translate(architectureNode.id, { x: -200, y: 0 });
  await builderState.area?.translate(dataset.id, { x: -600, y: 0 });
  await builderState.area?.translate(outputNode.id, { x: 200, y: 0 });

  for (let i = 0; i < metrics.length; i++) {
    const metricNode = createMetricNode(metrics[i]);
    await editor.addNode(metricNode);
    await builderState.area?.translate(metricNode.id, { x: 600, y: -metricNode.height + i * (metricNode.height + 50) });
    await editor.addConnection(new ClassicPreset.Connection(outputNode, 'metrics', metricNode, 'in') as ConnProps);
  }
}

function createMetricNode(metric: MetricDisplayName): MetricNode {
  const metricNode = createNodeInstance('MetricNode', metric);
  return metricNode as MetricNode;
}
