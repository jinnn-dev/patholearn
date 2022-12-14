export interface QuestionnaireAnswer {
  id: number;
  user_id: number;
  question_id: number;
  answer?: string;
}

export interface QuestionnaireAnswerCreate {}

export interface QuestionnaireAnswerUpdate {
  id: number;
  user_id: number;
  question_id: number;
  answer?: string;
}
