const fs = require('fs');

const rootPath = require('path').resolve(__dirname, '../');
const iconPath = rootPath + '/src/assets/icons';

const directories = fs
  .readdirSync(iconPath, { withFileTypes: true })
  .filter((dirent) => dirent.isDirectory())
  .map((dirent) => dirent.name);

const icons = [];

directories.forEach((dir) => {
  const dirPath = iconPath + '/' + dir;
  fs.readdirSync(dirPath).forEach((file) => {
    const data = fs.readFileSync(dirPath + '/' + file, 'utf-8');

    const regex = new RegExp(`</?(?!(?:svg)\b)[a-z](?:[^>"']|"[^"]*"|'[^']*')*>`);
    const path = data
      .replace(regex, '')
      .replace('</svg>', '')
      .replace(/stroke="#(.)*?"/g, 'stroke="current"')
      .replace(/fill="#(.)*?"/g, 'fill="current"')
      .replace(/stroke-width="(.)*?"/g, '');

    const icon = {
      style: dir,
      name: file.split('.')[0],
      path: path
    };
    icons.push(icon);
  });
});

let iconsString = '';

let typeNames = [];
icons.forEach((icon) => {
  const escapedName = icon.name.replace(/-|\./g, '');

  const iconString = `export const ${escapedName}: Icon = {style: '${icon.style}', name: '${icon.name}', path: '${icon.path}'}\n`;
  iconsString += iconString;
  typeNames.push(icon.name);
});

const iconInterface = 'export interface Icon {\n\tstyle: string;\n\tname: string;\n\tpath: string;\n}\n';

const typeString = 'export type IconNames = ' + "'" + typeNames.join("' | '") + "'";

const resultString = iconInterface + '\n' + iconsString + '\n' + typeString;
fs.writeFileSync(rootPath + '/icons.ts', resultString);
// fs.writeFileSync(rootPath + '/icons.ts', typeString);
