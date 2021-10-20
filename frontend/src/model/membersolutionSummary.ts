// class SummaryUser(BaseModel):
//     firstname: Optional[str]
//     middlename: Optional[str]
//     lastname: Optional[str]

// class SummaryRow(BaseModel):
//     user: Optional[SummaryUser]
//     summary: Optional[List[int]]

// class MembersolutionSummary(BaseModel):
//     tasks: Optional[List[str]]
//     rows: Optional[List[SummaryRow]]

export interface SummaryUser {
  firstname: string;
  middlename: string;
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
