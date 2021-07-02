# coding=utf-8
import xlrd


class ReadData:
    def get_name(self,sheet):
        return sheet.row_values(1)[0]

    def get_url(self,sheet):
        return sheet.row_values(1)[1]

    def get_method(self,sheet):
        return sheet.row_values(1)[2]

    def get_query(self,sheet):
        query_rows = []
        for row_num in range(1, sheet.nrows):
            row_values = sheet.row_values(row_num)
            query_rows.append(row_values)
        return query_rows

    def get_header(self,sheet):
        header_rows = []
        for row_num in range(1, sheet.nrows):
            row_values = sheet.row_values(row_num)
            header_rows.append(row_values)
        return header_rows

    def get_body(self,sheet):
        body = []
        for col_num in range(sheet.ncols):
            col_values = sheet.col_values(col_num)
            self.remove_tail_space(col_values)  # 删除每列最后由于列值个数不同而自动生成的空字符串
            param = dict()
            param['name'] = col_values[0]
            param['values'] = col_values[1:]
            body.append(param)
        return body

    def remove_tail_space(self, array):
        new_array = array[:]
        for i in range(len(new_array) - 1, -1, -1):
            if new_array[i] == '':
                array.pop()
            else:
                break

    def get_assert(self,sheet):
        assert_rows = []
        for row_num in range(1, sheet.nrows):
            row_values = sheet.row_values(row_num)
            assert_rows.append(row_values)
        return assert_rows

    def get_extract(self,sheet):
        extract_rows = []
        for row_num in range(1, sheet.nrows):
            row_values = sheet.row_values(row_num)
            extract_rows.append(row_values)
        return extract_rows

    def read_excel(self, excel_file):
        data = xlrd.open_workbook(excel_file)
        cfg_sheet = data.sheet_by_index(0)
        header_sheet = data.sheet_by_index(1)
        body_sheet = data.sheet_by_index(2)
        assert_normal_sheet = data.sheet_by_index(3)
        assert_fail_sheet = data.sheet_by_index(4)
        extract_sheet = data.sheet_by_index(5)

        result_json = dict()
        result_json["name"] = self.get_name(cfg_sheet)
        result_json["url"] = self.get_url(cfg_sheet)
        result_json["method"] = self.get_method(cfg_sheet)
        result_json["header"] = self.get_header(header_sheet)
        result_json["body"] = self.get_body(body_sheet)
        result_json["normal_assert"] = self.get_assert(assert_normal_sheet)
        result_json["fail_assert"] = self.get_assert(assert_fail_sheet)
        result_json["extract"] = self.get_extract(extract_sheet)
        return result_json

if __name__ == '__main__':
    # 测试代码
    readdata = ReadData()
    result_json = readdata.read_excel('F:\\code\\itest\\autocase\\data\studentcase.xls')
    print(result_json)


