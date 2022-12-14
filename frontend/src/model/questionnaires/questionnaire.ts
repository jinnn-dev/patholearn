import { Task } from '../task/task';
import { QuestionnaireQuestion } from './questionnaireQuestion';

export interface Questionnaire {
  id: number;
  name: string;
  description: string;
  is_mandatory: boolean;
  questions?: QuestionnaireQuestion[];
  tasks?: Task[];
}

export interface QuestionnaireCreate extends Questionnaire {}

export interface QuestionnaireUpdate {
  id: number;
  name?: string;
  description?: string;
  is_mandatory?: boolean;
}
