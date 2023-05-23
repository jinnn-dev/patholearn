import * as Nodes from './index';
import * as Layers from './layer';
import * as Inputs from './input';
import * as Transforms from './transform';

export type LayerType = keyof typeof Layers;
export type InputType = keyof typeof Inputs;
export type TransformType = keyof typeof Transforms;

export type NodeType = LayerType | InputType | TransformType;

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
