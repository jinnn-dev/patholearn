export interface ClearmlDataset {
  id: string;
  name: string;
  basename: string;
  description: string;
  created: string;
  dataset_stats: {
    file_count: number;
    total_size: number;
  };
}

export type DatasetStatus = 'saving' | 'processing' | 'completed' | 'failed';
export interface Dataset {
  id: string;
  name: string;
  description?: string;
  type: DatasetType;
  status: DatasetStatus;
  created_at: string;
  creator_id: string;
  metadata?: {
    class_map: {
      [key in string]: string;
    };
    is_grayscale: boolean;
    classes: string[];
  };
  clearml_dataset?: {
    id: string;
    name: string;
    project: {
      id: string;
    };
    runtime: {
      orig_dataset_name: string;
      orig_dataset_id: string;
      version: string;
      ds_file_count: number;
      ds_link_count: number;
      ds_total_size: number;
      ds_total_size_compressed: number;
      ds_change_add: number;
      ds_change_remove: number;
      ds_cange_modify: number;
      ds_change_size: number;
      status: string;
    };
  };
}

export type DatasetType = 'classification' | 'detection' | 'segmentation';

export interface CreateDataset {
  name: string;
  description?: string;
  type: DatasetType;
  file?: File;
  is_grascale: boolean;
}
