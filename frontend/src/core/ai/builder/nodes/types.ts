import * as Nodes from './index';
import * as Layers from './layer';
import * as Inputs from './input';
import * as Transforms from './transform';
import * as Outputs from './output';
import * as Combines from './combine';

type LayerClasses = {
  [K in keyof typeof Layers]: InstanceType<typeof Layers[K]>;
};

type InputClasses = {
  [K in keyof typeof Inputs]: InstanceType<typeof Inputs[K]>;
};

type TransformClasses = {
  [K in keyof typeof Transforms]: InstanceType<typeof Transforms[K]>;
};

type OutputClasses = {
  [K in keyof typeof Outputs]: InstanceType<typeof Outputs[K]>;
};

type CombineClasses = {
  [K in keyof typeof Combines]: InstanceType<typeof Combines[K]>;
};

export type NodeClassesType =
  | LayerClasses[keyof LayerClasses]
  | InputClasses[keyof InputClasses]
  | TransformClasses[keyof TransformClasses]
  | OutputClasses[keyof OutputClasses]
  | CombineClasses[keyof CombineClasses];

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
