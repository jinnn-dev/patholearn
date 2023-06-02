import { PortData, Preset } from 'rete-auto-arrange-plugin/_types/presets';

export const arrangeSetup = (props?: {
  spacing?: number;
  top?: number;
  bottom?: number;
  distance?: number;
}): Preset => {
  return () => ({
    port(data): PortData {
      const { spacing, top, bottom, distance } = {
        spacing: props && typeof props.spacing !== 'undefined' ? props.spacing : 35,
        top: props && typeof props.top !== 'undefined' ? props.top : 35,
        bottom: props && typeof props.bottom !== 'undefined' ? props.bottom : 15,
        distance: props && typeof props.distance !== 'undefined' ? props.distance : 15
      };

      if (data.side === 'output') {
        return {
          x: data.index * spacing,
          y: 0,
          width: distance,
          height: 15,
          side: 'EAST'
        };
      }
      return {
        x: data.index * spacing,
        y: 0,
        width: distance,
        height: 15,
        side: 'WEST'
      };
    }
  });
};
