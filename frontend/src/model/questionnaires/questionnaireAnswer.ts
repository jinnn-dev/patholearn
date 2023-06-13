export interface QuestionnaireAnswer {
  id: number;
  user_id: string;
  question_id: number;
  question_option_id: number;
  questionnaire_id: number;
  selected: string;
  answer?: string;
}

export interface QuestionnaireAnswerCreate {
  question_id: number;
  question_option_id: number;
  questionnaire_id: number;
  selected: string;
  answer?: string;
}

export interface QuestionnaireAnswerUpdate {
  id: number;
  user_id: string;
  question_id: number;
  answer?: string;
  selected: string;
}
