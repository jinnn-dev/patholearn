import * as Nodes from './index';
import * as Layers from './layer';
import * as Inputs from './input';
import * as Transforms from './transform';
import * as Outputs from './output';
import * as Combines from './combine';

export type LayerType = keyof typeof Layers;
export type InputType = keyof typeof Inputs;
export type TransformType = keyof typeof Transforms;
export type OutputType = keyof typeof Outputs;
export type CombineType = keyof typeof Combines;

export type NodeType = LayerType | InputType | TransformType | OutputType | CombineType;

export type NodeGroupType = 'Input' | 'Layer' | 'Transform' | 'Output' | 'Combine';

export function isNode(value: string) {
  return Object.keys(Nodes).includes(value);
}

export function isLayerType(value: string) {
  return Object.keys(Layers).includes(value);
}

export function isInputType(value: string) {
  return Object.keys(Inputs).includes(value);
}

export function isTransformType(value: string) {
  return Object.keys(Transforms).includes(value);
}

export function isOutputTpye(value: string) {
  return Object.keys(Outputs).includes(value);
}

export function isCombineType(value: string) {
  return Object.keys(Combines).includes(value);
}

export function getNodeGroup(nodeType: NodeType): NodeGroupType | undefined {
  if (isInputType(nodeType)) {
    return 'Input';
  }
  if (isLayerType(nodeType)) {
    return 'Layer';
  }
  if (isTransformType(nodeType)) {
    return 'Transform';
  }

  if (isOutputTpye(nodeType)) {
    return 'Output';
  }

  if (isCombineType(nodeType)) {
    return 'Combine';
  }
}
