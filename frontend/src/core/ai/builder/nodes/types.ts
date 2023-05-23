import * as Layers from './layer';
import * as Inputs from './input';
import * as Transforms from './transform';

export type LayerType = keyof typeof Layers;
export type InputType = keyof typeof Inputs;
export type TransformType = keyof typeof Transforms;

export type NodeType = LayerType | InputType | TransformType;

export function isLayerType(value: NodeType) {
  return Object.keys(Layers).includes(value);
}

export function isInputType(value: NodeType) {
  return Object.keys(Inputs).includes(value);
}

export function isTransformType(value: NodeType) {
  return Object.keys(Transforms).includes(value);
}
