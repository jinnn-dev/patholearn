import { ExtractionResult } from '../model/viewer/export/extractionResult';
import { handleError } from './error-handler';
import { ApiService } from './api.service';
import { BASE_API_URL } from '../config';

export class ImageService {
  public static async convertImageToAnnotations(
    data: FormData,
    onUploadProgress?: (event: any) => void
  ): Promise<ExtractionResult[]> {
    const [_, response] = await handleError(
      ApiService.post<ExtractionResult[]>({
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
