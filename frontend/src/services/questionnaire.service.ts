import { handleError } from './error-handler';
import { ApiService } from './api.service';
import { Questionnaire, QuestionnaireCreate } from '../model/questionnaires/questionnaire';
import { QuestionnaireQuestionCreate } from '../model/questionnaires/questionnaireQuestion';
import { QuestionnaireAnswerCreate } from '../model/questionnaires/questionnaireAnswer';

export class QuestionnaireService {
  public static async createQuestionnaire(questionnaireCreate: QuestionnaireCreate, task_id: number) {
    const [_, response] = await handleError(
      ApiService.post<Questionnaire>({
        resource: this.apiURL(`/${task_id}`),
        data: {
          ...questionnaireCreate
        }
      })
    );
  }

  public static async getQuestionnairesToTask(task_id: number) {
    const [_, response] = await handleError(
      ApiService.get<Questionnaire[]>({
        resource: this.apiURL(`/${task_id}`)
      })
    );
    return response!.data;
  }

  public static async saveQuestionnaireAnswers(answers: QuestionnaireAnswerCreate[]) {
    const [_, response] = await handleError(
      ApiService.post<Questionnaire[]>({
        resource: this.apiURL(`/answers/multiple`),
        data: answers
      })
    );

    return response!.data;
  }

  public static async deleteQuestionnaire(questionnaireId: number) {
    const [_, response] = await handleError(
      ApiService.delete({
        resource: this.apiURL(`/${questionnaireId}`)
      })
    );
    return response!.data;
  }

  private static apiURL = (path: string = '') => '/questionnaires' + path;
}
