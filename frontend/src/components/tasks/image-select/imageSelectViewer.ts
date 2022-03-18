import { select, Selection } from 'd3-selection';
import OpenSeadragon, { MouseTracker, TileCache, Viewer } from 'openseadragon';
import { ref, Ref } from 'vue';
import { SLIDE_IMAGE_URL } from '../../../config';
import { ImageSelectFeedback, RESULT_POLYGON_COLOR } from '../../../model/result';
import { ANNOTATION_COLOR } from '../../../model/viewer/colors';
import { shuffle } from '../../../utils/seadragon.utils';
import { options, SVG_ID } from '../../viewer/core/options';
import { BACKGROUND_NODE_ID, SvgOverlay } from '../../viewer/core/svg-overlay';
import { viewerLoadingState } from '../../viewer/core/viewerState';

export class ImageSelectViewer {
  private _viewer: Viewer;

  private _overlay: SvgOverlay;

  private _selectedImages: Ref<Set<string>>;

  private _tilesSources: string[];

  private _selectColor: string;

  private _rects: Selection<SVGRectElement, unknown, HTMLElement, any>[];

  private _imageSelectFeedback: ImageSelectFeedback[];

  private _clickDisabled: Boolean = false;

  constructor(
    images: string[],
    selected: string[],
    selectColor = ANNOTATION_COLOR.SOLUTION_COLOR,
    shuffleImages: boolean = true
  ) {
    this._selectedImages = ref(new Set(selected));
    this._tilesSources = [];
    this._selectColor = selectColor;
    this._rects = [];
    this._imageSelectFeedback = [];

    const viewerOptions = options(
      'viewerImage',
      'https://images.unsplash.com/photo-1634546703473-d8809bba39b2?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1587&q=80'
    );

    viewerOptions.zoomPerScroll = 1.2;
    viewerOptions.collectionMode = true;
    viewerOptions.collectionTileMargin = 100;

    if (shuffleImages) {
      this._tilesSources = shuffle(images);
    } else {
      this._tilesSources = images;
    }

    // for (const image of images) {
    //   this._tilesSources.push(SLIDE_IMAGE_URL + '/' + image);
    // }

    viewerOptions.tileSources = this._tilesSources.map((image) => {
      return {
        type: 'image',
        url:
          SLIDE_IMAGE_URL +
          (image.includes('task-image') ? '/' : '/task-images/') +
          image +
          (image.includes('task-image') ? '' : '.jpeg')
      };
    });

    this._viewer = OpenSeadragon(viewerOptions);
    new TileCache({
      maxImageCacheCount: 500
    });

    new SvgOverlay(this._viewer);
    select('#' + SVG_ID).remove();

    this._overlay = this._viewer.svgOverlay();

    this.initViewer();
  }

  initViewer() {
    this._viewer.addHandler('open', () => {
      for (let i = 0; i < this._tilesSources.length; i++) {
        const tiledImage = this._viewer.world.getItemAt(i);
        const box = tiledImage.getBounds(true);

        const imageId = this._tilesSources[i].includes('task-image')
          ? this._tilesSources[i].split('/')[1].split('.')[0]
          : this._tilesSources[i];

        this._rects[i] = select(`#${BACKGROUND_NODE_ID}`)
          .append('rect')
          .attr('x', box.x)
          .attr('y', box.y)
          .attr('width', box.width)
          .attr('height', box.height)
          .attr('fill', 'transparent')
          .attr('stroke-width', 10)
          .attr('stroke', this._selectedImages.value.has(imageId) ? this._selectColor : 'none')
          .attr('id', imageId);
      }

      viewerLoadingState.tilesLoaded = true;
      viewerLoadingState.annotationsLoaded = true;

      this._setRectColors();
    });

    const self = this;

    new MouseTracker({
      element: this._viewer.canvas,
      clickHandler: (event: any) => {
        if (event.quick) {
          select(`#${BACKGROUND_NODE_ID}`)
            .selectAll('rect')
            .on('click', function () {
              if (!self._clickDisabled) {
                const rect = select(this);
                const index = rect.attr('id');

                if (self._selectedImages.value.has(index)) {
                  self._selectedImages.value.delete(index);
                  rect.attr('stroke', 'none');
                } else {
                  self._selectedImages.value.add(index);
                  rect.attr('stroke', self._selectColor);
                }
              }
            });
        } else {
          select(`#${BACKGROUND_NODE_ID}`).selectAll('rect').on('click', null);
        }
      }
    });
  }

  setResultColors(imageSelectFeedback: ImageSelectFeedback[]) {
    this._imageSelectFeedback = imageSelectFeedback;
    this._setRectColors();
  }

  resetResultColors() {
    if (this._selectedImages) {
      for (const rect of this._rects) {
        if (rect.attr('stroke') !== 'none') {
          rect.attr('stroke', this._selectColor);
        }
      }
    }
  }

  destroy() {
    this._viewer.destroy();
  }

  private _setRectColors() {
    for (const feedback of this._imageSelectFeedback) {
      const rect = this._rects.find((rect) => rect.attr('id') === feedback.image);
      if (rect) {
        rect.attr('stroke', RESULT_POLYGON_COLOR[feedback.status]!);
      }
    }
  }

  get selectedImagesRef(): Ref<Set<string>> {
    return this._selectedImages;
  }

  set clickDisabled(disabled: Boolean) {
    this._clickDisabled = disabled;
  }
}
