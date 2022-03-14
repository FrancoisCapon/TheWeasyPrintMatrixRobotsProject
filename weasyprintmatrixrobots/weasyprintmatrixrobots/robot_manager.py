from weasyprintmatrixrobots.robot_ import Robot

from weasyprintmatrixrobots.matrix import Matrix

from weasyprintmatrixrobots.robot_retriever import Retriever
from weasyprintmatrixrobots.robot_preparer import Preparer
from weasyprintmatrixrobots.robot_writer import Writer
from weasyprintmatrixrobots.robot_printer import Printer


class Manager(Robot):

    def __init__(self, path_matrix_root):
        super().__init__(Matrix(path_matrix_root))

    def do_job(self):
        Retriever(self.matrix).do_job()
        Preparer(self.matrix).do_job()
        Writer(self.matrix).do_job()
        Printer(self.matrix).do_job()
