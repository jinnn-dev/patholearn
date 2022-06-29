import { TaskService } from '../../../services/task.service';
import { ValidationResult } from '../../../model/viewer/validation/validationResult';

export async function validateTaskAnnotations(task_id: number): Promise<ValidationResult[]> {
  return await TaskService.validateTaskAnnotations(task_id);
}
