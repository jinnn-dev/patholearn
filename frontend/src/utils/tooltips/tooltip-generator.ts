import { select } from 'd3-selection';
import tippy, { animateFill, followCursor, Instance, Placement, roundArrow } from 'tippy.js';
import 'tippy.js/animations/shift-away.css';
import 'tippy.js/dist/backdrop.css';
import 'tippy.js/dist/svg-arrow.css';
import 'tippy.js/dist/tippy.css';
import { RESULT_RESPONSE_DETAIL, RESULT_RESPONSE_NAME, TaskStatus } from '../../core/types/taskStatus';
import { TaskResultDetail } from '../../model/task/result/taskResultDetail';

export class TooltipGenerator {
  private static instances: Instance[] = [];

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
        arrow: roundArrow + roundArrow,
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
  public static destroyAll() {
    for (const tooltip of this.instances) {
      tooltip.hide();
      tooltip.destroy();
    }
    this.instances = [];
  }

  public static removeTooltipByElementId(elementId: string) {
    const tooltip = TooltipGenerator.getTooltipByElementId(elementId);
    if (tooltip) {
      tooltip.hide();
      tooltip.destroy();
    }
  }

  public static disableTooltip(elementId: string) {
    const tooltip = TooltipGenerator.getTooltipByElementId(elementId);
    if (tooltip) {
      tooltip.disable();
    }
  }

  public static enableTooltip(elementId: string) {
    const tooltip = TooltipGenerator.getTooltipByElementId(elementId);
    if (tooltip) {
      tooltip.enable();
    }
  }

  public static addGeneralTooltip({
    target,
    content,
    placement,
    delay
  }: {
    target: string;
    content: string;
    placement: Placement;
    delay?: number | [number, number];
  }) {
    const instances = tippy(target, {
      content,
      placement,
      theme: 'myDark',
      delay: delay || 0,
      arrow: roundArrow + roundArrow
    });

    if (instances.length == 1) {
      const instance = instances[0];
      this.instances.push(instance);
      return instance;
    }
  }

  public static updateTooltipContent(elementId: string, newContent: string) {
    const tooltip = TooltipGenerator.getTooltipByElementId(elementId);
    tooltip?.setContent(newContent);
  }

  private static getTooltipByElementId(elementId: string): Instance | undefined {
    const index = this.instances.findIndex((item) => item.reference.id === elementId);
    if (index < 0) {
      return undefined;
    }
    return this.instances[index];
  }

  private static _generateContent(percentage: number, header: string, content?: string): string {
    return `<h1 class='text-lg text-center font-semibold'>${header}</h1>
    <div class='text-center'>
    <p class='text-sm my-2'>${percentage}% Übereinstimmung</p>
    ${content ? `<p class='font-semibold break-words'>${content}</p>` : ''}
    </div>`;
  }
}
