---
title: 将CPP代码转成Word
date: 2024-04-30
categories:
  - windows程序
tags:
  - Python
  - CPP
description: 使用Python脚本将CPP代码文件转换为Word文档的实用工具
author: JerryMa
---

# 将cpp代码转成word

代码如下所示：

```python
# -*- coding:UTF-8 -*-
import os

# 获取同一目录下的所有.h和.cpp文件的绝对路径
def getFileName(filedir):

    file_list = [os.path.join(root, filespath) \
                 for root, dirs, files in os.walk(filedir) \
                 for filespath in files \
                 if str(filespath).endswith((".h", ".cpp"))
                 ]
    return file_list if file_list else []
def renaming(file):
    """修改后缀"""
    ext = os.path.splitext(file)    # 将文件名路径与后缀名分开

    if ext[1] == '.h':                    # 文件名：ext[0]
        new_name = ext[0] + '.doc'         # 文件后缀：ext[1]
        os.rename(file, new_name)           # tree()已切换工作地址，直接替换后缀
    elif ext[1] == '.cpp':
        new_name = ext[0] + '.doc'
        os.rename(file, new_name)

def  MergeHFileToWord(file_dir):
    h_fileName = getFileName(file_dir)
    if h_fileName:
        wordFile = file_dir + "\\code.doc";
        print('输出的word为:'+ str(wordFile))
        for h_file in h_fileName:
            print('文件名为:'+ str(h_file))
            with open(h_file,encoding='utf-8', errors='ignore') as f: #读取每个文件
                flag=0
                for line in f.readlines(): #将每个文件文本统一逐行写入一个word中
                    try:
                        with open(wordFile,"a",encoding='utf-8') as mom:
                            if flag==0:
                                mom.write(h_file)	#每行开头写入文件名
                                flag=1
                            mom.write('\n'+line)
                            mom.write('\n') #用回车分隔
                    except Exception as e:
                        print(e)
                        pass


def generateSingleFile(file_dir):
    h_fileName = getFileName(file_dir)
    if h_fileName:
        for h_file in h_fileName:
            print('文件名为:'+ str(h_file))
            with open(h_file,encoding='utf-8', errors='ignore') as f: #读取每个文件
                flag=0
                docfile = h_file + ".doc"
                print('输出为:'+ str(docfile))
                for line in f.readlines(): #将每个文件文本统一逐行写入一个word中
                    try:
                        with open(docfile,"a",encoding='utf-8') as mom:
                            if flag==0:
                                mom.write(h_file)	#每行开头写入文件名
                                flag=1
                            mom.write('\n'+line)          
                    except Exception as e:
                        print(e)
                        pass

if __name__ == '__main__':
    file_dir = str(input('\n请输入代码文件夹目录: '))
    if file_dir.strip() == '':
        file_dir = "E:\\Gitee\\project\\zw-wh-for-cpp\\SecondPart\\DimTools\\DimTools"
    MergeHFileToWord(file_dir);
    generateSingleFile(file_dir);

```

