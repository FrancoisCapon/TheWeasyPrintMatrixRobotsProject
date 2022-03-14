import shutil
import os
import sqlite3

from weasyprintmatrixrobots.robot_ import Robot

class Writer(Robot):

    def __init__(self,matrix):
       super().__init__(matrix)

    def do_job(self):
        # clean print directory
        shutil.rmtree(self.matrix.path_print, ignore_errors = True)
        os.mkdir(self.matrix.path_print)
        # html
        with open(f'{self.matrix.path_print}weasyprint.html', 'w',  encoding='utf8') as file:
            file.write(self.matrix.html)
        file.close()
        # scss
        with open(f'{self.matrix.path_print}print.scss', 'w',  encoding='utf8') as file:
            file.write(self.matrix.scss_main)
        file.close()
        for scss_number, scss_content in self.matrix.scss_prints:
            with open(f'{self.matrix.path_print}print{scss_number}.scss', 'w',  encoding='utf8') as file:
                file.write(scss_content)
            file.close()
        os.system(f'sass --no-source-map {self.matrix.path_print}print.scss:{self.matrix.path_print}weasyprint.css')
        # matrix html
        with open(f'{self.matrix.path_print}matrix.html', 'w',  encoding='utf8') as file:
            file.write(self.matrix.html_matrix)
        file.close()
        # matrix sqlite
        sqlite3_connection_file = sqlite3.connect(f'{self.matrix.path_print}matrix.db3')
        self.matrix.sqlite3_connection.backup(sqlite3_connection_file)