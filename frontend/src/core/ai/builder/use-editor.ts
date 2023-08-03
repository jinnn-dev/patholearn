import { NodeEditor, GetSchemes, ClassicPreset } from 'rete';
import { AreaPlugin, AreaExtensions } from 'rete-area-plugin';
import { ConnectionPlugin, Presets as ConnectionPresets } from 'rete-connection-plugin';
import { VuePlugin, Presets, VueArea2D } from 'rete-vue-plugin';
import { AutoArrangePlugin, ArrangeAppliers } from 'rete-auto-arrange-plugin';

import CustomNodeVue from '../../../components/ai/builder/CustomNode.vue';
import CustomConnectionVue from '../../../components/ai/builder/CustomConnection.vue';
import CustomSocketVue from '../../../components/ai/builder/CustomSocket.vue';
import DimensionControlVue from '../../../components/ai/builder/controls/DimensionControl.vue';
import NumberControlVue from '../../../components/ai/builder/controls/NumberControl.vue';
import DropdownControlVue from '../../../components/ai/builder/controls/DropdownControl.vue';
import AsyncDropdownControlVue from '../../../components/ai/builder/controls/AsyncDropdownControl.vue';
import DiagramControlVue from '../../../components/ai/builder/controls/DiagramControl.vue';
import MetricControlVue from '../../../components/ai/builder/controls/MetricControl.vue';

import { DropdownControl } from './controls/dropdown-control';
import { NumberControl } from './controls/number-control';
import { Ref, ref } from 'vue';
import { IConnection, IGraph, INode, INodePositions } from './serializable';
import { addCustomBackground } from './plugins/custom-background';
import { NodeClassesType, NodeType } from './nodes/types';
import { DimensionControl } from './controls/dimension-control';
import { ContextMenuExtra, ContextMenuPlugin } from 'rete-context-menu-plugin';
import { setupContext, setupContextItems } from './plugins/context-menu';
import { arrangeSetup } from './plugins/arrange-nodes';
import { SyncPlugin } from './plugins/sync-plugin';
import { createNodeInstance, parseNode } from './factories/node-factory';
import { builderState } from './state';
import { MousePlugin, setupMousePlugin } from './plugins/mouse-plugin';
import { selectableNodes, selector } from './trackedSelector';
import { pushTrainingStarted } from './sync';
import { PresenceChannel } from 'pusher-js';
import { DiagramControl } from './controls/diagram-control';
import { nodesCanConnect } from './validators/socket-validator';
import { AsyncDropdownControl, MetricControl } from './controls';
import { nodeCanBeCreated, validateNodes } from './validators/node-validator';
import { validateConnections } from './validators/connection-validator';

export type NodeProps = NodeClassesType;

export class Connection<A extends NodeProps, B extends NodeProps> extends ClassicPreset.Connection<A, B> {}

export type ConnProps = Connection<NodeClassesType, NodeClassesType> | Connection<NodeClassesType, NodeClassesType>;
export type Schemes = GetSchemes<NodeProps, ConnProps>;

export type AreaExtra = VueArea2D<Schemes> | ContextMenuExtra;

export function useEditor() {
  const eventsRegisterd = ref(false);

  const area: Ref<AreaPlugin<Schemes, AreaExtra> | undefined> = ref();
  const connection: Ref<ConnectionPlugin<Schemes, AreaExtra> | undefined> = ref();
  const render: Ref<VuePlugin<Schemes> | undefined> = ref();
  const editor: Ref<NodeEditor<Schemes> | undefined> = ref();
  const contextMenu: Ref<ContextMenuPlugin<Schemes> | undefined> = ref();
  const sync: Ref<SyncPlugin | undefined> = ref();
  const mousePlugin: Ref<MousePlugin<Schemes> | undefined> = ref();
  const arrange: Ref<AutoArrangePlugin<any> | undefined> = ref();
  const animationApplier: Ref<ArrangeAppliers.TransitionApplier<any, never> | undefined> = ref();

  const loading = ref(false);

  const init = async (container: HTMLElement) => {
    builderState.builderLoaded = false;

    // socket.value = new ClassicPreset.Socket('socket');
    editor.value = new NodeEditor<Schemes>();
    area.value = new AreaPlugin<Schemes, AreaExtra>(container);
    connection.value = new ConnectionPlugin<Schemes, AreaExtra>();
    render.value = new VuePlugin<Schemes>();
    sync.value = new SyncPlugin();

    builderState.syncPlugin = sync.value;

    contextMenu.value = new ContextMenuPlugin<Schemes>({
      items: setupContextItems([
        ['Input', [['Dataset', () => createNodeInstance('DatasetNode') as NodeProps]]],
        [
          'Layer',
          [
            ['Conv2D', () => createNodeInstance('Conv2DNode') as NodeProps],
            ['Linear', () => createNodeInstance('LinearNode') as NodeProps],
            ['Pooling', () => createNodeInstance('PoolingNode') as NodeProps]
          ]
        ],
        ['Architecture', [['ResNet', () => createNodeInstance('ResNetNode') as NodeProps]]],
        [
          'Transform',
          [
            ['Dropout', () => createNodeInstance('DropoutNode') as NodeProps],
            ['Flatten', () => createNodeInstance('FlattenNode') as NodeProps],
            ['Batch Norm.', () => createNodeInstance('BatchNormNode') as NodeProps]
          ]
        ],
        [
          'Combine',
          [
            ['Add', () => createNodeInstance('AddNode') as NodeProps],
            ['Concatenate', () => createNodeInstance('ConcatenateNode') as NodeProps]
          ]
        ],
        ['Output', () => createNodeInstance('OutputNode') as NodeProps],
        ['Metric', () => createNodeInstance('MetricNode') as NodeProps]
      ])
    });

    mousePlugin.value = new MousePlugin();

    arrange.value = new AutoArrangePlugin<any>();

    animationApplier.value = new ArrangeAppliers.TransitionApplier<any, never>({
      duration: 300,
      timingFunction: (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2)
    });
    addCustomBackground(area.value);
    selectableNodes(area.value, selector(), { accumulating: AreaExtensions.accumulateOnCtrl() });

    const presets = Presets.classic.setup({
      customize: {
        // @ts-ignore
        node(data) {
          return CustomNodeVue;
        },
        // @ts-ignore
        connection(data) {
          return CustomConnectionVue;
        },
        // @ts-ignore
        socket(data) {
          return CustomSocketVue;
        },
        // @ts-ignore
        control(data) {
          if (data.payload instanceof MetricControl) {
            return MetricControlVue;
          }
          if (data.payload instanceof DiagramControl) {
            return DiagramControlVue;
          }
          if (data.payload instanceof DropdownControl) {
            return DropdownControlVue;
          }
          if (data.payload instanceof AsyncDropdownControl) {
            return AsyncDropdownControlVue;
          }
          if (data.payload instanceof NumberControl) {
            return NumberControlVue;
          }
          if (data.payload instanceof DimensionControl) {
            return DimensionControlVue;
          }
          if (data.payload instanceof ClassicPreset.InputControl) {
            return Presets.classic.Control;
          }
        }
      }
    });

    // @ts-ignore
    render.value.addPreset(presets);
    // @ts-ignore
    render.value.addPreset(setupContext({ delay: 3000 }));
    // @ts-ignore
    render.value.addPreset(setupMousePlugin({ delay: 300 }));

    connection.value.addPreset(ConnectionPresets.classic.setup());

    arrange.value.addPreset(arrangeSetup({ distance: 20 }));

    editor.value.use(area.value);
    editor.value.use(sync.value.root);
    builderState.editor = editor.value;
    // TODO: ADJUST -> PREVENT CONNECTION CREATION BASED ON SOCKET OBJECT
    // editor.value.addPipe((context) => {
    //   if (context.type === 'connectioncreate') {
    //     // const source = editor.value!.getNode(context.data.source);
    //     // const sourceSocket = source.outputs[context.data.sourceOutput]?.socket;
    //     // const target = editor.value!.getNode(context.data.target);
    //     // const targetSocket = (target.inputs as any)[context.data.targetInput]?.socket;

    //     console.log(sourceSocket, targetSocket);

    //     if (sourceSocket !== targetSocket) return; // prevent 'connectioncreate' if the ports have different sockets
    //   }
    //   return context;
    // });

    editor.value.addPipe((context) => {
      if (!editor.value) {
        return;
      }

      if (context.type === 'nodecreate') {
        if (!nodeCanBeCreated(context.data, editor.value)) {
          return;
        }
        return context;
      }

      if (context.type === 'connectioncreate') {
        const source = editor.value.getNode(context.data.source);
        const target = editor.value.getNode(context.data.target);

        if (!nodesCanConnect(source, target)) {
          return;
        }

        return context;
      }
      return context;
    });

    area.value.use(connection.value);
    area.value.use(render.value);
    area.value.use(arrange.value);
    area.value.use(contextMenu.value);
    // @ts-ignore
    area.value.use(mousePlugin.value);

    area.value.use(sync.value.area);

    // sync.value.area.use(render.value);
    // @ts-ignore
    connection.value.use(sync.value.connection);

    area.value.area.content.holder.style.height = '100%';

    AreaExtensions.simpleNodesOrder(area.value);

    await arrangeLayout();
    await zoomAt();

    // Hacky way to disable double click zooming
    // @ts-ignore
    area.value.area.zoomHandler.container.removeEventListener('dblclick', area.value.area.zoomHandler.dblclick);

    builderState.builderLoaded = true;
  };

  const arrangeLayout = async () => {
    await arrange.value?.layout({
      applier: animationApplier.value
    });
  };

  const addNode = async (layerType: NodeType) => {
    if (!editor.value) {
      return;
    }
    let layer = createNodeInstance(layerType);

    if (!layer) {
      return;
    }

    const container = area.value?.area.content.holder;
    let position = { x: 0, y: 0 };
    if (container && area.value) {
      const [hw, hh] = [container.clientWidth / 2, container.clientHeight / 2];

      const transform = area.value.area.transform;
      const center = [(hw - transform.x) / transform.k, (hh - transform.y) / transform.k];
      position.x = center[0];
      position.y = center[1];
    }

    await sync.value?.createNode(layer as NodeProps, position);
  };

  const zoomAt = async () => {
    if (!area.value || !editor.value) {
      return;
    }
    await AreaExtensions.zoomAt(area.value, editor.value.getNodes());
  };

  const validate = async () => {
    if (!editor.value) {
      return;
    }
    const nodesAreValid = validateNodes(editor.value);
    const connectionsAreValid = validateConnections(editor.value);

    return nodesAreValid && connectionsAreValid;
  };

  const download = (): IGraph => {
    const nodeData: INode[] = [];
    const nodePositions: INodePositions[] = [];

    const nodes = editor.value?.getNodes();
    for (const node of nodes || []) {
      const serializedNode = node.serialize();
      nodeData.push(serializedNode);
      const position = area.value?.nodeViews.get(serializedNode.id)?.position;
      if (position) {
        nodePositions.push({
          id: serializedNode.id,
          x: position.x,
          y: position.y
        });
      }
    }

    const connectionsData: IConnection[] = [];
    const connections = editor.value?.getConnections();

    for (const connection of connections || []) {
      const conData: IConnection = {
        id: connection.id,
        source: connection.source,
        sourceOutput: connection.sourceOutput,
        target: connection.target,
        targetInput: connection.targetInput
      };
      connectionsData.push(conData);
    }

    const graphData: IGraph = {
      nodes: nodeData,
      connections: connectionsData,
      positions: nodePositions
    };

    return graphData;
  };

  const importGraph = async (graph: IGraph) => {
    builderState.initialGraphLoaded = false;
    await editor.value?.clear();

    for (const nodeData of graph.nodes) {
      const node = parseNode(nodeData);
      await editor.value?.addNode(node);
    }

    for (const connectionData of graph.connections) {
      const sourceNode = editor.value!.getNode(connectionData.source);
      const sourceOutput = connectionData.sourceOutput;

      const targetNode = editor.value?.getNode(connectionData.target);
      const targetInput = connectionData.targetInput;

      // @ts-ignore
      const connection = new Connection(sourceNode, sourceOutput, targetNode, targetInput);
      connection.id = connectionData.id;
      await editor.value?.addConnection(connection);
    }

    for (const position of graph.positions) {
      await area.value?.translate(position.id, { x: position.x, y: position.y });
    }

    await zoomAt();

    builderState.initialGraphLoaded = true;
  };

  const startTraining = () => {
    pushTrainingStarted(builderState.channel as PresenceChannel, 'creating');
  };

  const clear = async () => {
    await editor.value?.clear();
    await zoomAt();
  };

  const registerEvents = () => {
    if (eventsRegisterd.value) {
      return;
    }

    sync.value?.registerEvents();
    eventsRegisterd.value = true;
  };

  return {
    editor,
    loading,
    arrangeLayout,
    zoomAt,
    download,
    importGraph,
    init,
    clear,
    addNode,
    validate,
    area,
    registerEvents,
    startTraining,
    destroy: () => area.value?.destroy()
  };
}
