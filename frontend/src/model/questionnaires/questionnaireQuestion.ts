import { QuestionnaireQuestionOption } from './questionnaireQuestionOption';
import { QuestionnaireAnswer } from './questionnaireAnswer';

export enum QuestionnaireQuestionType {
  SINGLE_CHOICE = 0,
  FREE_TEXT = 1
}

export const QuestionnaireQuestionTypeNames: { [key in QuestionnaireQuestionType]: string } = {
  [QuestionnaireQuestionType.SINGLE_CHOICE]: 'Single choice',
  [QuestionnaireQuestionType.FREE_TEXT]: 'Freitext'
};

export interface QuestionnaireQuestion {
  id: number;
  questionnaire_id: string;
  order: number;
  question_text: string;
  is_mandatory: boolean;
  question_type: QuestionnaireQuestionType;
  answers?: QuestionnaireAnswer[];
  options?: QuestionnaireQuestionOption[];
}

export interface QuestionnaireQuestionCreate extends QuestionnaireQuestion {}

export interface QuestionnaireQuestionUpdate {
  id: number;
  questionnaire_id: string;
  order: number;
  question_text: string;
  is_mandatory: boolean;
  question_type: QuestionnaireQuestionType;
  answers?: QuestionnaireAnswer[];
  options?: QuestionnaireQuestionOption[];
}
