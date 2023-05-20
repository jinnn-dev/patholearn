import { NodeEditor, GetSchemes, ClassicPreset } from 'rete';
import { AreaPlugin, AreaExtensions } from 'rete-area-plugin';
import { ConnectionPlugin, Presets as ConnectionPresets } from 'rete-connection-plugin';
import { VueRenderPlugin, Presets, VueArea2D } from 'rete-vue-render-plugin';
import { AutoArrangePlugin, Presets as ArrangePresets, ArrangeAppliers } from 'rete-auto-arrange-plugin';

import CustomNodeVue from './CustomNode.vue';
import CustomConnectionVue from './CustomConnection.vue';
import CustomSocketVue from './CustomSocket.vue';
import { DatasetNode, IDatasetNode } from './components/dataset-node';
import { DropdownControl } from './components/dataset/dropdown-control';
import CustomDropdownVue from './components/dataset/CustomDropdown.vue';
import { Conv2DNode, IConv2DNode } from './components/conv2d-node';
import { NumberControl } from './components/number-control/number-control';
import NumberControlVue from './components/number-control/NumberControl.vue';
import DimensionControlVue from './components/dimension-control/DimensionControl.vue';
import { Ref, ref } from 'vue';
import { IConnection, IGraph, INode } from './serializable';
import { addCustomBackground } from './custom-background';
import { LayerType } from './components/types';
import { DimensionControl } from './components/dimension-control/dimension-control';
import { ContextMenuExtra, ContextMenuPlugin, Presets as ContextMenuPresets } from 'rete-context-menu-plugin';

// type Schemes = GetSchemes<
//   ClassicPreset.Node,
//   ClassicPreset.Connection<ClassicPreset.Node, ClassicPreset.Node> | ClassicPreset.Connection<DatasetNode, Conv2DNode>
// >;

type NodeProps = DatasetNode | Conv2DNode;

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
    contextMenu.value = new ContextMenuPlugin<Schemes>({
      items: ContextMenuPresets.classic.setup([])
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
            return CustomDropdownVue;
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
    render.value.addPreset(Presets.contextMenu.setup());
    connection.value.addPreset(ConnectionPresets.classic.setup());
    arrange.value.addPreset(ArrangePresets.classic.setup());

    editor.value.use(area.value);
    area.value.use(connection.value);
    area.value.use(render.value);
    area.value.use(arrange.value);
    area.value.use(contextMenu.value);

    AreaExtensions.simpleNodesOrder(area.value);

    const dataset = new DatasetNode(socket.value);
    dataset.addDefault();
    await editor.value.addNode(dataset);

    const convLayer = new Conv2DNode(socket.value);
    convLayer.addDefault();
    await editor.value.addNode(convLayer);

    const convLayer2 = new Conv2DNode(socket.value);
    convLayer2.addDefault();
    await editor.value.addNode(convLayer2);

    const convLayer3 = new Conv2DNode(socket.value);
    convLayer3.addDefault();
    await editor.value.addNode(convLayer3);

    const convLayer4 = new Conv2DNode(socket.value);
    convLayer4.addDefault();
    await editor.value.addNode(convLayer4);

    await editor.value.addConnection(new Connection(dataset, 'dataset', convLayer, 'in'));
    await editor.value.addConnection(new Connection(convLayer, 'out', convLayer2, 'in'));
    await editor.value.addConnection(new Connection(convLayer, 'out', convLayer3, 'in'));
    await editor.value.addConnection(new Connection(convLayer, 'out', convLayer4, 'in'));

    await arrangeLayout();
    await zoomAt();

    loading.value = false;
  };

  const arrangeLayout = async () => {
    await arrange.value?.layout({
      applier: animationApplier.value
    });
  };

  const addNode = async (layerType: LayerType) => {
    if (!socket.value || !editor.value) {
      return;
    }
    let layer;
    if (layerType === 'Conv2D') {
      layer = new Conv2DNode(socket.value);
      layer.addDefault();
    } else {
      layer = new DatasetNode(socket.value);
      layer.addDefault();
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
    const nodes = editor.value?.getNodes();

    for (const node of nodes || []) {
      const serializedNode = node.serialize();
      nodeData.push(serializedNode);
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
      connections: connectionsData
    };

    return graphData;
  };

  const importGraph = async (graph: IGraph) => {
    loading.value = true;
    await editor.value?.clear();

    for (const nodeData of graph.nodes) {
      let node;

      if (nodeData._type === Conv2DNode.name) {
        node = Conv2DNode.parse(nodeData as IConv2DNode);
      } else if (nodeData._type === DatasetNode.name) {
        node = DatasetNode.parse(nodeData as IDatasetNode);
      } else {
        node = new Presets.classic.Node();
      }
      node.id = nodeData.id;

      await editor.value?.addNode(node);
    }

    for (const connectionData of graph.connections) {
      const sourceNode = editor.value!.getNode(connectionData.source);
      const sourceOutput = connectionData.sourceOutput;

      const targetNode = editor.value?.getNode(connectionData.target);
      const targetInput = connectionData.targetInput;

      const connection = new Connection(sourceNode, sourceOutput, targetNode, targetInput);
      await editor.value?.addConnection(connection);
    }
    await arrangeLayout();
    await zoomAt();

    loading.value = false;
  };

  return {
    editor,
    loading,
    arrangeLayout,
    zoomAt,
    download,
    importGraph,
    init,
    addNode,
    destroy: () => area.value?.destroy()
  };
}
