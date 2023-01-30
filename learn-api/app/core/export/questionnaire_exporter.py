from typing import Type, Optional, List

from pydantic import BaseModel
from sqlalchemy.orm import Session
from xlsxwriter.worksheet import Worksheet

from app.core.export.export_helper import ExportHelper
from app.schemas.questionnaire import Questionnaire


class QuestionnaireRow(BaseModel):
    question_text: str
    firstname: str
    middlename: str
    lastname: str
    selection: str
    answer: Optional[str]


class QuestionnaireExporter:
    @staticmethod
    def export_questionnaire_answers(db: Session, answers: List[QuestionnaireRow]):
        workbook, worksheet, output = ExportHelper.initialize_xlsx_file()
        ExportHelper.write_xlsx_header(worksheet, QuestionnaireRow)

        start_row = 2
        char = "A"
        for row in answers:
            for col_index, item in enumerate(QuestionnaireRow.__fields__):
                json_row = row.dict()
                worksheet.write(
                    chr(ord(char[0]) + col_index) + str(start_row), json_row[item]
                )
            start_row += 1

        workbook.close()
        output.seek(0)
        return output
