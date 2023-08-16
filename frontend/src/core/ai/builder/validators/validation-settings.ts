import { DatasetType } from '../../../../model/ai/datasets/dataset';
import { NodeType } from '../nodes/types';

export interface ValidationItems {
  unique?: boolean;
  datasetType?: DatasetType;
}

export const NodeValidation: { [type in NodeType]?: ValidationItems } = {
  DatasetNode: {
    unique: true
  },
  OutputNode: {
    unique: true
  },
  ResNetNode: {
    unique: true,
    datasetType: 'classification'
  },
  SegmentationNode: {
    unique: true,
    datasetType: 'segmentation'
  }
};