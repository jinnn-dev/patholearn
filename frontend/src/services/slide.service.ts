import { SLIDE_API_URL } from '../config';
import { ExtractionResult } from '../model';
import { Slide } from '../model/slide';
import { ApiService } from './api.service';

export class SlideService {
  /**
   * Returns all wsi slides available
   *
   * @returns All found slides
   */
  public static async getSlides(): Promise<Slide[]> {
    const response = await ApiService.get<Slide[]>({ resource: '/slides', host: SLIDE_API_URL });
    return response.data;
  }

  /**
   * Creates a new Slide and triggers the image pyramid conversion
   *
   * @param data FormData containing the name and file to upload
   * @param onUploadProgress Callback for showing upload progess
   * @returns The created Slide
   */
  public static async uploadSlide(data: FormData, onUploadProgress: (event: any) => void): Promise<any> {
    const response = await ApiService.post({
      resource: '/slides',
      data,
      config: { onUploadProgress },
      host: SLIDE_API_URL
    });
    return response.data;
  }

  /**
   * Deletes the given Slide
   *
   * @param slideName ID of the slide
   * @returns The deleted Slide
   */
  public static async deleteSlide(slideName: string): Promise<any> {
    const response = await ApiService.delete({ resource: `/slides/${slideName}`, host: SLIDE_API_URL });
    return response.data;
  }

  /**
   * Converts an image to annotations
   *
   * @param data FormData containing the image to convert
   * @param onUploadProgress Callback for the upload progress
   * @returns The conversion result
   */
  public static async convertImage(data: FormData, onUploadProgress?: (event: any) => void): Promise<ExtractionResult> {
    const response = await ApiService.post<ExtractionResult>({
      resource: '/slides/convert',
      data,
      config: {
        ...(onUploadProgress && onUploadProgress)
      },
      host: SLIDE_API_URL
    });
    return response.data;
  }
}
