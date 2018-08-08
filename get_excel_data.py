import xlrd


class GetExcel:

    def __init__(self, file_path):
        self.xlsfile = file_path
        self.book = self.get_book()

    def get_book(self):
        """获取excel文件的book对象"""
        return xlrd.open_workbook(self.xlsfile)

    def get_sheet(self, index):
        """根据索引获取excel表格的sheet"""
        return self.book.sheet_by_index(index)

    def get_sheet_name(self, index):
        return self.book.sheet_names()[index]

    def get_sheet_by_name(self, name):
        """根据name获取对应的sheet对象"""
        return self.book.sheet_by_name(name)

    def get_rows(self, index):
        return self.get_sheet(index).nrows

    def get_data(self, index):
        """返回对应sheet的列表数据"""
        return [self.get_sheet(index).row_values(row)[0] for row in range(self.get_rows(index))]





