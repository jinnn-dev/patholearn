import { Questionnaire } from '../../model/questionnaires/questionnaire';
import { Task } from '../../model/task/task';

export interface LayerQuestionnaire extends Questionnaire {
  isSkipped: boolean;
}

export interface TaskWithQuestionnaires {
  questionnaireBefore?: LayerQuestionnaire;
  task: Task;
  questionnaireAfter?: LayerQuestionnaire;
}

export interface TaskWithQuestionnairesLayer extends TaskWithQuestionnaires {
  layer: number;
  index: number;
}

export interface LayeredTasks {
  [key: number]: TaskWithQuestionnairesLayer[];
}
