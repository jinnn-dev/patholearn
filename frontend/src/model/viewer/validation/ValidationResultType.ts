import { IconNames } from '../../../../icons';

export enum ValidationResultType {
  MISSING_NAME,
  INVALID_GEOMETRY
}

type ValidationResultStringRepresentation = {
  [key in ValidationResultType]: string;
};

export const VALIDATION_RESULT: ValidationResultStringRepresentation = {
  [ValidationResultType.MISSING_NAME]: 'Klasse fehlt',
  [ValidationResultType.INVALID_GEOMETRY]: 'Geometrie ist invalide'
};

type ValidationResultIcon = {
  [key in ValidationResultType]: IconNames;
};

export const VALIDATION_RESULT_ICON: ValidationResultIcon = {
  [ValidationResultType.MISSING_NAME]: 'tag',
  [ValidationResultType.INVALID_GEOMETRY]: 'polygon-segments'
};
