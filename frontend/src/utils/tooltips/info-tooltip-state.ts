import { reactive } from 'vue';

export const infotooltipState = reactive<{
  id: string;
  show: boolean;
  x: number;
  y: number;
  headerText: string;
  detailText: string;
  animate: boolean;
  images?: string[];
}>({
  id: '',
  show: false,
  x: 100,
  y: 100,
  headerText: '',
  detailText: '',
  animate: false
});

export const resetInfoTooltipState = () => {
  infotooltipState.id = '';
  infotooltipState.show = false;
  infotooltipState.x = 100;
  infotooltipState.y = 100;
  infotooltipState.headerText = '';
  infotooltipState.detailText = '';
  infotooltipState.animate = false;
};
