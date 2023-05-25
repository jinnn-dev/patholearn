import { BaseSchemes, Root, Scope, ClassicPreset, NodeEditor } from 'rete';
import { Area2D, AreaPlugin } from 'rete-area-plugin';
import { Connection, ConnectionPlugin } from 'rete-connection-plugin';
import { builderState } from '../state';
import { NodeTranslatedEvent, pushNodeTranslatedEvent } from '../sync';
import { Channel } from 'pusher-js';
import { AreaExtra, Schemes } from '../use-editor';
export class SyncPlugin {
  root = new Scope<never, [Root<Schemes>]>('sync');
  area = new Scope<never, [Area2D<Schemes>, Root<Schemes>]>('sync');
  connection = new Scope<never, [Connection, Root<Schemes>]>('sync');

  eventsRegistered = false;

  externalDrag = false;

  constructor() {
    this.root.addPipe((context) => {
      if (
        builderState.builderLoaded &&
        builderState.initialGraphLoaded &&
        (context.type === 'nodecreated' ||
          context.type === 'noderemoved' ||
          context.type === 'connectioncreated' ||
          context.type === 'connectionremoved')
      ) {
        builderState.shouldSaveEditor = true;
      }

      return context;
    });
    this.area.addPipe((context) => {
      if (builderState.builderLoaded && builderState.initialGraphLoaded) {
        if (context.type === 'nodetranslated') {
          if (builderState.channel && !this.externalDrag) {
            pushNodeTranslatedEvent(50, builderState.channel as Channel, {
              userId: builderState.me!.id,
              nodeId: context.data.id,
              position: context.data.position,
              previous: context.data.previous
            });
          }
          this.externalDrag = false;
        }

        if (context.type === 'nodedragged') {
          builderState.shouldSaveEditor = true;
        }
      }
      return context;
    });
    this.connection.addPipe((context) => {
      return context;
    });
  }

  registerEvents() {
    if (this.eventsRegistered || !builderState.channel) {
      return;
    }

    builderState.channel.bind('client-node-dragged', (data: NodeTranslatedEvent) => {
      const area = this.area.parent as AreaPlugin<Schemes, AreaExtra>;
      const connection = this.connection.parent as ConnectionPlugin<Schemes>;

      const editor = this.root.parent as NodeEditor<Schemes>;
      const node = area.nodeViews.get(data.nodeId);
      if (node) {
        this.externalDrag = true;
        node.translate(data.position.x, data.position.y);
      }
    });
  }
}
