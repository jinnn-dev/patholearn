import { BaseSchemes, Root, Scope, ClassicPreset, NodeEditor } from 'rete';
import { Area2D, AreaPlugin, BaseArea } from 'rete-area-plugin';
import { Connection, ConnectionPlugin } from 'rete-connection-plugin';
import { builderState, getLockedBy } from '../state';
import {
  NodeTranslatedEvent,
  lockElement,
  pushConnectionCreatedEvent,
  pushConnectionRemovedEvent,
  pushControlChanged,
  pushControlLock,
  pushControlUnlock,
  pushNodeCreatedEvent,
  pushNodeRemovedEvent,
  pushNodeTranslatedEvent,
  unlockElement
} from '../sync';
import { Channel, PresenceChannel } from 'pusher-js';
import { AreaExtra, ConnProps, NodeProps, Schemes } from '../use-editor';
import { INode } from '../serializable';
import { createNodeInstance, parseNode } from '../factories/node-factory';
import { Produces } from 'rete-vue-render-plugin';
import { Member } from '../../../../composables/ws/usePresenceChannel';
import { animateBetweenTwoPoints, calculatePointsBetween } from '../../../../utils/animate';

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

        if (context.type === 'nodetranslate') {
          if (this.externalDrag) {
            return context;
          }
          const node = this.editor.getNode(context.data.id);
          if (!node.lockStatus?.externalLock) {
            return context;
          }
          return;
        }

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

        // if (context.type === 'nodedragged') {
        //   console.log(context.data);

        //   builderState.shouldSaveEditor = true;
        //   return context;
        // }

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

  cloneNode(nodeId: string) {
    const node = this.editor.getNode(nodeId);
    this.editor.addNode(node.duplicate());
  }

  async removeNode(nodeId: string) {
    const connections = this.editor.getConnections().filter((c) => {
      return c.source === nodeId || c.target === nodeId;
    });
    for (const connection of connections) {
      await this.editor.removeConnection(connection.id);
    }
    await this.editor.removeNode(nodeId);
    pushNodeRemovedEvent(builderState.channel as PresenceChannel, nodeId);
    builderState.shouldSaveEditor = true;
  }

  selectControl(controlId: string) {
    const nodeToSelect = builderState.controlToNode.get(controlId);
    const control = nodeToSelect?.getControl(controlId);
    if (!control?.lockStatus?.lockedControlId) {
      this.areaPlugin.emit({
        type: 'nodepicked',
        data: {
          id: nodeToSelect!.id
        }
      });

      pushControlLock(builderState.channel as PresenceChannel, controlId);
      lockElement(builderState.task!.id, controlId, builderState.me!.id);
    }
  }

  unselectControl(controlId: string) {
    pushControlUnlock(builderState.channel as PresenceChannel, controlId);
    unlockElement(builderState.task!.id, controlId, builderState.me!.id);
    builderState.shouldSaveEditor = true;
  }

  controlChanged(controlId: string, ...value: any) {
    const node = builderState.controlToNode.get(controlId);
    if (!node) {
      return;
    }
    pushControlChanged(builderState.channel as PresenceChannel, node.id, controlId, ...value);
  }

  registerEvents() {
    if (this.eventsRegistered || !builderState.channel) {
      return;
    }

    builderState.memberRemovedCallbacks.push((leftMember: Member) => {
      if (!builderState.task?.lockStatus) {
        return;
      }
      for (const [key, value] of Object.entries(builderState.task.lockStatus)) {
        if (value === leftMember.id) {
          delete builderState.task.lockStatus[key];
          const node = this.editor.getNode(key);
          node.unlock();
          this.areaPlugin.update('node', key);
        }
      }
    });

    builderState.channel.bind('client-node-dragged', async (data: NodeTranslatedEvent) => {
      console.log('NODE DRAGGED EVENT');

      const area = this.area.parent as AreaPlugin<Schemes, AreaExtra>;
      const node = area.nodeViews.get(data.nodeId);
      if (node) {
        this.externalDrag = true;
        // node.translate(data.position.x, data.position.y);
        const translate = async (x: number, y: number) => {
          // console.log(x, y);

          await node.translate(x, y);
          node.position = { x: x, y: y };
          // console.log(node.position);
        };

        // await animateBetweenTwoPoints(node.position, { x: data.position.x, y: data.position.y }, 0.05, translate);
        node.translate(data.position.x, data.position.y);
        // const points = calculatePointsBetween(node.position, data.position, 100);
        // for (const point of points) {
        //   node.translate(point.x, point.y);
        // }
      }
    });

    builderState.channel.bind('client-node-created', async (data: INode) => {
      console.log('NODE CREATED EVENT');
      this.externalAdd = true;
      const node = parseNode(data);
      this.editor.addNode(node);
    });

    builderState.channel.bind('client-node-removed', async (nodeId: string) => {
      console.log('NODE REMOVED EVENT');
      this.externalRemove = true;
      const connections = this.editor.getConnections().filter((c) => {
        return c.source === nodeId || c.target === nodeId;
      });
      for (const connection of connections) {
        await this.editor.removeConnection(connection.id);
      }
      await this.editor.removeNode(nodeId);
    });

    builderState.channel.bind('client-node-locked', (data: { nodeId: string; userId: string }) => {
      console.log('CLIENT NODE LOCKED');
      const node = this.editor.getNode(data.nodeId);
      node.lock({
        lockedBy: builderState.channel?.members.get(data.userId),
        externalLock: true
      });
      // const nodeView = this.areaPlugin.nodeViews.get(data.nodeId);
      // if (nodeView?.element) {
      //   nodeView.element.style.transition = 'transform 50ms ease-in-out';
      // }
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
      // const nodeView = this.areaPlugin.nodeViews.get(nodeId);
      // if (nodeView?.element) {
      //   nodeView.element.style.transition = '';
      // }
      this.areaPlugin.update('node', nodeId);
    });

    builderState.channel.bind('client-connection-created', (connectionData: ConnProps) => {
      console.log('CONNECTION CREATED EVENT');
      this.externalConnectionCreated = true;
      this.editor.addConnection(connectionData);
    });

    builderState.channel.bind('client-connection-removed', (connectionId: string) => {
      console.log('CONNECTION REMOVED EVENT');

      this.externalConnectionRemoved = true;
      this.editor.removeConnection(connectionId);
    });

    builderState.channel.bind('client-control-locked', (controlId: string) => {
      console.log('CONTROL LOCKED EVENT');

      const node = builderState.controlToNode.get(controlId);
      const control = node?.getControl(controlId);
      if (node && node.lockStatus && control && control.lockStatus) {
        node.lockStatus.lockedControlId = controlId;
        control.lockStatus.lockedControlId = controlId;
        this.areaPlugin.update('control', controlId);
        this.areaPlugin.update('node', node.id);
      }
    });

    builderState.channel.bind('client-control-unlocked', (controlId: string) => {
      console.log('CONTROL UNLOCKED EVENT');

      const node = builderState.controlToNode.get(controlId);
      const control = node?.getControl(controlId);
      if (node && node.lockStatus && control && control.lockStatus) {
        node.lockStatus.lockedControlId = undefined;
        control.lockStatus.lockedControlId = undefined;
        this.areaPlugin.update('control', controlId);
        this.areaPlugin.update('node', node.id);
      }
    });

    builderState.channel.bind('client-control-changed', (data: { nodeId: string; controlId: string; value: any }) => {
      const node = builderState.controlToNode.get(data.controlId);
      if (!node) {
        return;
      }
      const control = node.getControl(data.controlId);
      if (control) {
        control.setValue(...data.value);
      }
    });
  }
}
