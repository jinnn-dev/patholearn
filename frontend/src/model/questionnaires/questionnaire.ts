import { Task } from '../task/task';
import { QuestionnaireQuestion } from './questionnaireQuestion';

export interface Questionnaire {
  id: number;
  name: string;
  description: string;
  is_mandatory: boolean;
  questions?: QuestionnaireQuestion[];
  tasks?: Task[];
  is_before: boolean;
}

export interface QuestionnaireCreate {
  name?: string;
  description?: string;
  is_mandatory: boolean;
  questions?: QuestionnaireQuestion[];
  tasks?: Task[];
  is_before: boolean;
}

export interface QuestionnaireUpdate {
  id: number;
  name?: string;
  description?: string;
  is_mandatory?: boolean;
  is_before: boolean;
  questions?: QuestionnaireQuestion[];
}
