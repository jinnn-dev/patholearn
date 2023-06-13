import { AreaExtensions, BaseArea, BaseAreaPlugin } from 'rete-area-plugin';
import { Schemes } from './use-editor';
import { NodeEditor } from 'rete';
import { lockElement, pushNodeLockedEvent, pushNodeUnlockedEvent, unlockElement } from './sync';
import { builderState, isTraining } from './state';
import { PresenceChannel } from 'pusher-js';

export function trackedSelector<
  E extends { label: string; id: string; unselect(): void; translate(dx: number, dy: number): void }
>() {
  const selector = AreaExtensions.selector();
  return {
    ...selector,
    add(entity: E, accumulate: boolean) {
      if (!accumulate) {
        // entity.unselect();
      } // they have selected = true until selector.add is called
      selector.add(entity, accumulate);
    },
    unselectAll() {
      selector.unselectAll();
    },
    remove(entity: Pick<E, 'label' | 'id'>) {
      console.log('Unselect', entity);
    }
  };
}

export function selector<
  E extends { label: string; id: string; unselect(): void; translate(dx: number, dy: number): void }
>() {
  const entities = new Map<string, E>();
  let pickId: string | null = null;

  function unselectAll() {
    entities.forEach((item) => item.unselect());
    entities.clear();
  }
  return {
    isSelected(entity: Pick<E, 'label' | 'id'>) {
      return entities.has(`${entity.label}_${entity.id}`);
    },
    add(entity: E, accumulate: boolean) {
      if (!accumulate) unselectAll();
      entities.set(`${entity.label}_${entity.id}`, entity);
    },
    remove(entity: Pick<E, 'label' | 'id'>) {
      const id = `${entity.label}_${entity.id}`;
      const item = entities.get(id);

      if (item) {
        entities.delete(id);
        item.unselect();
      }
    },
    unselectAll,
    translate(dx: number, dy: number) {
      entities.forEach((item) => !this.isPicked(item) && item.translate(dx, dy));
    },
    pick(entity: Pick<E, 'label' | 'id'>) {
      pickId = `${entity.label}_${entity.id}`;
    },
    release() {
      pickId = null;
    },
    isPicked(entity: Pick<E, 'label' | 'id'>) {
      return pickId === `${entity.label}_${entity.id}`;
    }
  };
}

export type Accumulating = {
  active(): boolean;
};

export type Selectable = ReturnType<typeof selector>;

export function selectableNodes<T>(
  base: BaseAreaPlugin<Schemes, T>,
  core: Selectable,
  options: { accumulating: Accumulating }
) {
  let editor: null | NodeEditor<Schemes> = null;
  const area = base as BaseAreaPlugin<Schemes, BaseArea<Schemes>>;
  const getEditor = () => editor || (editor = area.parentScope<NodeEditor<Schemes>>(NodeEditor));

  let unselect = false;

  function selectNode(node: Schemes['Node']) {
    if (node.selected || node.lockStatus || isTraining.value) {
      return;
    }
    pushNodeLockedEvent(builderState.channel as PresenceChannel, node.id);
    lockElement(builderState.task!.id, node.id, builderState.me!.id);
    const lockStatus = {
      lockedBy: builderState.me!
    };
    node.lockStatus = lockStatus;
    for (const control of Object.values(node.controls)) {
      control.lockStatus = lockStatus;
    }

    node.selected = true;
    area.update('node', node.id);
  }

  function unselectNode(node: Schemes['Node']) {
    if (!node.selected) {
      return;
    }
    const editorNode = editor?.getNode(node.id);
    if (!editorNode) {
      return;
    }

    pushNodeUnlockedEvent(builderState.channel as PresenceChannel, node.id);
    unlockElement(builderState.task!.id, node.id, builderState.me!.id);
    node.lockStatus = undefined;
    node.selected = false;
    area.update('node', node.id);
  }

  // eslint-disable-next-line max-statements, complexity
  area.addPipe((context) => {
    if (!context || typeof context !== 'object' || !('type' in context)) return context;

    if (context.type === 'nodepicked') {
      const pickedId = context.data.id;

      const accumulate = options.accumulating.active();
      const node = getEditor().getNode(pickedId);

      if (!node || node.selected) return;

      core.pick({ id: pickedId, label: 'node' });

      core.add(
        {
          label: 'node',
          id: node.id,
          translate(dx, dy) {
            const view = area.nodeViews.get(node.id);
            const current = view?.position;

            if (current) {
              view.translate(current.x + dx, current.y + dy);
            }
          },
          unselect() {
            unselectNode(node);
          }
        },
        accumulate
      );
      selectNode(node);
    } else if (context.type === 'nodetranslated') {
      const { id, position, previous } = context.data;
      const dx = position.x - previous.x;
      const dy = position.y - previous.y;

      if (core.isPicked({ id, label: 'node' })) core.translate(dx, dy);
    } else if (context.type === 'pointerdown') {
      unselect = true;
    } else if (context.type === 'pointermove') {
      unselect = false;
    } else if (context.type === 'pointerup') {
      if (unselect) {
        core.unselectAll();
      }
      unselect = false;
    }
    return context;
  });
}
