export enum SLIDE_STATUS {
  ERROR = 0,
  SUCCESS = 1,
  RUNNING = 2
}

type SlideStatus = {
  [key in SLIDE_STATUS]: string;
};

export const SLIDE_STATUS_STRING: SlideStatus = {
  [SLIDE_STATUS.ERROR]: 'Error',
  [SLIDE_STATUS.SUCCESS]: 'Complete',
  [SLIDE_STATUS.RUNNING]: 'Running'
};
