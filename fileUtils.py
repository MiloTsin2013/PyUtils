import codecs
import chardet
import os
import pickle
import csv
import xlwt
import xlrd
from xlutils.copy import copy
from win32com.client import Dispatch

def getCode1(file):
    '''
    以二进制的形式获取文件内容，判断文件编码格式，适用于小文件。
    （注：若文本内容过少可能会引起误判。）
    '''
    print("Getting code type...")
    with open(file, 'rb') as f:
        # result = chardet.detect(f.read())
        # print(result)
        code = chardet.detect(f.read())['encoding']
    print('Code is {}'.format(code))
    return code

def getCode2(file):
    '''
    以二进制的形式分行获取文件内容，分析文件编码格式。
    当达到高准确率时，返回编码格式，适用于大文件。
    '''
    print("Getting code type...")
    detector = chardet.universaldetector.UniversalDetector()
    with open(file, 'rb') as f:
        for line in f.readlines():
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    # print(detector.result)
    code = detector.result['encoding']
    print('Code is {}'.format(code))
    return code

def getSize(file):
    '''获取文件的大小,结果保留两位小数，单位为MB'''
    size = os.path.getsize(file)
    size = size/float(1024*1024)
    return round(size, 2) # 四舍五入，保留两位小数点

def convert(file, codeType=None, encoding="UTF-8"):
    '''将指定文件转换到指定格式，默认的是转到 UTF-8'''
    print("Start")
    if codeType == None:
        if getSize(file) <= 1:
            print('Small File...')
            codeType = getCode1(file)
        else:
            print('Big File...')
            codeType = getCode2(file)
    print("Convert {}".format(file))
    print("From {} to {} ...".format(codeType, encoding))
    with codecs.open(file, 'r', codeType, errors="ignore") as f:
        data = f.read()
    with codecs.open(file, 'w', encoding, errors='ignore') as f:
        f.write(data)
    print("Over")

def getFileNames(filePath):
    '''获取文件夹下所有文件的名字'''
    fileNames = []
    files = os.listdir(filePath)	# 得到文件夹下的所有文件名称
    # print(files)
    for file in files:	# 遍历文件夹
        # print(file)
        # print(os.path.isfile("{}//{}".format(filePath, file)))
        if os.path.isfile("{}//{}".format(filePath, file)):	# 判断是否是文件
            fileNames.append(file)
    # print(fileNames)
    return fileNames

def getFolderNames(folderPath):
    '''获取文件夹下所有文件夹的名字'''
    folderNames = []
    files=os.listdir(folderPath)	# 得到文件夹下的所有文件名称
    for file in files:	# 遍历文件夹
        if os.path.isdir("{}//{}".format(folderPath, file)):	# 判断是否是文件夹
            folderNames.append(file)
    return folderNames

def serializate(self,variable,file):
    '''进行序列化操作'''
    with open(file,'wb') as f:
        pickle.dump(variable,f)

def deserializate(self,file):
    '''进行反序列化操作'''
    with open(file,'rb') as f:
        variable = pickle.load(f)
    return variable

def writeExcel(savePath,content):
    '''Excel 写操作'''
    #创建一个Workbook
    book = xlwt.Workbook()
    #创建一个sheet,参数 名字,是否覆盖原有内容
    sheet = book.add_sheet("sheet1",cell_overwrite_ok=True)
    #将查询出的数据添加到表格中
    for row,rowContents in enumerate(content):
        for col,value in enumerate(rowContents):
            sheet.write(row,col,value)
    book.save(savePath)

def readExcel():
    '''Excel 读操作'''
    #打开文件获取数据
    myfile = xlrd.open_workbook('sheet.xls')
    # sheet_names = myfile.sheet_names()#获取表格中所有的sheet名字
    # print(sheet_names)
    #获取表单
    sheet = myfile.sheet_by_index(0)
    #sheet = myfile.sheets()[1]
    #sheet = myfile.sheet_by_name('Sheet2')
    # print(sheet.name)
    # print(sheet.ncols)
    # print(sheet.nrows)
    # print(sheet.row_values(0))#获取某一行的所有值
    # print(sheet.col_values(0))#获取某一列的所有值
    #获取某个单元格的值
    target = sheet.cell(0,1).value
    target = sheet.row(0)[0].value
    target = sheet.col(1)[1].value
    print(target)
    for row in range(0,sheet.nrows):
        for col in range(0,sheet.ncols):
            print(sheet.cell(row,col).value)

def modifyExcel(filePath, sheetNum):
    '''Excel 修改操作 （只能保存为 xls 格式，报讯 xlsx 格式文件损坏）'''
    # 打开文件获取数据
    myfile = xlrd.open_workbook(filePath)
    wb = copy(myfile)
    # 通过get_sheet()获取的sheet有write()方法
    ws = wb.get_sheet(sheetNum)
    row = 0
    col = 0
    ws.write(row, col, "modify")
    wb.save(filePath)

def doc2pdf(doc_name, pdf_name):
    """word文件转pdf"""
    try:
        word = Dispatch("Word.Application")
        if os.path.exists(pdf_name):
            os.remove(pdf_name)
        worddoc = word.Documents.Open(doc_name,ReadOnly = 1)
        worddoc.SaveAs(pdf_name, FileFormat = 17)
        worddoc.Close()
        word.Quit()
        return pdf_name
    except Exception as e:
        print('Error:',e)

def doc2docx(doc_name,docx_name):
    """doc转docx"""
    try:
        w = Dispatch('Word.Application')
        w.Visible = 0
        w.DisplayAlerts=0
        doc = w.Documents.Open(doc_name)
        doc.SaveAs(docx_name,FileFormat=12)
        doc.Close()
        w.Quit()
    except Exception as e:
        print(e)

def writeWord(path, value):
    '''Word 覆写操作'''
    try:
        doc = docx.Document(path)
        paragraphs=doc.paragraphs
        p = paragraphs[0].clear()
        r = p.add_run(value)
        r.font.bold = True    #加粗
        r.font.size = Pt(14)
        r.font.name = u'宋体'
        doc.save(path)
    except Exception as e:
        print(e)

        
if __name__ == "__main__":
    pass
