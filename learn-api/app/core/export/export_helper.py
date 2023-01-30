from io import BytesIO
from typing import Type, Tuple

import xlsxwriter
from pydantic import BaseModel
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet


class ExportHelper:
    @staticmethod
    def write_xlsx_header(worksheet: Worksheet, model: Type[BaseModel]) -> None:
        """
        Writes all fields in the given model to the worksheet first row

        :param worksheet: Worksheet to write to
        :param model: Model which field represent the column names
        """
        char = "A"
        for index, field in enumerate(model.__fields__):
            col = chr(ord(char[0]) + index) + "1"
            worksheet.write(col, field)

    @staticmethod
    def initialize_xlsx_file() -> Tuple[Workbook, Worksheet, BytesIO]:
        """
        Initializes a xlsx workbook, worksheet and Bytes Buffer
        :return: Initialized workbook, worksheet and bytes buffer
        """
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        return workbook, worksheet, output
