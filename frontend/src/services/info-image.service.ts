import { SLIDE_API_URL } from '../config';
import { InfoImage } from '../model/infoImage';
import { ApiService } from './api.service';
import { handleError } from './error-handler';

export class InfoImageService {
  public static async uploadMultipleInfoImages(
    formData: FormData,
    onUploadProgress: (event: any) => void
  ): Promise<InfoImage[]> {
    const [_, response] = await handleError(
      ApiService.post<InfoImage[]>({
        resource: '/infoImages',
        host: SLIDE_API_URL,
        data: formData,
        config: { onUploadProgress }
      }),
      'Info Images upload failed'
    );

    return response!.data;
  }

  public static async deleteInfoImages(images: string[]): Promise<any> {
    const [_, response] = await handleError(
      ApiService.delete<any>({
        resource: '/infoImages',
        host: SLIDE_API_URL,
        data: images
      })
    );

    return response!.data;
  }

  public static async getInfoImagesById(image_ids: string[]): Promise<InfoImage[]> {
    const params = new URLSearchParams();
    for (const id of image_ids) {
      params.append('infoimageid', id);
    }

    const [_, response] = await handleError(
      ApiService.get<InfoImage[]>({
        resource: `/infoImages?${params.toString()}`,
        host: SLIDE_API_URL
      })
    );

    return response!.data;
  }

  public static async updateInfoImages(images: InfoImage[]): Promise<InfoImage[]> {
    const [_, response] = await handleError(
      ApiService.put<InfoImage[]>({
        resource: '/infoImages',
        host: SLIDE_API_URL,
        data: images
      })
    );

    return response!.data;
  }
}
