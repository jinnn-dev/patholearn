export interface Dataset {
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
