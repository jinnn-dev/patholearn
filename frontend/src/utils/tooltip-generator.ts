import { select } from 'd3-selection';
import tippy, { animateFill, followCursor, Instance, Placement, Props } from 'tippy.js';
import 'tippy.js/animations/shift-away.css';
import 'tippy.js/dist/backdrop.css';
import 'tippy.js/dist/tippy.css';
import { RESULT_RESPONSE_DETAIL, RESULT_RESPONSE_NAME, TaskResultDetail, TaskStatus } from '../model/result';
export class TooltipGenerator {
  private static instances: Instance<Props>[] = [];

  /**
   * Creates a new tooltip with the given task result detail
   *
   * @param resultDetail The content of the tooltip
   */
  public static addTooltip(resultDetail: TaskResultDetail): void {
    const percentage =
      resultDetail.percentage! % 1 === 0
        ? resultDetail.percentage! * 100
        : Number((resultDetail.percentage! * 100).toFixed(2));

    let detailContent = RESULT_RESPONSE_DETAIL[resultDetail.status!];
    if (resultDetail.status === TaskStatus.WRONG_NAME) {
      const name = select('[id="' + resultDetail.id + '"]').attr('name');

      if (!name) {
        detailContent = 'Du hast vergessen der Annotation eine Klasse zu geben';
      } else {
        detailContent = name + ' ' + detailContent;
      }
    }

    this.instances.push(
      ...tippy('[id="' + resultDetail.id + '"]', {
        content: this._generateContent(percentage, RESULT_RESPONSE_NAME[resultDetail.status!]!, detailContent),
        theme: 'myDark',
        animateFill: true,
        delay: 200,
        followCursor: 'initial',
        allowHTML: true,
        plugins: [animateFill, followCursor]
      })
    );
  }

  /**
   * Creates a tooltip for every task result
   *
   * @param resultDetails List of result details
   */
  public static addAll(resultDetails: TaskResultDetail[]) {
    if (resultDetails) {
      for (const resultDetail of resultDetails) {
        this.addTooltip(resultDetail);
      }
    }
  }

  /**
   * Hides all tooltips
   */
  public static hideAll() {
    for (const tooltip of this.instances) {
      tooltip.hide();
    }
  }

  /**
   * Destroys all tooltips
   */
  public static destoyAll() {
    for (const tooltip of this.instances) {
      tooltip.hide();
      tooltip.destroy();
    }
    this.instances = [];
  }

  private static _generateContent(percentage: number, header: string, content?: string): string {
    return `<h1 class="text-lg text-center font-semibold">${header}</h1>
    <div class="text-center">
    <p class="text-sm my-2">${percentage}% Übereinstimmung</p>
    ${content ? `<p class="font-semibold break-words">${content}</p>` : ''}
    </div>`;
  }

  public static addGeneralTooltip({
    target,
    content,
    placement
  }: {
    target: string;
    content: string;
    placement: Placement;
  }) {
    tippy(target, { content, placement, theme: 'myDark' });
  }
}
