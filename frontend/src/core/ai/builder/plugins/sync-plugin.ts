import { BaseSchemes, Root, Scope, ClassicPreset } from 'rete';
import { Area2D } from 'rete-area-plugin';
import { Connection } from 'rete-connection-plugin';
import { builderState } from '../state';
export class SyncPlugin<Schemes extends BaseSchemes> {
  root = new Scope<never, [Root<Schemes>]>('readonly');
  area = new Scope<never, [Area2D<Schemes>, Root<Schemes>]>('readonly');
  connection = new Scope<never, [Connection, Root<Schemes>]>('readonly');

  enabled = false;

  constructor() {
    this.root.addPipe((context) => {
      if (
        builderState.builderLoaded &&
        builderState.initialGraphLoaded &&
        (context.type === 'nodecreated' ||
          context.type === 'noderemoved' ||
          context.type === 'connectioncreated' ||
          context.type === 'connectionremoved')
      ) {
        builderState.shouldSaveEditor = true;
      }
      return context;
    });
    this.area.addPipe((context) => {
      if (context.type === 'pointermove') {
      }

      if (builderState.builderLoaded && builderState.initialGraphLoaded && context.type === 'nodedragged') {
        builderState.shouldSaveEditor = true;
      }
      return context;
    });
    this.connection.addPipe((context) => {
      return context;
    });
  }
}
