import OpenSeadragon, { Point, Viewer } from 'openseadragon';
import { viewportToImage, webToViewport } from '../../src/utils/seadragon.utils';

const div = document.createElement('div');
div.id = 'viewer';
document.body.append(div);

describe('Openseadragon utils should correctly work', () => {
  let viewer: Viewer;

  beforeEach(async () => {
    viewer = OpenSeadragon({
      id: 'viewer',
      tileSources: {
        url: '../_helper/test.jpg',
        type: 'image'
      }
    });
    await new Promise((r) => setTimeout(r, 2000));
    console.log(viewer.world);
    // while (!loaded) {}
  });

  it('Openseadragon instance is not null', () => {
    expect(viewer).not.toBeNull();
  });

  it('webToViewport should correctly return viewport point', () => {
    const expectedPoint = new Point(50, 50);
    expect(webToViewport(50, 50, viewer)).toEqual(expectedPoint);
  });

  it('viewportToImage should correctly return image point', () => {
    const expectedPoint = new Point(50, 50);
    expect(viewportToImage(new Point(50, 50), viewer)).toEqual(expectedPoint);
  });

  it('imageToViewport should correctly return image point', () => {
    const expectedPoint = new Point(50, 50);
    console.log(viewer.world.getItemCount());

    // const myViewer = expect(imageToViewport(new Point(50, 50), viewer)).toEqual(expectedPoint);
  });
});
