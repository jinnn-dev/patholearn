export interface SummaryUser {
  firstname: string;
  lastname: string;
}

export interface SummaryRow {
  user: SummaryUser;
  summary: number[];
}

export interface MembersolutionSummary {
  tasks: string[];
  rows: SummaryRow[];
}
