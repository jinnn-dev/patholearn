import { BaseSchemes, Root, Scope, ClassicPreset, NodeEditor } from 'rete';
import { Area2D, AreaPlugin, BaseArea } from 'rete-area-plugin';
import { Connection, ConnectionPlugin } from 'rete-connection-plugin';
import { builderState, getLockedBy } from '../state';
import {
  NodeTranslatedEvent,
  lockElement,
  pushConnectionCreatedEvent,
  pushConnectionRemovedEvent,
  pushNodeCreatedEvent,
  pushNodeLockedEvent,
  pushNodeRemovedEvent,
  pushNodeTranslatedEvent,
  pushNodeUnlockedEvent,
  unlockElement
} from '../sync';
import { Channel, PresenceChannel } from 'pusher-js';
import { AreaExtra, ConnProps, Schemes } from '../use-editor';
import { INode } from '../serializable';
import { parseNode } from '../factories/node-factory';
import { Produces } from 'rete-vue-render-plugin';
import { Member } from 'composables/ws/usePresenceChannel';

export class SyncPlugin {
  root = new Scope<never, [Root<Schemes>]>('sync');
  area = new Scope<never, [BaseArea<Schemes>, Root<Schemes>]>('sync');
  connection = new Scope<never, [Connection, Root<Schemes>]>('sync');
  render = new Scope<never, [Produces<Schemes>, Root<Schemes>]>('sync');

  eventsRegistered = false;

  externalDrag = false;
  externalAdd = false;
  externalRemove = false;
  externalConnectionCreated = false;
  externalConnectionRemoved = false;
  externalPicked = false;

  areaPlugin: AreaPlugin<Schemes, AreaExtra>;
  editor: NodeEditor<Schemes>;

  constructor() {
    this.areaPlugin = this.area.parent;
    this.editor = this.root.parent;

    // this.root.parentScope()?.addPipe((context) => {
    //   console.log('CONTEXT', context.type);
    //   return context;
    // });

    this.root.addPipe((context) => {
      if (!this.areaPlugin) {
        this.areaPlugin = this.area.parent;
      }
      if (!this.editor) {
        this.editor = this.root.parent;
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
            pushNodeCreatedEvent(builderState.channel as PresenceChannel, context.data.serialize());
            builderState.shouldSaveEditor = true;
          }
          this.externalAdd = false;
        }

        if (context.type === 'noderemoved') {
          if (!this.externalRemove) {
            pushNodeRemovedEvent(builderState.channel as PresenceChannel, context.data.id);
            builderState.shouldSaveEditor = true;
          }
          this.externalRemove = false;
        }

        if (context.type === 'connectioncreated') {
          if (!this.externalConnectionCreated) {
            pushConnectionCreatedEvent(builderState.channel as PresenceChannel, context.data);
            builderState.shouldSaveEditor = true;
          }
        }

        if (context.type === 'connectionremoved') {
          if (!this.externalConnectionRemoved) {
            pushConnectionRemovedEvent(builderState.channel as PresenceChannel, context.data.id);
            builderState.shouldSaveEditor = true;
          }
        }
      }

      return context;
    });
    this.area.addPipe((context) => {
      // console.log(context);

      if (builderState.builderLoaded && builderState.initialGraphLoaded) {
        // if (context.type === 'nodepicked' && builderState.channel && !this.externalPicked) {
        //   const node = this.editor.getNode(context.data.id);
        //   if (!node.lockStatus) {
        //     pushNodeLockedEvent(builderState.channel as PresenceChannel, context.data.id);
        //     this.externalPicked = false;
        //     return context;
        //   }

        //   return;
        // }

        if (context.type === 'nodetranslated') {
          if (builderState.channel && !this.externalDrag && !this.externalAdd) {
            pushNodeTranslatedEvent(builderState.channel as PresenceChannel, {
              userId: builderState.me!.id,
              nodeId: context.data.id,
              position: context.data.position,
              previous: context.data.previous
            });
          }
          this.externalDrag = false;
          return context;
        }

        if (context.type === 'nodedragged') {
          builderState.shouldSaveEditor = true;
          return context;
        }

        // if (context.type === 'pointerdown' || context.type === 'pointerup') {
        //   console.log(context);
        // }

        // if (context.type === 'rendered' && context.data.type === 'node') {
        //   if (!context.data.payload.selected) {
        //     pushNodeUnlockedEvent(builderState.channel as PresenceChannel, context.data.payload.id);
        //   }
        // }

        // if (context.type === 'unmount') {
        //   console.log(context);
        //   return context;
        // }
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

    builderState.memberRemovedCallbacks.push((leftMember: Member) => {
      if (!builderState.task?.lockStatus) {
        return;
      }
      for (const [key, value] of Object.entries(builderState.task.lockStatus)) {
        if (value === leftMember.id) {
          delete builderState.task.lockStatus[key];
          const node = editor.getNode(key);
          node.unlock();
          this.areaPlugin.update('node', key);
        }
      }
    });

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

    builderState.channel.bind('client-node-locked', (data: { nodeId: string; userId: string }) => {
      console.log('CLIENT NODE LOCKED');

      this.editor.getNode(data.nodeId).lock({
        lockedBy: builderState.channel?.members.get(data.userId)
      });
      if (builderState.task) {
        if (builderState.task.lockStatus) {
          builderState.task.lockStatus[data.nodeId] = data.userId;
        } else {
          builderState.task.lockStatus = {
            [data.nodeId]: data.userId
          };
        }
      }

      this.areaPlugin.update('node', data.nodeId);
      this.externalPicked = true;
    });

    builderState.channel.bind('client-node-unlocked', (nodeId: string) => {
      console.log('CLIENT NODE UNLOCKED');
      delete builderState.task?.lockStatus[nodeId];
      this.editor.getNode(nodeId).unlock();
      this.areaPlugin.update('node', nodeId);
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
