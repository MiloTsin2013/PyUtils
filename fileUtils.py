import codecs
import chardet
import os

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
    以二进制的形式分行获取文件内容，分析文件编码格式，当达到高准确率时，返回编码格式，适用于大文件。
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
    '''
    获取文件的大小,结果保留两位小数，单位为MB
    '''
    size = os.path.getsize(file)
    size = size/float(1024*1024)
    return round(size, 2) # 四舍五入，保留两位小数点

def convert(file, encoding="UTF-8"):
    '''
    将指定文件转换到指定格式，默认的是转到 UTF-8
    file:    文件路径
    encoding:  输出文件格式
    '''
    print("Start")
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
    '''
    获取文件夹下所有文件的名字
    '''
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
    '''
    获取文件夹下所有文件夹的名字
    '''
    folderNames = []
    files=os.listdir(folderPath)	# 得到文件夹下的所有文件名称
    for file in files:	# 遍历文件夹
        if os.path.isdir("{}//{}".format(folderPath, file)):	# 判断是否是文件夹
            folderNames.append(file)
    return folderNames

if __name__ == "__main__":
    pass
