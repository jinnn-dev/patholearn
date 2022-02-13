import 'tippy.js/animations/shift-away.css';
import 'tippy.js/dist/backdrop.css';
import 'tippy.js/dist/tippy.css';
import { infotooltipState } from './info-tooltip-state';

export class InfoTooltipGenerator {
  public static updateTooltip(id: string, animate: boolean = false) {
    if (infotooltipState.show && id === infotooltipState.id) {
      infotooltipState.animate = animate;
      const element = document.getElementById(id);
      if (element) {
        const rect = element.getBoundingClientRect();
        infotooltipState.x = rect.x;
        infotooltipState.y = rect.y;
      }
    }
  }

  public static showTooltip(id: string, headerText: string, detailText: string, images?: string[]): void {
    infotooltipState.id = id;
    infotooltipState.headerText = headerText;
    infotooltipState.detailText = detailText;
    infotooltipState.images = images;
    infotooltipState.show = true;

    this.updateTooltip(id, false);
  }

  public static hideTooltip(id: string): void {
    infotooltipState.show = false;
  }
}
