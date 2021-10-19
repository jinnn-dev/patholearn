export default function getEnv(name: string) {
  console.log(window?.configs);
  console.log(window?.configs?.[name]);
  return window?.configs?.[name] || import.meta.env['VITE_' + name];
}

const SLIDE_API_URL = getEnv('SLIDE_API_URL');
const BASE_API_URL = getEnv('BASE_API_URL');
const SLIDE_IMAGE_URL = getEnv('SLIDE_IMAGE_URL');
const SLIDE_URL = `${SLIDE_IMAGE_URL}/pyramids`;

const getSlideUrl = (slide_id: string) => {
  return `${SLIDE_URL}/${slide_id}/dzi.dzi`;
};

const getThumbnailUrl = (slide_id: string) => {
  return `${SLIDE_URL}/${slide_id}/thumbnail.jpeg`;
};

export { BASE_API_URL, SLIDE_API_URL, SLIDE_IMAGE_URL, SLIDE_URL, getSlideUrl, getThumbnailUrl };
