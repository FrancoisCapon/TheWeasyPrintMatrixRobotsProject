import logging
import weasyprint

from weasyprintmatrixrobots.robot_ import Robot

class Printer(Robot):

    def __init__(self,matrix):
        super().__init__(matrix)
        
    def do_job(self):
        logging.basicConfig(
            level=logging.WARNING,
            format="[%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(f'{self.matrix.path_print_weasyprint_inout}weasyprint.log')]
        )
        print(self.matrix.path_print_weasyprint_inout)
        weasyprint_object = weasyprint.HTML(self.matrix.path_print_weasyprint_inout + 'weasyprint.html')
        weasyprint_object.write_pdf(
            self.matrix.path_print + 'print.pdf',
            stylesheets=[self.matrix.path_print_weasyprint_inout + 'weasyprint.css'],
            # https://doc.courtbouillon.org/weasyprint/latest/api_reference.html#html
            # HTML presentational hints are not supported by default, but most of them can be supported:
            # ...various table alignment attributes
            presentational_hints = True,
            )
