import { EventHandler, MouseTracker, OSDEvent, Point, Viewer } from 'openseadragon';
export const SVG_ID = 'drawingSvg';

// Adaption of: https://github.com/openseadragon/svg-overlay | License: BSD-3-Clause License
export class SvgOverlay {
  private _viewer: Viewer;
  private _containerWidth: number;
  private _containerHeight: number;
  private _svg: HTMLElement;
  private _solutionNode: HTMLElement;
  private _backgroundNode: HTMLElement;
  private _userSolutionNode: HTMLElement;
  private _infoNode: HTMLElement;

  private static svgNS = 'http://www.w3.org/2000/svg';

  constructor(viewer: Viewer) {
    const self = this;

    this._viewer = viewer;
    this._containerWidth = 0;
    this._containerHeight = 0;

    this._svg = document.createElementNS(SvgOverlay.svgNS, 'svg') as HTMLElement;
    this._svg.id = SVG_ID;
    this._svg.style.position = 'absolute';
    this._svg.style.left = '0';
    this._svg.style.top = '0';
    this._svg.style.width = '100%';
    this._svg.style.height = '100%';
    this._viewer.canvas.appendChild(this._svg);

    this._backgroundNode = document.createElementNS(SvgOverlay.svgNS, 'g') as HTMLElement;
    this._backgroundNode.id = 'background';
    this._svg.appendChild(this._backgroundNode);

    this._solutionNode = document.createElementNS(SvgOverlay.svgNS, 'g') as HTMLElement;
    this._solutionNode.id = 'solution';
    this._svg.appendChild(this._solutionNode);

    this._infoNode = document.createElementNS(SvgOverlay.svgNS, 'g') as HTMLElement;
    this._infoNode.id = 'info';
    this._svg.appendChild(this._infoNode);

    this._userSolutionNode = document.createElementNS(SvgOverlay.svgNS, 'g') as HTMLElement;
    this._userSolutionNode.id = 'userSolution';
    this._svg.appendChild(this._userSolutionNode);

    this._viewer.addHandler('animation', function () {
      self.resize();
    });

    this._viewer.addHandler('open', function () {
      self.resize();
    });

    this._viewer.addHandler('rotate', function (evt) {
      self.resize();
    });

    this._viewer.addHandler('resize', function () {
      self.resize();
    });

    this.resize();
  }

  svg() {
    return this._svg;
  }

  solutionNode(): HTMLElement {
    return this._solutionNode;
  }

  backgroundNode(): HTMLElement {
    return this._backgroundNode;
  }

  infoNode(): HTMLElement {
    return this._infoNode;
  }

  userSolutionNode(): HTMLElement {
    return this._userSolutionNode;
  }

  resize() {
    if (this._containerWidth !== this._viewer.container.clientWidth) {
      this._containerWidth = this._viewer.container.clientWidth;
      this._svg.setAttribute('width', this._containerWidth + '');
    }

    if (this._containerHeight !== this._viewer.container.clientHeight) {
      this._containerHeight = this._viewer.container.clientHeight;
      this._svg.setAttribute('height', this._containerHeight + '');
    }

    var p = this._viewer.viewport.pixelFromPoint(new Point(0, 0), true);
    var zoom = this._viewer.viewport.getZoom(true);
    var rotation = this._viewer.viewport.getRotation();
    var scale = this._viewer.viewport._containerInnerSize.x * zoom;
    this._solutionNode.setAttribute(
      'transform',
      'translate(' + p.x + ',' + p.y + ') scale(' + scale + ') rotate(' + rotation + ')'
    );
    this._backgroundNode.setAttribute(
      'transform',
      'translate(' + p.x + ',' + p.y + ') scale(' + scale + ') rotate(' + rotation + ')'
    );

    this._infoNode.setAttribute(
      'transform',
      'translate(' + p.x + ',' + p.y + ') scale(' + scale + ') rotate(' + rotation + ')'
    );

    this._userSolutionNode.setAttribute(
      'transform',
      'translate(' + p.x + ',' + p.y + ') scale(' + scale + ') rotate(' + rotation + ')'
    );
  }

  onClick(node: string | Element, handler: EventHandler<OSDEvent<any>>) {
    new MouseTracker({
      element: node,
      clickHandler: handler
    }).setTracking(true);
  }
}

declare module 'openseadragon' {
  interface Viewer {
    svgOverlay(): SvgOverlay;
  }
}

Viewer.prototype.svgOverlay = function () {
  return new SvgOverlay(this);
};
