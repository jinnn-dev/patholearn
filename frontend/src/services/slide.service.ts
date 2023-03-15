import { SLIDE_STATUS } from 'core/types/slideStatus';
import { BASE_API_URL, SLIDE_API_URL } from '../config';
import { Slide } from '../model/slide';
import { ExtractionResult } from '../model/viewer/extract/extractionResult';
import { ApiService } from './api.service';
import { handleError } from './error-handler';

export class SlideService {
  /**
   * Returns all wsi slides available
   *
   * @returns All found slides
   */
  public static async getSlides(
    data: { metadata?: boolean; status?: SLIDE_STATUS } = { metadata: true }
  ): Promise<Slide[]> {
    const [_, response] = await handleError(
      ApiService.get<Slide[]>({
        resource: '/slides',
        data: {
          metadata: data.metadata,
          ...(data.status && { status: data.status })
        },
        host: SLIDE_API_URL
      }),
      'Slides could not be loaded'
    );
    return response!.data;
  }

  public static async getSlide(slide_id: string, metadata: boolean = true): Promise<Slide> {
    const [_, response] = await handleError(
      ApiService.get<Slide>({
        resource: `/slides/${slide_id}?metadata=${metadata}`,
        host: SLIDE_API_URL
      }),
      'Slide could not be loaded'
    );
    return response!.data;
  }

  /**
   * Creates a new Slide and triggers the image pyramid conversion
   *
   * @param data FormData containing the name and file to upload
   * @param onUploadProgress Callback for showing upload progess
   * @returns The created Slide
   */
  public static async uploadSlide(data: FormData, onUploadProgress: (event: any) => void): Promise<any> {
    const [_, response] = await handleError(
      ApiService.post<any[]>({
        resource: '/slides',
        data,
        config: { onUploadProgress },
        host: SLIDE_API_URL
      }),
      'Slide could not be uploaded'
    );
    return response!.data;
  }

  /**
   * Deletes the given Slide
   *
   * @param slideName ID of the slide
   * @returns The deleted Slide
   */
  public static async deleteSlide(slideName: string): Promise<any> {
    const [_, response] = await handleError(
      ApiService.delete({
        resource: `/slides/${slideName}`,
        host: SLIDE_API_URL
      }),
      'Slide could bot be deleted'
    );
    return response!.data;
  }

  /**
   * Converts an image to annotations
   *
   * @param data FormData containing the image to convert
   * @param onUploadProgress Callback for the upload progress
   * @returns The conversion result
   */
  public static async convertImage(data: FormData, onUploadProgress?: (event: any) => void): Promise<ExtractionResult> {
    const [_, response] = await handleError(
      ApiService.post<ExtractionResult>({
        resource: '/annotations/convert',
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

  public static async getNumberOfLayers(slide_id: string): Promise<number> {
    const [_, response] = await handleError(
      ApiService.get<number>({
        resource: `/slides/${slide_id}/layers`,
        host: SLIDE_API_URL
      })
    );
    return response!.data;
  }

  public static async downloadSlide(slide_id: string, layer: number): Promise<any> {
    const [_, response] = await handleError(
      ApiService.get<any>(
        {
          resource: `/slides/${slide_id}/download/${layer}`,
          host: SLIDE_API_URL
        },
        'arraybuffer'
      )
    );

    return response!.data;
  }
}
