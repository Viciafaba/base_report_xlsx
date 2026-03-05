import io
import base64
import xlsxwriter
from odoo import models, api

class XlsxHelper(models.AbstractModel):
    _name = 'export.xlsx.helper'
    _description = 'Uniwersalny pomocnik do eksportu XLSX'

    @api.model
    def generate_xlsx(self, headers, data_rows, sheet_name='Dane'):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet(sheet_name)

        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        text_format = workbook.add_format({'num_format': '@'}) 
        default_format = workbook.add_format({})

        for col_num, header in enumerate(headers):
            sheet.write(0, col_num, header, header_format)

        for row_num, row_data in enumerate(data_rows, start=1):
            for col_num, cell_value in enumerate(row_data):
                if isinstance(cell_value, str) and cell_value.isdigit() and len(cell_value) > 7:
                    sheet.write(row_num, col_num, cell_value, text_format)
                else:
                    sheet.write(row_num, col_num, cell_value, default_format)

        workbook.close()
        output.seek(0)
        return base64.b64encode(output.read())