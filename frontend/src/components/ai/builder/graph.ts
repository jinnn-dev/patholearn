import { IGraph, INode } from './serializable';

export const DEFAULT_GRAPH: IGraph = {
  nodes: [
    {
      id: '96df2779b6938ca8',
      _type: 'DatasetNode',
      label: 'Input',
      inputs: [],
      outputs: [
        {
          _type: 'ClassicPreset.Output',
          key: 'dataset',
          id: 'fedb9bcb178cdd9b',
          label: 'Dataset',
          socket: {
            name: 'socket'
          }
        }
      ],
      controls: [
        {
          key: 'dataset',
          value: 'MNIST',
          _type: 'DropdownControl',
          id: '440ec63c9bd5cdd3',
          values: ['MNIST', 'BHI'],
          label: 'Dataset'
        }
      ],
      socket: 'socket'
    },
    {
      id: 'b3a317bab8c22739',
      _type: 'Conv2DNode',
      label: 'Conv2D',
      inputs: [
        {
          _type: 'ClassicPreset.Input',
          key: 'in',
          id: '7025466bae4d2e5a',
          label: 'in',
          socket: {
            name: 'socket'
          }
        }
      ],
      outputs: [
        {
          _type: 'ClassicPreset.Output',
          key: 'out',
          id: 'a2c6a5e7f78ce4cc',
          label: 'out',
          socket: {
            name: 'socket'
          }
        }
      ],
      controls: [
        {
          _type: 'InputControl2',
          id: '2aa8dd06471cac55',
          key: 'filters',
          type: 'number',
          value: 1234
        },
        {
          _type: 'InputControl2',
          id: '33ef5be0a522f6c4',
          key: 'kernel',
          type: 'number',
          value: 124234
        },
        {
          _type: 'InputControl2',
          id: 'dfd7ce44cea4aee3',
          key: 'stride',
          type: 'number',
          value: 12344
        }
      ],
      socket: 'socket'
    },
    {
      id: 'faa81db565af4ee9',
      _type: 'Conv2DNode',
      label: 'Conv2D',
      inputs: [
        {
          _type: 'ClassicPreset.Input',
          key: 'in',
          id: '1f9df164720ebc70',
          label: 'in',
          socket: {
            name: 'socket'
          }
        }
      ],
      outputs: [
        {
          _type: 'ClassicPreset.Output',
          key: 'out',
          id: '71cf00655cc857ea',
          label: 'out',
          socket: {
            name: 'socket'
          }
        }
      ],
      controls: [
        {
          _type: 'InputControl2',
          id: '9ba0699d7453a125',
          key: 'filters',
          type: 'number',
          value: 1234
        },
        {
          _type: 'InputControl2',
          id: '62013f07fb7af393',
          key: 'kernel',
          type: 'number',
          value: 1234
        },
        {
          _type: 'InputControl2',
          id: 'd8bb3e01e3c0cf26',
          key: 'stride',
          type: 'number',
          value: 1234
        }
      ],
      socket: 'socket'
    },
    {
      id: '9f7c7614ca83069c',
      _type: 'Conv2DNode',
      label: 'Conv2D',
      inputs: [
        {
          _type: 'ClassicPreset.Input',
          key: 'in',
          id: '301b7d21158be288',
          label: 'in',
          socket: {
            name: 'socket'
          }
        }
      ],
      outputs: [
        {
          _type: 'ClassicPreset.Output',
          key: 'out',
          id: '56ecae5bc062619b',
          label: 'out',
          socket: {
            name: 'socket'
          }
        }
      ],
      controls: [
        {
          _type: 'InputControl2',
          id: '667513a563eac0be',
          key: 'filters',
          type: 'number',
          value: 1234
        },
        {
          _type: 'InputControl2',
          id: '3fac4c419725b1af',
          key: 'kernel',
          type: 'number',
          value: 1234
        },
        {
          _type: 'InputControl2',
          id: 'd4f5bc6df2ebe778',
          key: 'stride',
          type: 'number',
          value: 1234
        }
      ],
      socket: 'socket'
    },
    {
      id: '201be3c86bcb6279',
      _type: 'Conv2DNode',
      label: 'Conv2D',
      inputs: [
        {
          _type: 'ClassicPreset.Input',
          key: 'in',
          id: 'd77ef9be30b99458',
          label: 'in',
          socket: {
            name: 'socket'
          }
        }
      ],
      outputs: [
        {
          _type: 'ClassicPreset.Output',
          key: 'out',
          id: '4215f6ac86a5fed8',
          label: 'out',
          socket: {
            name: 'socket'
          }
        }
      ],
      controls: [
        {
          _type: 'InputControl2',
          id: '84d4ff84bd4acc3c',
          key: 'filters',
          type: 'number',
          value: 1234
        },
        {
          _type: 'InputControl2',
          id: 'b7e8299265d03ee3',
          key: 'kernel',
          type: 'number',
          value: 1234
        },
        {
          _type: 'InputControl2',
          id: 'd19488fae1337c13',
          key: 'stride',
          type: 'number',
          value: 1234
        }
      ],
      socket: 'socket'
    }
  ],
  connections: [
    {
      id: 'aaf553eebda9e0ad',
      source: '96df2779b6938ca8',
      sourceOutput: 'dataset',
      target: 'b3a317bab8c22739',
      targetInput: 'in'
    },
    {
      id: 'd8f8678d3a173571',
      source: 'b3a317bab8c22739',
      sourceOutput: 'out',
      target: 'faa81db565af4ee9',
      targetInput: 'in'
    },
    {
      id: '9ad7ca504c65892c',
      source: 'b3a317bab8c22739',
      sourceOutput: 'out',
      target: '9f7c7614ca83069c',
      targetInput: 'in'
    },
    {
      id: '48e1a0aab3026ec0',
      source: 'b3a317bab8c22739',
      sourceOutput: 'out',
      target: '201be3c86bcb6279',
      targetInput: 'in'
    }
  ]
};
