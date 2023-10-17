import os
from datetime import date

from App.ExcelHandler import get_order_number
from Database.Database import Path, session


def generate_path_list(excel_file):
    clear_dir_list = []
    path_list = []
    for row in excel_file.iter_rows():
        row_data = []
        for cell in row:
            row_data.append(cell.value)
        row_data.pop(0)
        for value in row_data:
            if value is not None and len(value) > 0:
                clear_dir_list.append(value)

        directory_path = '/'.join(clear_dir_list)
        path_list.append(directory_path)
        clear_dir_list = []
    path_list.pop(0)
    path_list.pop()
    return path_list
    # print(path_list)


def folder_generator(excel_file, selected_path, path_list):
    cleared_path_list = []
    year = date.today().year
    order_nr = get_order_number(excel_file)
    for path in path_list:
        try:
            os.makedirs(f"{selected_path}/{year}/{order_nr}/VD/{path}")
            # print('Directory', path, ' created')
        except FileExistsError:
            pass
            # print('Directory', path, ' already exists')
        if path not in cleared_path_list:
            cleared_path_list.append(path)

    return cleared_path_list


def save_path_to_db(path_list):
    for p in range(len(path_list)):
        new_path = Path(path=path_list[p])
        query_path = session.query(Path).filter(Path.path == new_path.path).first()

        if query_path is not None:
            pass
        else:
            session.add(new_path)
            session.commit()
    session.close()
