export function formatBytes(bytes: number, base: 1000 | 1024 = 1000, decimals = 2) {
  if (!+bytes) return '0 Bytes';

  const k = base;
  const dm = decimals < 0 ? 0 : decimals;
  const roundedSizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  const correctSizes = ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${base === 1000 ? roundedSizes[i] : correctSizes[i]}`;
}
