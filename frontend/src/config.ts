export function getEnv(name: string) {
  // @ts-ignore
  return window?.configs?.[name] || import.meta.env['VITE_' + name];
}

const SLIDE_API_URL = getEnv('SLIDE_API_URL');
const BASE_API_URL = getEnv('BASE_API_URL');
const AI_API_URL = getEnv('AI_API_URL');
const SLIDE_IMAGE_URL = getEnv('SLIDE_IMAGE_URL');
const APP_LOGO_URL = getEnv('APP_LOGO_URL');
const SLIDE_URL = `${SLIDE_IMAGE_URL}/pyramids`;

const getSlideUrl = (slide_id: string) => {
  return `${SLIDE_URL}/${slide_id}/dzi.dzi`;
};

const getThumbnailUrl = (slide_id: string) => {
  return `${SLIDE_URL}/${slide_id}/thumbnail.jpeg`;
};

const getInfoImageUrl = (image_id: string) => {
  return `${SLIDE_IMAGE_URL}/info-images/${image_id}.jpeg`;
};

export {
  BASE_API_URL,
  SLIDE_API_URL,
  AI_API_URL,
  SLIDE_IMAGE_URL,
  SLIDE_URL,
  getSlideUrl,
  getThumbnailUrl,
  getInfoImageUrl,
  APP_LOGO_URL
};
