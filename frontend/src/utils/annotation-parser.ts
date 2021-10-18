import { Simplify } from 'curvereduce';
import { nanoid } from 'nanoid';
import OpenSeadragon, { Point } from 'openseadragon';
import { ANNOTATION_TYPE } from '../model/viewer/annotationType';
import { ANNOTATION_COLOR } from '../model/viewer/colors';
import { AnnotationData } from '../model/viewer/export/annotationData';
import { ExtractionResult } from '../model/viewer/export/extractionResult';
import { PointData } from '../model/viewer/export/pointData';
import { imageToViewport } from './seadragon.utils';
export interface ParseResult {
  name: string | null;
  color: string | null;
  polygons: AnnotationData[];
}

export class AnnotationParser {
  /**
   * Converts an XML-File to annotations with its annotation groups
   *
   * @param file XML file to convert
   * @param viewer OpenSeadragon viewer for coordinate conversion
   * @param callback Call to call, when file conversion is completet
   */
  public static convertXmlToPolygons(
    file: File,
    viewer: OpenSeadragon.Viewer,
    callback: (data: ParseResult[]) => void
  ): void {
    const reader = new FileReader();

    reader.onload = function () {
      const loadedXML = reader.result;
      const parser = new DOMParser();
      const doc = parser.parseFromString(loadedXML as string, 'application/xml');

      const parseResults: ParseResult[] = [];

      const annotations = doc.getElementsByTagName('Annotation');

      Array.from(annotations).forEach((annotation) => {
        const name = annotation.getAttribute('Name');
        const color = annotation.getAttribute('LineColor');

        let slicedColor = ANNOTATION_COLOR.SOLUTION_COLOR.toString();
        if (color && color !== '0') {
          slicedColor = color!.slice(0, 6);

          if (slicedColor.length < 6) {
            slicedColor += 'F';
          }
          slicedColor = '#' + slicedColor;
        }

        const parentRegions = annotation.getElementsByTagName('Regions');
        const parentItem: ParseResult = {
          name,
          color: slicedColor,
          polygons: []
        };

        Array.from(parentRegions).forEach((parentRegion) => {
          Array.from(parentRegion.getElementsByTagName('Region')).forEach((region) => {
            const item: AnnotationData = {
              color: slicedColor,
              name: name!,
              id: nanoid(),
              type: ANNOTATION_TYPE.SOLUTION,
              coord: {
                image: []
              }
            };
            const vertices = region.getElementsByTagName('Vertex');

            const imagePoints: PointData[] = [];
            const viewportPoints: PointData[] = [];
            Array.from(vertices).forEach((vertice) => {
              const x = +vertice.getAttribute('X')!;
              const y = +vertice.getAttribute('Y')!;
              imagePoints.push({ x: x, y: y });
            });
            const simplifiedImage = Simplify(imagePoints, 3);

            simplifiedImage.forEach((item) => {
              const point = imageToViewport(new Point(item.x, item.y), viewer);
              viewportPoints.push(point);
            });

            item.coord.image = simplifiedImage;
            parentItem.polygons.push(item);
          });
        });
        parseResults.push(parentItem);
      });
      callback(parseResults);
    };

    reader.readAsText(file);
  }

  /**
   * Converts the extraction result of an image to annotations and annotation groups
   *
   * @param data The extraction result from the image
   * @param viewer OpenseaDragon Viewer for coordniate conversion
   * @param type Type of te annotation
   * @returns the parse result which can be added to the viewer
   */
  public static convertImageToAnnotations(
    data: ExtractionResult,
    viewer: OpenSeadragon.Viewer,
    type: ANNOTATION_TYPE = ANNOTATION_TYPE.SOLUTION
  ): ParseResult[] {
    const parseResult: ParseResult[] = [];

    const width = viewer.world.getItemAt(0).getContentSize().x;
    const factor = width / data.image.width;
    for (const item of data.annotations) {
      const color = '#' + item.gray_value.toString().repeat(6);
      const parseItem: ParseResult = {
        color: color,
        name: item.gray_value + '',
        polygons: []
      };

      for (const annotation of item.annotations) {
        const polygonItem: AnnotationData = {
          color: color,
          id: nanoid(),
          type: type,
          name: item.gray_value + '',
          coord: {
            image: [],
            viewport: []
          }
        };

        for (const coord of annotation) {
          const imagePoint = new Point(coord.x * factor, coord.y * factor);
          const viewportPoint = imageToViewport(imagePoint, viewer);
          polygonItem.coord.image.push(imagePoint);
          polygonItem.coord.viewport!.push(viewportPoint);
        }
        parseItem.polygons.push(polygonItem);
      }

      parseResult.push(parseItem);
    }

    return parseResult;
  }
}
