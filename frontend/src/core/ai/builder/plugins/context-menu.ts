import { BaseSchemes, NodeEditor } from 'rete';
import { RenderPreset } from 'rete-vue-render-plugin';
import { ContextMenuRender } from 'rete-vue-render-plugin/_types/presets/context-menu/types';
import ContextMenu from '../../../../components/ai/builder/context-menu/ContextMenu.vue';
import { BSchemes, ItemDefinition } from 'rete-context-menu-plugin/_types/presets/classic/types';
import { Item, Items } from 'rete-context-menu-plugin/_types/types';
import { BaseAreaPlugin } from 'rete-area-plugin';

export function setupContext<Schemes extends BaseSchemes, K extends ContextMenuRender>(props?: {
  delay?: number;
}): RenderPreset<Schemes, K> {
  const delay = typeof props?.delay === 'undefined' ? 1000 : props.delay;

  return {
    update(context) {
      if (context.data.type === 'contextmenu') {
        return {
          items: context.data.items,
          delay,
          searchBar: context.data.searchBar,
          onHide: context.data.onHide
        };
      }
    },
    render(context) {
      if (context.data.type === 'contextmenu') {
        return {
          component: ContextMenu,
          props: {
            items: context.data.items,
            delay,
            searchBar: context.data.searchBar,
            onHide: context.data.onHide
          }
        };
      }
    }
  };
}

export function createItem<S extends BSchemes>(
  [label, factory]: ItemDefinition<S>,
  key: string | number,
  context: { editor: NodeEditor<S>; area: BaseAreaPlugin<S, any> }
): Item {
  const item = {
    label,
    key: String(key)
  };

  if (typeof factory === 'function') {
    return <Item>{
      ...item,
      async handler() {
        const node = await factory();

        await context.editor.addNode(node);

        context.area.translate(node.id, context.area.area.pointer);
      }
    };
  }
  return <Item>{
    ...item,
    subitems: factory.map((data, i) => createItem(data, i, context))
  };
}

export function setupContextItems<Schemes extends BSchemes>(nodes: ItemDefinition<Schemes>[]) {
  return <Items<Schemes>>function (context, plugin) {
    const area = plugin.parentScope<BaseAreaPlugin<Schemes, any>>(BaseAreaPlugin);
    const editor = area.parentScope<NodeEditor<Schemes>>(NodeEditor);

    if (context === 'root') {
      return {
        searchBar: true,
        list: nodes.map((item, i) => createItem(item, i, { editor, area }))
      };
    }

    const deleteItem: Item = {
      label: 'Delete',
      key: 'delete',
      async handler() {
        const nodeId = context.id;
        const connections = editor.getConnections().filter((c) => {
          return c.source === nodeId || c.target === nodeId;
        });

        for (const connection of connections) {
          await editor.removeConnection(connection.id);
        }
        await editor.removeNode(nodeId);
      }
    };

    const clone = context.clone;
    const cloneItem: undefined | Item = clone && {
      label: 'Clone',
      key: 'clone',
      async handler() {
        const node = clone();

        await editor.addNode(node);

        area.translate(node.id, area.area.pointer);
      }
    };

    return {
      // searchBar: false,
      // list: [deleteItem, ...(cloneItem ? [cloneItem] : [])]
    };
  };
}
