import openpyxl


def load_excel_file(file, sheet):
    excel_file = openpyxl.load_workbook(file)
    excel_sheet = excel_file[sheet]
    return excel_sheet


def get_order_number(file):
    s = slice(-15, None)
    order_number = file[s][:-5]
    return order_number


def get_files_from_excel(excel_file):
    files = []
    for cell in excel_file['A']:
        files.append(cell.value)
    files.pop(0)
    files.pop()  # odkontrolovat poslednu polozku
    return files
