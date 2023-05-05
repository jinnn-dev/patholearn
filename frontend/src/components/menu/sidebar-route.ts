import { IconNames } from '../../../icons';

export interface SidebarRoute {
  to: string;
  icon: IconNames;
  label: string;
  children?: SidebarRoute[];
  restricted?: boolean;
}
