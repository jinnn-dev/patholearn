import { BaseSchemes, Root, Scope, ClassicPreset, NodeEditor } from 'rete';
import { Area2D, AreaPlugin } from 'rete-area-plugin';
import { Connection, ConnectionPlugin } from 'rete-connection-plugin';
import { builderState } from '../state';
import {
  NodeTranslatedEvent,
  pushConnectionCreatedEvent,
  pushConnectionRemovedEvent,
  pushNodeCreatedEvent,
  pushNodeRemovedEvent,
  pushNodeTranslatedEvent
} from '../sync';
import { Channel } from 'pusher-js';
import { AreaExtra, ConnProps, Schemes } from '../use-editor';
import { INode } from '../serializable';
import { parseNode } from '../factories/node-factory';
export class SyncPlugin {
  root = new Scope<never, [Root<Schemes>]>('sync');
  area = new Scope<never, [Area2D<Schemes>, Root<Schemes>]>('sync');
  connection = new Scope<never, [Connection, Root<Schemes>]>('sync');

  eventsRegistered = false;

  externalDrag = false;
  externalAdd = false;
  externalRemove = false;
  externalConnectionCreated = false;
  externalConnectionRemoved = false;

  areaPlugin: AreaPlugin<Schemes, AreaExtra>;

  constructor() {
    this.areaPlugin = this.area.parent;
    this.root.addPipe((context) => {
      if (!this.areaPlugin) {
        this.areaPlugin = this.area.parent;
      }
      if (
        builderState.builderLoaded &&
        builderState.initialGraphLoaded &&
        (context.type === 'nodecreated' ||
          context.type === 'noderemoved' ||
          context.type === 'connectioncreated' ||
          context.type === 'connectionremoved')
      ) {
        if (context.type === 'nodecreated' && !this.externalAdd) {
          if (!this.externalAdd) {
            pushNodeCreatedEvent(builderState.channel as Channel, context.data.serialize());
            builderState.shouldSaveEditor = true;
          }
          this.externalAdd = false;
        }

        if (context.type === 'noderemoved') {
          if (!this.externalRemove) {
            pushNodeRemovedEvent(builderState.channel as Channel, context.data.id);
            builderState.shouldSaveEditor = true;
          }
          this.externalRemove = false;
        }

        if (context.type === 'connectioncreated') {
          if (!this.externalConnectionCreated) {
            pushConnectionCreatedEvent(builderState.channel as Channel, context.data);
            builderState.shouldSaveEditor = true;
          }
        }

        if (context.type === 'connectionremoved') {
          if (!this.externalConnectionRemoved) {
            pushConnectionRemovedEvent(builderState.channel as Channel, context.data.id);
            builderState.shouldSaveEditor = true;
          }
        }
      }

      return context;
    });
    this.area.addPipe((context) => {
      if (builderState.builderLoaded && builderState.initialGraphLoaded) {
        if (context.type === 'nodetranslated') {
          if (builderState.channel && !this.externalDrag && !this.externalAdd) {
            pushNodeTranslatedEvent(builderState.channel as Channel, {
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
    const editor = this.root.parent as NodeEditor<Schemes>;

    builderState.channel.bind('client-node-dragged', (data: NodeTranslatedEvent) => {
      console.log('NODE DRAGGED EVENT');

      const area = this.area.parent as AreaPlugin<Schemes, AreaExtra>;
      const node = area.nodeViews.get(data.nodeId);
      if (node) {
        this.externalDrag = true;
        node.translate(data.position.x, data.position.y);
      }
    });

    builderState.channel.bind('client-node-created', (data: INode) => {
      console.log('NODE CREATED EVENT');
      this.externalAdd = true;
      const node = parseNode(data);
      editor.addNode(node);
    });

    builderState.channel.bind('client-node-removed', (nodeId: string) => {
      console.log('NODE REMOVED EVENT');
      this.externalRemove = true;
      editor.removeNode(nodeId);
    });

    builderState.channel.bind('client-connection-created', (connectionData: ConnProps) => {
      console.log('CONNECTION CREATED EVENT');
      this.externalConnectionCreated = true;
      editor.addConnection(connectionData);
    });

    builderState.channel.bind('client-connection-removed', (connectionId: string) => {
      console.log('CONNECTION REMOVED EVENT');

      this.externalConnectionRemoved = true;
      editor.removeConnection(connectionId);
    });
  }
}
