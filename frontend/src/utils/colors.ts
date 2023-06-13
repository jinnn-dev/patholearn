export function getTextColor(hex: string): string {
  // Remove the "#" symbol if present
  hex = hex.replace('#', '');

  // Convert the hex value to RGB
  const r = parseInt(hex.substring(0, 2), 16) / 255;
  const g = parseInt(hex.substring(2, 4), 16) / 255;
  const b = parseInt(hex.substring(4, 6), 16) / 255;

  // Calculate relative luminance
  const luminance =
    0.2126 * getRGBComponentLuminance(r) + 0.7152 * getRGBComponentLuminance(g) + 0.0722 * getRGBComponentLuminance(b);

  // Choose the text color based on the luminance value
  return luminance > 0.5 ? 'black' : 'white';
}

function getRGBComponentLuminance(component: number): number {
  return component <= 0.03928 ? component / 12.92 : Math.pow((component + 0.055) / 1.055, 2.4);
}
