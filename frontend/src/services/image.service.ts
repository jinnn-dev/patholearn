import { ExtractionResultList } from '../model/viewer/export/extractionResult';
import { handleError } from './error-handler';
import { ApiService } from './api.service';
import { BASE_API_URL } from '../config';

export class ImageService {
  public static async convertImagesToAnnotations(
    data: FormData,
    onUploadProgress?: (event: any) => void
  ): Promise<ExtractionResultList> {
    const [_, response] = await handleError(
      ApiService.post<ExtractionResultList>({
        resource: '/annotations/convertMultiple',
        data,
        config: {
          ...(onUploadProgress && onUploadProgress)
        },
        host: BASE_API_URL
      }),
      'Image could not be converted'
    );
    return response!.data;
  }
}
