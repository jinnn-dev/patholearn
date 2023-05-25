import { BaseSchemes, Scope } from 'rete';
import { BaseArea, BaseAreaPlugin, RenderSignal } from 'rete-area-plugin';
import { RenderPreset } from 'rete-vue-render-plugin';
import MouseCursors from '../../../../components/ai/builder/mouse-cursor/MouseCursors.vue';
import ContextMenu from '../../../../components/ai/builder/context-menu/ContextMenu.vue';
import { pushMouseEvent } from '../sync';
import { builderState } from '../state';
import { Channel } from 'pusher-js';

type Requires<Schemes extends BaseSchemes> =
  | { type: 'mount'; data: { context: 'root' | Schemes['Node'] | Schemes['Connection'] } }
  | { type: 'unmount'; data: { element: HTMLElement } }
  | { type: 'pointermove'; data: { type: 'mouse'; event: MouseEvent; position: { x: number; y: number } } }
  | { type: 'zoomed' };
type MousePluginExtra = RenderSignal<'mount', { type: string }>;
const scaleRegex = /scale\(([^\)]+)\)/;

export class MousePlugin<Schemes extends BaseSchemes> extends Scope<never, [Requires<Schemes> | MousePluginExtra]> {
  constructor() {
    super('mouse');
  }

  setParent(scope: Scope<Requires<Schemes>, []>): void {
    super.setParent(scope);

    const area = this.parentScope<BaseAreaPlugin<Schemes, BaseArea<Schemes>>>(BaseAreaPlugin);
    const container = (area as any).area.content;
    const element = document.createElement('div');
    container.add(element);

    this.parentScope().emit({
      type: 'render',
      data: {
        type: 'mount',
        element: element
      }
    });

    this.addPipe((context) => {
      if (!context || typeof context !== 'object' || !('type' in context)) return context;

      if (context.type === 'pointermove') {
        if (builderState.isConnected && builderState.channel && builderState.me) {
          pushMouseEvent(
            builderState.channel as Channel,
            {
              id: builderState.me.id,
              x: area.area.pointer.x,
              y: area.area.pointer.y,
              scale: builderState.areaZoom
            },
            100
          );
        }
      }

      if (context.type === 'zoomed') {
        const transform = builderState.area?.area.content.holder.style.transform;

        const scaleMatch = transform?.match(scaleRegex);
        if (scaleMatch) {
          // The scale property is captured in the first group of the match
          const scaleValue = scaleMatch[1];
          builderState.areaZoom = +scaleValue;
        }
        builderState.areaZoom;
      }

      return context;
    });
  }
}

export function setupMousePlugin<Schemes extends BaseSchemes, K extends MousePluginExtra>(props?: {
  delay?: number;
}): RenderPreset<Schemes, K> {
  return {
    update(context) {
      if (context.data.type === 'mount') {
        return {
          props: {
            ...context.data
          }
        };
      }
    },
    render(context) {
      if (context.data.type === 'mount') {
        return {
          component: MouseCursors,
          props: {}
        };
      }
    }
  };
}
