import { Course } from '../../course';
import { BaseTask } from '../../task/baseTask';
import { Task } from '../../task/task';
import { TaskGroup } from '../../task/taskGroup';

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
export interface DatasetMetadata {
  class_map: {
    [key in string]: string;
  };
  is_grayscale: boolean;
  classes: string[];
  dimension: {
    x: number;
    y: number;
  };
  patch_size: number;
  patch_magnification: number;
  task_ids: number[];
}

export interface Dataset {
  id: string;
  name: string;
  description?: string;
  dataset_type: DatasetType;
  status: DatasetStatus;
  created_at: string;
  creator_id: string;
  metadata?: DatasetMetadata;
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

export type PatchSize = 128 | 256 | 512;
export type PatchMagnification = 0.2 | 0.5 | 1.0;

export interface CreateDataset {
  name: string;
  description?: string;
  type: DatasetType;
  file?: File;
}

export interface CreateOwnDataset {
  name: string;
  description?: string;
  type: DatasetType;
  patchSize: PatchSize;
  patchMagnification: PatchMagnification;
  tasks: {
    course: Course;
    taskGroup: TaskGroup;
    baseTask: BaseTask;
    task: Task;
  }[];
}

export type ConditionalDatasetMap<T> = {
  [key in DatasetType]: T[];
};
