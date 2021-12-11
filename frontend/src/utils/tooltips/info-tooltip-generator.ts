import tippy, { animateFill, followCursor, Instance, Props } from 'tippy.js';
import 'tippy.js/animations/shift-away.css';
import 'tippy.js/dist/backdrop.css';
import 'tippy.js/dist/tippy.css';
export class InfoTooltipGenerator {
  private static _instances: Map<string, Instance<Props>> = new Map();

  public static addTooltip(id: string, node: HTMLElement, headerText: string, detailText: string, images?: string[]) {
    const element = document.getElementById('viewerImage');

    const tooltip = tippy(`[id="${id}"]`, {
      content: this._generateContent(headerText, detailText, images),
      theme: 'mydark',
      animateFill: true,
      delay: 200,
      trigger: 'none',
      allowHTML: true,
      appendTo: element!,
      plugins: [animateFill, followCursor]
    });

    this._instances.set(id, tooltip[0]);
  }

  public static destroyAll() {
    for (const tooltip of this._instances.values()) {
      tooltip.hide();
      tooltip.destroy();
    }
    this._instances = new Map();
  }

  private static _generateContent(headerText: string, detailText: string, images?: string[]) {
    return `<h1>${headerText}</h1><p>${detailText}</p><h1>HELLOO asdkfjh sakljdhf sadkf sd fsadf </h1> <Icon name="info"/>`;
  }

  public static updateTooltip(id: string) {
    const tooltipInstance = this._instances.get(id);

    if (tooltipInstance && tooltipInstance.state.isVisible) {
      const tooltipElement = tooltipInstance?.popper;
      const elementBoundingRect = tooltipInstance?.reference.getBoundingClientRect();
      const elementX = elementBoundingRect?.x;
      const elementY = elementBoundingRect?.y;
      const tooltipWidth = tooltipElement?.clientWidth!;
      const tooltipHeight = tooltipElement?.clientHeight!;

      if (tooltipElement) {
        const newXTranslate = elementX! - tooltipWidth / 2 + 7;
        const newYTranslate = -window.innerHeight - tooltipHeight / 2 + elementY! + 24;
        const transformString = `translate(${newXTranslate}px, ${newYTranslate}px)`;

        tooltipElement.style.transform = transformString;
      }
    }
  }

  public static showTooltip(id: string): void {
    const tooltip = this._instances.get(id);
    if (tooltip) {
      tooltip.show();
    }
  }

  public static hideTooltip(id: string): void {
    const tooltip = this._instances.get(id);
    if (tooltip) {
      tooltip.hide();
    }
  }
}
