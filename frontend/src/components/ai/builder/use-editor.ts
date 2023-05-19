import { NodeEditor, GetSchemes, ClassicPreset } from 'rete';
import { AreaPlugin, AreaExtensions } from 'rete-area-plugin';
import { ConnectionPlugin, Presets as ConnectionPresets } from 'rete-connection-plugin';
import { VueRenderPlugin, Presets, VueArea2D } from 'rete-vue-render-plugin';
import { AutoArrangePlugin, Presets as ArrangePresets, ArrangeAppliers } from 'rete-auto-arrange-plugin';

import CustomNodeVue from './CustomNode.vue';
import CustomConnectionVue from './CustomConnection.vue';
import CustomSocketVue from './CustomSocket.vue';
import { DatasetNode } from './components/dataset-node';
import { DropdownControl } from './components/dataset/dropdown-control';
import CustomDropdownVue from './components/dataset/CustomDropdown.vue';
import { Conv2DNode } from './components/conv2d-node';
import { NumberControl } from './components/number-control/number-control';
import NumberControlVue from './components/number-control/NumberControl.vue';
import { Ref, ref } from 'vue';

// type Schemes = GetSchemes<
//   ClassicPreset.Node,
//   ClassicPreset.Connection<ClassicPreset.Node, ClassicPreset.Node> | ClassicPreset.Connection<DatasetNode, Conv2DNode>
// >;

type NodeProps = DatasetNode | Conv2DNode;

class Connection<A extends NodeProps, B extends NodeProps> extends ClassicPreset.Connection<A, B> {}

type ConnProps = Connection<DatasetNode, Conv2DNode> | Connection<Conv2DNode, Conv2DNode>;
type Schemes = GetSchemes<NodeProps, ConnProps>;

type AreaExtra = VueArea2D<Schemes>;

export function useEditor() {
  const socket: Ref<ClassicPreset.Socket | undefined> = ref();
  const area: Ref<AreaPlugin<Schemes, AreaExtra> | undefined> = ref();
  const connection: Ref<ConnectionPlugin<Schemes, AreaExtra> | undefined> = ref();
  const render: Ref<VueRenderPlugin<Schemes> | undefined> = ref();
  const editor: Ref<NodeEditor<Schemes> | undefined> = ref();

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

    arrange.value = new AutoArrangePlugin<Schemes>();

    animationApplier.value = new ArrangeAppliers.TransitionApplier<Schemes, never>({
      duration: 300,
      timingFunction: (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2)
    });

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
          if (data.payload instanceof ClassicPreset.InputControl) {
            return Presets.classic.Control;
          }
        }
      }
    });

    // @ts-ignore
    render.value.addPreset(presets);

    connection.value.addPreset(ConnectionPresets.classic.setup());
    arrange.value.addPreset(ArrangePresets.classic.setup());

    editor.value.use(area.value);
    area.value.use(connection.value);
    area.value.use(render.value);
    area.value.use(arrange.value);

    AreaExtensions.simpleNodesOrder(area.value);

    const dataset = new DatasetNode(socket.value);
    await editor.value.addNode(dataset);

    const convLayer = new Conv2DNode(socket.value);
    await editor.value.addNode(convLayer);

    const convLayer2 = new Conv2DNode(socket.value);
    await editor.value.addNode(convLayer2);

    const convLayer3 = new Conv2DNode(socket.value);
    await editor.value.addNode(convLayer3);

    const convLayer4 = new Conv2DNode(socket.value);
    await editor.value.addNode(convLayer4);

    await editor.value.addConnection(new ClassicPreset.Connection(dataset, 'dataset', convLayer, 'in'));
    await editor.value.addConnection(new ClassicPreset.Connection(convLayer, 'out', convLayer2, 'in'));
    await editor.value.addConnection(new ClassicPreset.Connection(convLayer, 'out', convLayer3, 'in'));
    await editor.value.addConnection(new ClassicPreset.Connection(convLayer, 'out', convLayer4, 'in'));

    await arrangeLayout();
    await AreaExtensions.zoomAt(area.value, editor.value.getNodes());
    loading.value = false;
  };

  const arrangeLayout = async () => {
    await arrange.value?.layout({
      applier: animationApplier.value
    });
  };

  const addNode = async () => {
    if (!socket.value || !editor.value) {
      return;
    }
    const layer = new Conv2DNode(socket.value);
    await editor.value.addNode(layer);
  };

  const zoomAt = async () => {
    if (!area.value || !editor.value) {
      return;
    }
    await AreaExtensions.zoomAt(area.value, editor.value.getNodes());
  };

  const download = () => {
    const data: { nodes: any[] } = { nodes: [] };
    const nodes = editor.value?.getNodes();
    for (const node of nodes || []) {
      data.nodes.push({
        id: node.id,
        label: node.label,
        inputs: node.inputs,
        controls: node.controls,
        outputs: node.outputs
      });
    }
    return JSON.stringify(data);
  };

  return { editor, loading, arrangeLayout, zoomAt, download, init, addNode, destroy: () => area.value?.destroy() };
}
