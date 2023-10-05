import { BaseSchemes, Root, Scope, ClassicPreset, NodeEditor } from 'rete';
import { Area2D, AreaPlugin, BaseArea } from 'rete-area-plugin';
import { Connection, ConnectionPlugin } from 'rete-connection-plugin';
import { builderState, getLockedBy, versionHasStatus } from '../state';
import {
  EventData,
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
  unlockElement,
  handleEvent
} from '../sync';
import { Channel, PresenceChannel } from 'pusher-js';
import { AreaExtra, ConnProps, NodeProps, Schemes } from '../use-editor';
import { INode } from '../serializable';
import { cacheControlsMapping, createNodeInstance, parseNode } from '../factories/node-factory';
import { Produces } from 'rete-vue-plugin';
import { Member } from '../../../../composables/ws/usePresenceChannel';
import { animateBetweenTwoPoints, calculatePointsBetween } from '../../../../utils/animate';
import { addNodeAtPosition, cloneNodeAndAdd, omitSyncEvents, removeNodeAndConnections } from '../editor-utils';
import { TaskVersion, TaskVersionStatus } from '../../../../model/ai/tasks/task';
import { getEnv } from '../../../../config';
import { getCurrentTime } from '../../../../utils/time';
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
  nodeChangedPosition = false;

  areaPlugin: AreaPlugin<Schemes, AreaExtra>;
  editor: NodeEditor<Schemes>;

  constructor() {
    this.areaPlugin = this.area.parent;
    this.editor = this.root.parent;

    this.root.addPipe((context) => {
      if (!this.areaPlugin) {
        this.areaPlugin = this.area.parent;
      }
      if (!this.editor) {
        this.editor = this.root.parent;
      }
      if (builderState.omitSyncEvents) {
        return context;
      }
      if (
        builderState.builderLoaded &&
        builderState.initialGraphLoaded &&
        (context.type === 'nodecreated' ||
          context.type === 'noderemoved' ||
          context.type === 'connectioncreated' ||
          context.type === 'connectionremoved')
      ) {
        // if (context.type === 'noderemoved') {
        //   if (!this.externalRemove) {
        //     pushNodeRemovedEvent(builderState.channel as PresenceChannel, context.data.id);
        //     builderState.shouldSaveEditor = true;
        //   }
        //   this.externalRemove = false;
        // }

        if (context.type === 'connectioncreated') {
          if (!this.externalConnectionCreated) {
            pushConnectionCreatedEvent(builderState.channel as PresenceChannel, context.data);
            builderState.shouldSaveEditor = true;
          }
          this.externalConnectionCreated = false;
        }

        if (context.type === 'connectionremoved') {
          if (!this.externalConnectionRemoved) {
            pushConnectionRemovedEvent(builderState.channel as PresenceChannel, context.data.id);
            builderState.shouldSaveEditor = true;
          }
          this.externalConnectionRemoved = false;
        }
      }

      return context;
    });
    this.area.addPipe((context) => {
      if (builderState.omitSyncEvents) {
        return context;
      }
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
          if (versionHasStatus.value) {
            return;
          }
          if (this.externalDrag) {
            return context;
          }
          const node = this.editor.getNode(context.data.id);
          if (!node.lockStatus?.externalLock) {
            if (
              context.data.position.x !== context.data.previous.x ||
              context.data.position.y !== context.data.previous.y
            ) {
              this.nodeChangedPosition = true;
            }
            return context;
          }
          return;
        }

        if (context.type === 'nodetranslated') {
          if (!this.externalDrag && this.nodeChangedPosition) {
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
          if (this.nodeChangedPosition) {
            builderState.shouldSaveEditor = true;
            this.nodeChangedPosition = false;
          }
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
      if (!versionHasStatus.value) return context;
      if (context.type === 'connectionpick') return;
      return context;
    });
  }

  async createNode(node: NodeProps, position: { x: number; y: number } = { x: 0, y: 0 }) {
    const created = await this.editor.addNode(node);
    if (!created) {
      return;
    }
    await this.areaPlugin.translate(node.id, position);
    const createdNode = this.editor.getNode(node.id);
    pushNodeCreatedEvent(builderState.channel as PresenceChannel, {
      node: createdNode.serialize(),
      position
    });
    builderState.shouldSaveEditor = true;
  }

  async cloneNode(nodeId: string) {
    const { clonedNode, position } = await omitSyncEvents(cloneNodeAndAdd, this.editor, this.areaPlugin, nodeId);
    cacheControlsMapping(clonedNode);
    pushNodeCreatedEvent(builderState.channel as PresenceChannel, {
      node: clonedNode.serialize(),
      position: position
    });

    builderState.shouldSaveEditor = true;
  }

  async removeNode(nodeId: string) {
    await removeNodeAndConnections(this.editor, nodeId);
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

    const showDebug = getEnv('WEBSOCKET_DEBUG').toLowerCase() === 'true';

    builderState.memberRemovedCallbacks.push((leftMember: Member) => {
      if (!builderState.task?.lockStatus) {
        return;
      }
      for (const [key, value] of Object.entries(builderState.task.lockStatus)) {
        if (value === leftMember.id) {
          delete builderState.task.lockStatus[key];
          const node = this.editor.getNode(key);
          if (node) {
            node.unlock();
            this.areaPlugin.update('node', key);
          }
        }
      }
    });

    builderState.channel.bind(
      'client-response',
      (event: EventData<EventData<any>>) => {
        const timeDiff = getCurrentTime() - event.data.timestamp;
        // console.log(`${event.event} took ${timeDiff}ms to receive`);
        console.log(event.data.userId, event.data.event, event.userId, timeDiff  / 2);
      }
    )

    builderState.channel.bind(
      'client-node-dragged',
      handleEvent((event: EventData<NodeTranslatedEvent>) => {
        const area = this.area.parent as AreaPlugin<Schemes, AreaExtra>;
        const node = area.nodeViews.get(event.data.nodeId);

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
          node.translate(event.data.position.x, event.data.position.y);
          // const points = calculatePointsBetween(node.position, data.position, 100);
          // for (const point of pointss) {
          //   node.translate(point.x, point.y);
          // }
        }
      }, showDebug, builderState.channel as PresenceChannel)
    );

    builderState.channel.bind(
      'client-node-created',
      handleEvent(async (event: EventData<{ node: INode; position: { x: number; y: number } }>) => {
        // console.log('NODE CREATED EVENT', event.data.node, event.data.position);
        await omitSyncEvents(
          addNodeAtPosition,
          this.editor,
          this.areaPlugin,
          parseNode(event.data.node),
          event.data.position
        );
      }, showDebug, builderState.channel as PresenceChannel)
    );

    builderState.channel.bind(
      'client-node-removed',
      handleEvent(async (event: EventData<string>) => {
        await removeNodeAndConnections(this.editor, event.data);
      }, showDebug, builderState.channel as PresenceChannel)
    );

    builderState.channel.bind(
      'client-node-locked',
      handleEvent((event: EventData<{ nodeId: string; userId: string }>) => {
        const node = this.editor.getNode(event.data.nodeId);
        node.lock({
          lockedBy: builderState.channel?.members.get(event.userId),
          externalLock: true
        });
        // const nodeView = this.areaPlugin.nodeViews.get(data.nodeId);
        // if (nodeView?.element) {
        //   nodeView.element.style.transition = 'transform 50ms ease-in-out';
        // }
        if (builderState.task) {
          if (builderState.task.lockStatus) {
            builderState.task.lockStatus[event.data.nodeId] = event.userId;
          } else {
            builderState.task.lockStatus = {
              [event.data.nodeId]: event.userId
            };
          }
        }

        this.areaPlugin.update('node', event.data.nodeId);
        this.externalPicked = true;
      }, showDebug, builderState.channel as PresenceChannel)
    );
    builderState.channel.bind(
      'client-node-unlocked',
      handleEvent((event: EventData<string>) => {
        // console.log('CLIENT NODE UNLOCKED');
        delete builderState.task?.lockStatus[event.data];
        this.editor.getNode(event.data)?.unlock();
        // const nodeView = this.areaPlugin.nodeViews.get(nodeId);
        // if (nodeView?.element) {
        //   nodeView.element.style.transition = '';
        // }
        this.areaPlugin.update('node', event.data);
      }, showDebug, builderState.channel as PresenceChannel)
    );

    builderState.channel.bind(
      'client-connection-created',
      handleEvent((event: EventData<ConnProps>) => {
        // // console.log('CONNECTION CREATED EVENT');
        this.externalConnectionCreated = true;
        this.editor.addConnection(event.data);
      }, showDebug, builderState.channel as PresenceChannel)
    );

    builderState.channel.bind(
      'client-connection-removed',
      handleEvent((event: EventData<string>) => {
        // // console.log('CONNECTION REMOVED EVENT');

        this.externalConnectionRemoved = true;
        this.editor.removeConnection(event.data);
      }, showDebug, builderState.channel as PresenceChannel)
    );

    builderState.channel.bind(
      'client-control-locked',
      handleEvent((event: EventData<string>) => {
        const controlId = event.data;
        const node = builderState.controlToNode.get(controlId);
        const control = node?.getControl(controlId);
        if (node && node.lockStatus && control && control.lockStatus) {
          node.lockStatus.lockedControlId = controlId;
          control.lockStatus.lockedControlId = controlId;
          this.areaPlugin.update('control', controlId);
          this.areaPlugin.update('node', node.id);
        }
      }, showDebug, builderState.channel as PresenceChannel)
    );

    builderState.channel.bind(
      'client-control-unlocked',
      handleEvent((event: EventData<string>) => {
        const controlId = event.data;
        const node = builderState.controlToNode.get(controlId);
        const control = node?.getControl(controlId);
        if (node && node.lockStatus && control && control.lockStatus) {
          node.lockStatus.lockedControlId = undefined;
          control.lockStatus.lockedControlId = undefined;
          this.areaPlugin.update('control', controlId);
          this.areaPlugin.update('node', node.id);
        }
      }, showDebug, builderState.channel as PresenceChannel)
    );

    builderState.channel.bind(
      'client-control-changed',
      handleEvent((event: EventData<{ nodeId: string; controlId: string; value: any }>) => {
        const node = builderState.controlToNode.get(event.data.controlId);
        if (!node) {
          return;
        }
        const control = node.getControl(event.data.controlId);
        if (control) {
          control.setValue(...event.data.value);
        }
      }, showDebug, builderState.channel as PresenceChannel)
    );

    builderState.channel.bind(
      'client-training-started',
      handleEvent((event: EventData<TaskVersionStatus>) => {
        if (builderState.selectedVersion) {
          builderState.selectedVersion.status = event.data;
        }
      }, showDebug, builderState.channel as PresenceChannel)
    );

    builderState.channel.bind(
      'client-training-reseted',
      handleEvent((event: EventData<TaskVersion>) => {
        if (event.data) {
          builderState.selectedVersion = event.data;
          builderState.versionMetrics = undefined;
        }
      }, showDebug, builderState.channel as PresenceChannel)
    );
  }
}
