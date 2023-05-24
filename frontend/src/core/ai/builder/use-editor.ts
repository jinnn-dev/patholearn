import { NodeEditor, GetSchemes, ClassicPreset } from 'rete';
import { AreaPlugin, AreaExtensions } from 'rete-area-plugin';
import { ConnectionPlugin, Presets as ConnectionPresets } from 'rete-connection-plugin';
import { VueRenderPlugin, Presets, VueArea2D } from 'rete-vue-render-plugin';
import { AutoArrangePlugin, ArrangeAppliers } from 'rete-auto-arrange-plugin';

import CustomNodeVue from '../../../components/ai/builder/CustomNode.vue';
import CustomConnectionVue from '../../../components/ai/builder/CustomConnection.vue';
import DimensionControlVue from '../../../components/ai/builder/controls/DimensionControl.vue';
import NumberControlVue from '../../../components/ai/builder/controls/NumberControl.vue';
import DropdownControlVue from '../../../components/ai/builder/controls/DropdownControl.vue';

import { DatasetNode } from './nodes/input/dataset-node';
import { DropdownControl } from './controls/dropdown-control';
import { Conv2DNode } from './nodes/layer/conv2d-node';
import { NumberControl } from './controls/number-control';
import { Ref, ref } from 'vue';
import { IConnection, IGraph, INode, INodePositions } from './serializable';
import { addCustomBackground } from './plugins/custom-background';
import { NodeType } from './nodes/types';
import { DimensionControl } from './controls/dimension-control';
import { ContextMenuExtra, ContextMenuPlugin, Presets as ContextMenuPresets } from 'rete-context-menu-plugin';
import { setupContext } from './plugins/context-menu';
import { LinearNode } from './nodes/layer/linear-node';
import { arrangeSetup } from './plugins/arrange-nodes';
import { DropoutNode } from './nodes/transform/dropout-node';
import { FlattenNode } from './nodes/transform/flatten-node';
import { BatchNormNode } from './nodes/transform/batch-norm-node';
import { PoolingNode } from './nodes/layer/pooling-node';
import { SyncPlugin } from './plugins/sync-plugin';
import { createNodeInstance, parseNode } from './factories/node-factory';

type NodeProps = DatasetNode | Conv2DNode | LinearNode | DropoutNode | FlattenNode | BatchNormNode | PoolingNode;

class Connection<A extends NodeProps, B extends NodeProps> extends ClassicPreset.Connection<A, B> {}

type ConnProps = Connection<DatasetNode, Conv2DNode> | Connection<Conv2DNode, Conv2DNode>;
type Schemes = GetSchemes<NodeProps, ConnProps>;

type AreaExtra = VueArea2D<Schemes> | ContextMenuExtra;

export function useEditor() {
  const socket: Ref<ClassicPreset.Socket | undefined> = ref();
  const area: Ref<AreaPlugin<Schemes, AreaExtra> | undefined> = ref();
  const connection: Ref<ConnectionPlugin<Schemes, AreaExtra> | undefined> = ref();
  const render: Ref<VueRenderPlugin<Schemes> | undefined> = ref();
  const editor: Ref<NodeEditor<Schemes> | undefined> = ref();
  const contextMenu: Ref<ContextMenuPlugin<Schemes> | undefined> = ref();
  const sync: Ref<SyncPlugin<Schemes> | undefined> = ref();

  const arrange: Ref<AutoArrangePlugin<Schemes> | undefined> = ref();
  const animationApplier: Ref<ArrangeAppliers.TransitionApplier<Schemes, never> | undefined> = ref();

  const loading = ref(false);

  const init = async (container: HTMLElement) => {
    loading.value = true;

    socket.value = new ClassicPreset.Socket('socket');
    editor.value = new NodeEditor<Schemes>();
    area.value = new AreaPlugin<Schemes, AreaExtra>(container);
    connection.value = new ConnectionPlugin<Schemes, AreaExtra>();
    render.value = new VueRenderPlugin<Schemes>();

    sync.value = new SyncPlugin();

    contextMenu.value = new ContextMenuPlugin<Schemes>({
      items: ContextMenuPresets.classic.setup([
        ['Input', [['Dataset', () => createNodeInstance('DatasetNode', socket.value!) as NodeProps]]],
        [
          'Layer',
          [
            ['Conv2D', () => createNodeInstance('Conv2DNode', socket.value!) as NodeProps],
            ['Linear', () => createNodeInstance('LinearNode', socket.value!) as NodeProps],
            ['Pooling', () => createNodeInstance('PoolingNode', socket.value!) as NodeProps]
          ]
        ],
        [
          'Transform',
          [
            ['Dropout', () => createNodeInstance('DropoutNode', socket.value!) as NodeProps],
            ['Flatten', () => createNodeInstance('FlattenNode', socket.value!) as NodeProps],
            ['Batch Norm.', () => createNodeInstance('BatchNormNode', socket.value!) as NodeProps]
          ]
        ]
      ])
    });
    arrange.value = new AutoArrangePlugin<Schemes>();

    animationApplier.value = new ArrangeAppliers.TransitionApplier<Schemes, never>({
      duration: 300,
      timingFunction: (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2)
    });
    addCustomBackground(area.value);

    AreaExtensions.selectableNodes(area.value, AreaExtensions.selector(), {
      accumulating: AreaExtensions.accumulateOnCtrl()
    });

    const presets = Presets.classic.setup({
      area,
      customize: {
        // @ts-ignore
        node(data) {
          return CustomNodeVue;
        },
        // @ts-ignore
        connection(data) {
          return CustomConnectionVue;
        },
        // // @ts-ignore
        // socket(data) {
        //   return CustomSocketVue;
        // },
        // @ts-ignore
        control(data) {
          if (data.payload instanceof DropdownControl) {
            return DropdownControlVue;
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
    connection.value.addPreset(ConnectionPresets.classic.setup());
    arrange.value.addPreset(arrangeSetup({ distance: 20 }));

    editor.value.use(area.value);
    editor.value.use(sync.value.root);

    area.value.use(connection.value);
    area.value.use(render.value);
    area.value.use(arrange.value);
    area.value.use(contextMenu.value);
    area.value.use(sync.value.area);

    // @ts-ignore
    connection.value.use(sync.value.connection);

    AreaExtensions.simpleNodesOrder(area.value);

    await arrangeLayout();
    await zoomAt();

    // Hacky way to disable double click zooming
    // @ts-ignore
    area.value.area.zoomHandler.container.removeEventListener('dblclick', area.value.area.zoomHandler.dblclick);

    loading.value = false;
  };

  const arrangeLayout = async () => {
    await arrange.value?.layout({
      applier: animationApplier.value
    });
  };

  const addNode = async (layerType: NodeType) => {
    if (!socket.value || !editor.value) {
      return;
    }
    let layer = createNodeInstance(layerType, socket.value);

    if (!layer) {
      return;
    }

    await editor.value.addNode(layer);
  };

  const zoomAt = async () => {
    if (!area.value || !editor.value) {
      return;
    }
    await AreaExtensions.zoomAt(area.value, editor.value.getNodes());
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
    loading.value = true;
    await editor.value?.clear();

    for (const nodeData of graph.nodes) {
      let node = parseNode(nodeData);
      // if (nodeData._type === Conv2DNode.name) {
      //   node = Conv2DNode.parse(nodeData as IConv2DNode);
      // } else if (nodeData._type === DatasetNode.name) {
      //   node = DatasetNode.parse(nodeData as IDatasetNode);
      // } else if (nodeData._type === LinearNode.name) {
      //   node = LinearNode.parse(nodeData as ILinearNode);
      // } else if (nodeData._type === DropoutNode.name) {
      //   node = DropoutNode.parse(nodeData as IDropoutNode);
      // } else if (nodeData._type === FlattenNode.name) {
      //   node = FlattenNode.parse(nodeData as IFlattenNode);
      // } else if (nodeData._type === BatchNormNode.name) {
      //   node = BatchNormNode.parse(nodeData as IBatchNormNode);
      // } else if (nodeData._type === PoolingNode.name) {
      //   node = PoolingNode.parse(nodeData as IPoolingNode);
      // } else {
      //   node = new Presets.classic.Node();
      // }
      // node.id = nodeData.id;
      // parseNode(nodeData);
      await editor.value?.addNode(node);
    }

    for (const connectionData of graph.connections) {
      const sourceNode = editor.value!.getNode(connectionData.source);
      const sourceOutput = connectionData.sourceOutput;

      const targetNode = editor.value?.getNode(connectionData.target);
      const targetInput = connectionData.targetInput;

      // @ts-ignore
      const connection = new Connection(sourceNode, sourceOutput, targetNode, targetInput);
      await editor.value?.addConnection(connection);
    }

    for (const position of graph.positions) {
      await area.value?.translate(position.id, { x: position.x, y: position.y });
    }

    // await arrangeLayout();
    await zoomAt();

    loading.value = false;
  };

  const clear = async () => {
    await editor.value?.clear();
    await zoomAt();
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
    destroy: () => area.value?.destroy()
  };
}
