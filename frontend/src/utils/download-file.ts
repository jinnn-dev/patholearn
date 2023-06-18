export function downloadFile(data: any, title: string) {
  const url = window.URL.createObjectURL(new Blob([data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', title);
  document.body.appendChild(link);
  link.click();
}
