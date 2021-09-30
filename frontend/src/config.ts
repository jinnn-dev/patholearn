const SLIDE_API_URL = import.meta.env.VITE_SLIDE_API_URL;
const BASE_API_URL = import.meta.env.VITE_BASE_API_URL;
const SLIDE_IMAGE_URL = import.meta.env.VITE_SLIDE_IMAGE_URL;
const SLIDE_URL = `${SLIDE_IMAGE_URL}/pyramids`;

const getSlideUrl = (slide_id: string) => {
  return `${SLIDE_URL}/${slide_id}/dzi.dzi`;
};

const getThumbnailUrl = (slide_id: string) => {
  return `${SLIDE_URL}/${slide_id}/thumbnail.jpeg`;
};

export { BASE_API_URL, SLIDE_API_URL, SLIDE_IMAGE_URL, SLIDE_URL, getSlideUrl, getThumbnailUrl };
