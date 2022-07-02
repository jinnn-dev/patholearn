import { TaskService } from '../../../services/task.service';
import { ValidationResult } from '../../../model/viewer/validation/validationResult';

export async function validateTaskAnnotations(taskId: number): Promise<ValidationResult[]> {
  return await TaskService.validateTaskAnnotations(taskId);
}

export async function validateUserSolutionAnnotations(taskId: number): Promise<ValidationResult[]> {
  return await TaskService.validateUserSolutionAnnotations(taskId);
}
