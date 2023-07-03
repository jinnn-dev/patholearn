import {
  NodeType,
  isArchitectureType,
  isCombineType,
  isInputType,
  isLayerType,
  isMetricType,
  isOutputTpye,
  isTransformType
} from './nodes/types';

const LAYER_COLOR = 'sky-700';
const TRANSFORM_COLOR = 'purple-800';
const INPUT_COLOR = 'emerald-800';
const OUTPUT_COLOR = 'rose-800';
const COMBINE_COLOR = 'amber-700';
const METRIC_COLOR = 'indigo-800';
const ARCHITECTURE_COLOR = 'fuchsia-600';

export function getNodeColor(nodeType: NodeType) {
  if (isLayerType(nodeType)) {
    return LAYER_COLOR;
  }
  if (isTransformType(nodeType)) {
    return TRANSFORM_COLOR;
  }
  if (isInputType(nodeType)) {
    return INPUT_COLOR;
  }

  if (isOutputTpye(nodeType)) {
    return OUTPUT_COLOR;
  }

  if (isCombineType(nodeType)) {
    return COMBINE_COLOR;
  }

  if (isMetricType(nodeType)) {
    return METRIC_COLOR;
  }

  if (isArchitectureType(nodeType)) {
    return ARCHITECTURE_COLOR;
  }
}
