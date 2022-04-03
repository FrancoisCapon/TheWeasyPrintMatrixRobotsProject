import os
import glob
import sqlite3
import pkgutil

class Matrix:

    def __init__(self,path_root):
        self.glob_pattern_columns = '[0-9][0-9]-*' + os.sep
        self.glob_pattern_rows = '[0-9][0-9][0-9][0-9]-*' + os.sep
        self.cells_files = [('content.html', 'html'), ('print.scss', 'scss'), ('meta.html', 'meta')]
        self.path_root = os.path.abspath(path_root) + os.sep
        self.path_print = self.path_root +  'print' +  os.sep
        self.path_print_matrix_out = self.path_print + 'matrix' + os.sep
        self.path_print_weasyprint_inout = self.path_print + 'weasyprint' + os.sep
        self.path_print_scss_in = self.path_print + 'scss' + os.sep

        # https://docs.python.org/3.4/library/sqlite3.html#connection-objects
        #self.sqlite3_cursor = sqlite3.connect("file::memory:", isolation_level=None).cursor() # autocommit
        self.sqlite3_connection = sqlite3.connect("file::memory:")
        self.sqlite3_cursor = self.sqlite3_connection.cursor()
        self.sqlite3_cursor.execute("CREATE TABLE cell (id PRIMARY KEY, number_row INTEGER, segment_row TEXT, number_column INTEGER, segment_column TEXT, html INTEGER, scss INTEGER, meta INTEGER)")
        
    def build_html_page(self):
        self.html_matrix = pkgutil.get_data(__name__, 'template-matrix.html').decode('utf-8')
        self.html_matrix = self.html_matrix.replace('<!-- TABLE -->', self.build_html_table_rows())

    def build_html_table_rows(self):
        # header
        html_table_rows = '<tr><th></th>'
        self.sqlite3_cursor.execute("SELECT DISTINCT number_column, segment_column FROM cell ORDER BY number_column")
        columns = self.sqlite3_cursor.fetchall()
        for column in columns:
            html_table_rows += f'<th data-column-id={column[0]}>{column[1]}</th>'
        html_table_rows += '</tr>'
        # rows
        html_cell_content = {
            # html
            2: { None: '', 0: '<span>HTML</span>', 1: '<del>HTML</del>', 2: '<ins>HTML</ins>'},
            # scss
            3: { None: '', 0: '<span>SCSS</span>', 1: '<del>SCSS</del>', 2: '<ins>SCSS</ins>'},
            # meta
            4: { None: '', 0: '<span>META</span>', 1: '<del>META</del>', 2: '<ins>META</ins>'},
        }
        sql_select = """
        SELECT rc.number_row, rc.number_column, html, scss, meta, segment_row FROM 
        (
        SELECT * FROM
            (SELECT DISTINCT number_row FROM cell) as row,
            (SELECT DISTINCT number_column FROM cell) as column 
        ORDER BY number_row, number_column
        ) as rc 
        LEFT JOIN cell 
        ON rc.number_row = cell.number_row 
        AND rc.number_column = cell.number_column
        """
        self.sqlite3_cursor.execute(sql_select)
        cells = self.sqlite3_cursor.fetchall()
        number_row_current = -1
        for cell in cells:
            if number_row_current != cell[0]: # new row
                if number_row_current != -1:
                    html_table_rows += '</tr>'
                number_row_current = cell[0]
                html_table_rows += f'<tr><th data-row-id="{number_row_current}">{number_row_current}</th>'
            # cell
            if cell[5] != None:
                html_data_title = f'data-title="{cell[5]}"'
            else:
                html_data_title = ''
            html_cell = f'<td data-row-id="{number_row_current}" data-column-id="{cell[1]}" {html_data_title}>'
            for i in [2,3,4]:
                html_cell += html_cell_content[i][cell[i]]
            html_cell + '</td>'
            html_table_rows += html_cell

        return html_table_rows + '</tr>'

    def get_cells_winner_files(self, cell_file, which_files ='last_of_each_row'):
        sql_select = f"SELECT * FROM cell WHERE {cell_file[1]} = 1 "
        if which_files == 'last_of_each_row':
            sql_select += f"""
                AND id IN 
                (
                SELECT number_row + MAX(number_column)/100.0
                FROM CELL
                WHERE {cell_file[1]} = 1
                GROUP BY number_row
                )
                ORDER BY id
            """
        elif which_files == 'last_of_matrix':
            sql_select += "ORDER BY id DESC LIMIT 1"
        cells = self.sqlite3_cursor.execute(sql_select).fetchall()
        winners = []
        for cell in cells:
            winners.append((self.path_root + cell[4] + os.sep + cell[2] + os.sep + cell_file[0], cell))
            self.sqlite3_cursor.execute(f"UPDATE cell SET {cell_file[1]} = 2 WHERE id = {cell[0]}")
        self.sqlite3_connection.commit()
        return winners