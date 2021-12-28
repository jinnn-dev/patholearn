import { Tool } from './tool';
export class DrawingTool extends Tool {
  constructor(readonly component: string, readonly hint: string, readonly subTools = []) {
    super(component, hint, subTools);
  }
}
