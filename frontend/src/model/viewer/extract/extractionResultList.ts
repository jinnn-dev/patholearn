import { GreyGroupSummary } from './greyGroupSummary';
import { ExtractionResult } from './extractionResult';

export interface ExtractionResultList {
  summary: GreyGroupSummary[];
  results: ExtractionResult[];
}
