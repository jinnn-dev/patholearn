import { ValidationResultType } from './validationResultType';

export interface ValidationResult {
  id: string;
  result: ValidationResultType[];
}
