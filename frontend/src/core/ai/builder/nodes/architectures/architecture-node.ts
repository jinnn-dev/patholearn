import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { Socket } from '../../sockets/socket';
import { Node, InputsMap, OutputsMap } from '../node';
import { Control } from '../../controls/control';

export abstract class ArchitectureNode<
  T extends INode,
  Inputs extends InputsMap = InputsMap,
  Outputs extends OutputsMap = OutputsMap,
  Controls extends { [key in string]?: Control<any> } = { [key in string]?: Control<any> }
> extends Node<T, Inputs, Outputs, Controls> {}
