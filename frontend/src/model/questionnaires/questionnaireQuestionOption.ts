export interface QuestionnaireQuestionOption {
  id: number;
  question_id: number;
  order: number;
  value: string;
  with_input: boolean;
}

export interface QuestionnaireQuestionOptionCreate {
  order: number;
  value: string;
  with_input: boolean;
}

export interface QuestionnaireQuestionOptionUpdate {
  id: number;
  question_id?: number;
  order?: number;
  value?: string;
  with_input: boolean;
}
