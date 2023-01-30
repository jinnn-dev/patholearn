import { User } from '../user';
import { QuestionnaireAnswer } from './questionnaireAnswer';
import { QuestionnaireQuestionOption } from './questionnaireQuestionOption';

export interface QuestionnaireAnswerStatistic {
  id: number;
  answer: string;
  selected: string;
  question_option: QuestionnaireQuestionOption;
  user: User;
  questionnaire_id: number;
}
