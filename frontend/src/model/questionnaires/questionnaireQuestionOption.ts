export interface QuestionnaireQuestionOption {
  id: number;
  question_id: number;
  order: number;
  value: string;
}

export interface QuestionnaireQuestionOptionCreate extends QuestionnaireQuestionOption {}

export interface QuestionnaireQuestionOptionUpdate {
  id: number;
  question_id?: number;
  order?: number;
  value?: string;
}
