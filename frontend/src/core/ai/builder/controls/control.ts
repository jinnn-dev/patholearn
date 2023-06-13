import { ClassicPreset } from 'rete';
import { ISerializable, Serializable } from '../serializable';
import { LockStatus } from '../sync';
import { ControlType } from './types';

export abstract class Control<S extends ISerializable>
  extends ClassicPreset.Control
  implements Serializable<S extends ISerializable ? any : any>
{
  public type: ControlType
  constructor(type: ControlType, public lockStatus?: LockStatus) {
    super();
    this.type = type;
  }
  public abstract serialize(key?: string | undefined): S extends ISerializable ? any : any;
  public abstract setValue(...args: any): void;
  public static parse<T>(nodeData: T extends ISerializable ? any : any) {}
  public abstract duplicate<T>(): Control<T extends ISerializable ? any : any>;
}
