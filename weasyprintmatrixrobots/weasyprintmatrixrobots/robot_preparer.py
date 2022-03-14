import os

from weasyprintmatrixrobots.robot_ import Robot

class Preparer(Robot):

    def __init__(self,matrix):
        super().__init__(matrix)

    def do_job(self):
        self.prepare_meta()
        self.prepare_html()
        self.prepare_scss()
        self.matrix.build_html_page()

    def prepare_scss(self):
        winners = self.matrix.get_cells_winner_files(self.matrix.cells_files[1])
        self.matrix.scss_main = ''
        self.matrix.scss_prints = []
        for filename, cell in winners :
            scss_comment = f'\n/* {filename} */\n'
            number_row = cell[1]
            with open(filename, encoding='utf8') as file:
                scss_content_cell = file.read()
                # absolute path for url with single quote url='' TO IMPROVE
                path_cell = os.path.dirname(filename) + os.sep
                scss_content_cell = scss_content_cell.replace("url('", "url('" + path_cell)
            file.close
            self.matrix.scss_prints.append((number_row, scss_comment + scss_content_cell))
            self.matrix.scss_main += scss_comment
            self.matrix.scss_main += f'@use "print{number_row}.scss";\n'

    def prepare_meta(self):
        filename, _ = self.matrix.get_cells_winner_files(self.matrix.cells_files[2], 'last_of_matix')[0]
        with open(filename, encoding='utf8') as file:
                self.matrix.html_meta = file.read()
        file.close()

    def prepare_html(self):
        winners = self.matrix.get_cells_winner_files(self.matrix.cells_files[0])
        html_content = ''
        for filename, _ in winners:
            html_content += f'\n\n<!-- {filename} -->\n\n'
            with open(filename, encoding='utf8') as file:
                html_content_cell = file.read()
                # absolute path for image with single quote src='' TO IMPROVE
                path_cell = os.path.dirname(filename) + os.sep
                html_content_cell = html_content_cell.replace("src='", "src='" + path_cell)
                html_content += html_content_cell
            file.close
        self.matrix.html = f'<html><head><meta charset="utf-8">\n\n{self.matrix.html_meta}\n\n</head><body>{html_content}\n\n</body></html>'
