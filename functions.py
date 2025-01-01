import csv
import sqlite3
import os
import shutil
from openpyxl import Workbook as wb, load_workbook as lw
def from_csv_to_xlsx(csvf, xlsxf):
    workbook = wb()
    sheet = workbook.active
    with open(csvf, newline='', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            sheet.append(row)
    workbook.save(xlsxf)

def format(fname, ext):
    '''
    формирует имя файла из названия и расширения
    :param fname: string
    :param ext: string
    :return: filename
    '''
    return fname + '.' + ext if '.' + ext not in fname else fname
def from_xlsx_to_csv(csvf, xlsf):
    with open(csvf, 'w', newline='', encoding="utf8") as csvfile:
        t = []
        for lst in lw(filename=xlsf, data_only=True):
            for i, col in enumerate(lst):
                z = list(map(lambda row: '' if row.value is None else str(row.value), col))
                if len(z) == 1:
                    ind = z[0].find('"')
                    if ind == -1:
                        s = z[0].split(';')
                    else:
                        s, v = z[0][:ind].split(';'), z[0][ind+1:-1]
                        s[-1] = v
                else:
                    s = z
                if i == 0:
                    fields = s
                else:
                    t.append(s)
        writer = csv.DictWriter(csvfile, quotechar='"', delimiter=';', fieldnames=fields)
        writer.writeheader()
        t = list(map(lambda x: dict(zip(fields, x)), t))
        writer.writerows(t)

class WrongTypeError(Exception):
    def __str__(self):
        return 'Неверный формат файла! Допускается только csv/xlsx!'


def from_csv_to_sql(type, filename, sqlname):
    with open(filename, encoding="utf8") as f:
        csvf = csv.DictReader(f, delimiter=';', quotechar='"')
        con = sqlite3.connect('PyQTest.db')
        for d in list(csvf):
            if 'MULTIMEDIA' in d.keys() and d['MULTIMEDIA']!='':
                old = d['MULTIMEDIA']
                d['MULTIMEDIA'] = f'media/{sqlname}/{os.path.basename(d["MULTIMEDIA"])}'
                shutil.copy2(old, d['MULTIMEDIA'])
            if type == 'game':
                req = f'''INSERT INTO {sqlname}(X, Y, THEME, POINT, ASK, CORRECT, MULTIMEDIA) VALUES(
                            "{d['X']}", "{d['Y']}", "{d['THEME']}", "{d['POINT']}", "{d['ASK']}", "{d['CORRECT']}", "{d['MULTIMEDIA']}")'''
            elif type == 'test':
                req = f'''INSERT INTO {sqlname}(ASK, CORRECT, MULTIMEDIA, ANSWERS) VALUES(
                            "{d['ASK']}", "{d['CORRECT']}", "{d['MULTIMEDIA']}", "{d['ANSWERS']}")'''
            else:
                raise WrongTypeError
            con.cursor().execute(req)
        con.commit()
def from_sql_to_csv(type, filename, sqlname):
    con = sqlite3.connect('PyQTest.db')
    if type == 'game':
        req = f'''SELECT X, Y, THEME, POINT, ASK, CORRECT, MULTIMEDIA FROM {sqlname}'''
    elif type == 'test':
        req = f'''SELECT ASK, CORRECT, MULTIMEDIA, ANSWERS FROM {sqlname}'''
    else:
        raise WrongTypeError
    vals = con.cursor().execute(req).fetchall()
    if type == 'game':
        fn = ['X', 'Y', 'THEME', 'POINT', 'ASK', 'CORRECT', 'MULTIMEDIA']
    elif type == 'test':
        fn = ['ASK', 'CORRECT', 'MULTIMEDIA', 'ANSWERS']
    with open(filename, 'w', newline='', encoding="utf8") as csvfile:
        csvf = csv.DictWriter(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=fn)
        csvf.writeheader()
        for val in vals:
            csvf.writerow(dict(zip(fn, val)))
def from_sql_to_file(ext, type, filename, sqlname):
    if ext == 'csv':
        from_sql_to_csv(type, format(filename,'csv'), sqlname)
    elif ext == 'xlsx':
        from_sql_to_csv(type, format(filename,'csv'), sqlname)
        from_csv_to_xlsx(format(filename,'csv'), format(filename,'xlsx'))
    else:
        raise WrongTypeError

def from_file_to_sql(ext, type, filename, sqlname):
    if ext == 'csv':
        from_csv_to_sql(type, format(filename,'csv'), sqlname)
    elif ext == 'xlsx':
        from_xlsx_to_csv(format(filename,'csv'), format(filename,'xlsx'))
        from_csv_to_sql(type, format(filename,'csv'), sqlname)
    else:
        raise WrongTypeError

