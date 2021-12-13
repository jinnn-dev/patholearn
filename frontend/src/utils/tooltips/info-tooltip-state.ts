import { reactive } from 'vue';

export const infotooltipState = reactive<{
  id: string;
  show: boolean;
  x: number;
  y: number;
  headerText: string;
  detailText: string;
  images?: string[];
}>({
  id: '',
  show: false,
  x: 100,
  y: 100,
  headerText: '',
  detailText: ''
});
