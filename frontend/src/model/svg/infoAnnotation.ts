export interface InfoAnnotation {
  headerText: string;
  detailText: string;
  images: string[];

  generateTooltip(): void;
  deleteTooltip(): void;
}
