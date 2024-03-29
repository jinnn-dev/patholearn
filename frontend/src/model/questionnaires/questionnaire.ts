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

export const questionnaireHasAnswer = (questionnaire?: Questionnaire) => {
  if (!questionnaire) return true;
  return questionnaire.questions?.find((question) => question.answers && question.answers.length > 0) !== undefined;
};
