export interface User {
  id: number;
  email: string;
  firstname: string;
  middlename?: string;
  lastname: string;
  is_active: boolean;
  is_superuser: boolean;
}
