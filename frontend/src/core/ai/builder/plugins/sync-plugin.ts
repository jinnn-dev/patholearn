import { BaseSchemes, Root, Scope, ClassicPreset } from 'rete';
import { Area2D } from 'rete-area-plugin';
import { Connection } from 'rete-connection-plugin';

export class SyncPlugin<Schemes extends BaseSchemes> {
  root = new Scope<never, [Root<Schemes>]>('readonly');
  area = new Scope<never, [Area2D<Schemes>, Root<Schemes>]>('readonly');
  connection = new Scope<never, [Connection, Root<Schemes>]>('readonly');

  enabled = false;

  constructor() {
    this.root.addPipe((context) => {
      // console.log(context);

      return context;
    });
    this.area.addPipe((context) => {
      return context;
    });
    this.connection.addPipe((context) => {
      return context;
    });
  }
}
