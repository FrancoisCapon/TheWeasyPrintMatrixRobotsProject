import os

def parse_path_cell(path_cell):
    segments = path_cell.split(os.sep)
    segment_row = segments[-2] # lmm/ => 'lmm', ''
    number_row = segment_row[0:4] # 9999-...
    segment_column = segments[-3] # lmm/ => 'lmm', ''
    number_column = segment_column[0:2] # 99-...
    id = int(number_row) + int(number_column) / 100.0
    return id, number_row, segment_row, number_column, segment_column