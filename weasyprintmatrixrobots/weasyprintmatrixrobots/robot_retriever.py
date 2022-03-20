import glob
import weasyprintmatrixrobots.tools

from weasyprintmatrixrobots.robot_ import Robot

class Retriever(Robot):

    def __init__(self,matrix):
        super().__init__(matrix)

    def do_job(self):
        self.retrieve_cells()
        self.retrieve_cells_files()

    def retrieve_cells_files(self):
        for cells_file in self.matrix.cells_files:
            self.retrieve_cells_file(cells_file)
    
    def retrieve_cells_file(self, file):
        # file = (filenanme, tablecolumn)
        path_cells = glob.glob(self.matrix.path_root + self.matrix.glob_pattern_columns + self.matrix.glob_pattern_rows + file[0])
        for path_cell in path_cells:
            parsed_path_cell = weasyprintmatrixrobots.tools.parse_path_cell(path_cell)
            self.matrix.sqlite3_cursor.execute(f"UPDATE cell SET {file[1]} = 1 WHERE id = {parsed_path_cell[0]}")
        self.matrix.sqlite3_connection.commit()

    def retrieve_cells(self):
        path_cells = glob.glob(self.matrix.path_root + self.matrix.glob_pattern_columns + self.matrix.glob_pattern_rows )
        for path_cell in path_cells:
            parsed_path_cell = weasyprintmatrixrobots.tools.parse_path_cell(path_cell)
            self.matrix.sqlite3_cursor.execute(f"INSERT INTO cell VALUES({parsed_path_cell[0]}, {parsed_path_cell[1]}, '{parsed_path_cell[2]}', {parsed_path_cell[3]}, '{parsed_path_cell[4]}', 0, 0, 0)")
        self.matrix.sqlite3_connection.commit()