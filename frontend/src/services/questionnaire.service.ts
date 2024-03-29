import { handleError } from './error-handler';
import { ApiService } from './api.service';
import { Questionnaire, QuestionnaireCreate, QuestionnaireUpdate } from '../model/questionnaires/questionnaire';
import { QuestionnaireAnswer, QuestionnaireAnswerCreate } from '../model/questionnaires/questionnaireAnswer';
import { QuestionnaireAnswerStatistic } from '../model/questionnaires/questionnaireAnswerStatistic';

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
    return response!.data;
  }

  public static async updateQuestionnaire(questionnaireUpdate: QuestionnaireUpdate) {
    const [_, response] = await handleError(
      ApiService.put<Questionnaire>({
        resource: this.apiURL(''),
        data: {
          ...questionnaireUpdate
        }
      })
    );
    return response!.data;
  }

  public static async getQuestionnairesToTask(task_id: number, isBefore?: boolean) {
    const [_, response] = await handleError(
      ApiService.get<Questionnaire[]>({
        data: {
          is_before: isBefore
        },
        resource: this.apiURL(`/${task_id}`)
      })
    );
    return response!.data;
  }

  public static async saveQuestionnaireAnswers(answers: QuestionnaireAnswerCreate[]) {
    const [_, response] = await handleError(
      ApiService.post<QuestionnaireAnswer[]>({
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

  public static async checkIfAnswersExist(questionnaireId: number) {
    const [_, response] = await handleError(
      ApiService.get<boolean>({
        resource: this.apiURL(`/${questionnaireId}/answers/exists`)
      })
    );
    return response!.data;
  }

  public static async getQuestionnaireAnswers(questionnaireId: number) {
    const [_, response] = await handleError(
      ApiService.get<QuestionnaireAnswerStatistic[]>({
        resource: this.apiURL(`/${questionnaireId}/statistic`)
      })
    );
    return response!.data;
  }

  public static async downloadAnswers(questionnaireId: number) {
    const [_, response] = await handleError(
      ApiService.get<any>(
        {
          resource: this.apiURL(`/${questionnaireId}/statistic/download`)
        },
        'arraybuffer'
      )
    );
    return response!.data;
  }

  private static apiURL = (path: string = '') => '/questionnaires' + path;
}
