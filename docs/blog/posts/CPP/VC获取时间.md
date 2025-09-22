---
title: VC获取时间
date: 2023-12-22
categories:
  - windows程序
tags:
  - CPP
description: Visual CPP中获取和处理时间的多种方法和技巧
author: JerryMa
---

## 获取当前时间

```none
    SYSTEMTIME localTimeMin;
    GetLocalTime(&localTimeMin);
```

Plain text

## 计算两个时间的时间差

```none
#include "atltime.h"
#include <iostream>

using std::cout;
using std::endl;
using std::wcout;

int main()
{
    // 获取最小起始时间
    CTime TimeObj;
    SYSTEMTIME sysTimeMin;	
    TimeObj.GetAsSystemTime(sysTimeMin);//获取可传参的时间最小值
    __time64_t time = TimeObj.GetTime(); //此时获取的time=0;
    
// 最小start time 1970.01.01.08.0.0，小于此值会出现断言失败。
//	CTime startTime = CTime(1970,01,01,08,00,00); 
    CTime startTime = CTime(sysTimeMin.wYear,sysTimeMin.wMonth,sysTimeMin.wDay,sysTimeMin.wHour,sysTimeMin.wMinute,sysTimeMin.wSecond); //最小Base start time 1970.1.2.0.0.0
    cout << "起始时间：";
    cout<<startTime.GetYear()<<"年"<<startTime.GetMonth()<<"月"<<startTime.GetDay()<<"日"<<startTime.GetHour()<<"时"<<startTime.GetMinute()<<"分"<<startTime.GetSecond()<<"秒"<<endl;   
    
    // 获取当前的本地时间
    SYSTEMTIME sysTime;
    ::GetLocalTime(&sysTime);	
    CTime curTime(sysTime); //curTime精确到秒, 10位
    
    // 计算当前时间与起始时间之间的时间差(秒)
    CTimeSpan timeSpan;
    timeSpan = curTime - startTime; // 由于设置的是最小起始时间，所以timeSpan与curTime的成员变量存储的值是相同的。
    
    cout << "时间差：";
    cout << timeSpan.GetDays() << "天" << timeSpan.GetHours() << "小时" << timeSpan.GetMinutes() << "分" << timeSpan.GetSeconds() << "秒" << endl;   
    cout << "总小时数：" << timeSpan.GetTotalHours() << "小时" << endl;
    cout << "总分钟数：" << timeSpan.GetTotalMinutes() << "分钟" << endl;   
    cout << "总秒数：" << timeSpan.GetTotalSeconds() << "秒" <<endl;

    CString strTime;
    // 将当前时间curTime对象格式化为字符串   
    strTime = curTime.Format(_T("%Y-%m-%d %H:%M:%S"));   
    // 输出格式化字符串，由于字符串使用Unicode字符，所以要使用wcout输出   
    wcout<<"日期时间："<<(LPCTSTR)strTime<<endl;   

    system("pause");
    return 0;
}
```

Plain text

## 获取文件的修改时间

```none
FILETIME ftCreate, ftModify, ftAccess;
 CString strCreateTime, strModifyTime, strAccessTime;
 CString strFilePath = _T("");

 HANDLE hFile = CreateFile(strFilePath, GENERIC_READ,          // open for reading
  FILE_SHARE_READ,       // share for reading
  NULL,                            // default security
  OPEN_EXISTING,          // existing file only
  FILE_FLAG_BACKUP_SEMANTICS , // normal file
  NULL);

 SYSTEMTIME stLocal;
 if (!GetFileTime(hFile, &ftCreate, &ftAccess, &ftModify))
 {
  return ;
 }

 ZeroMemory(&stLocal, sizeof(SYSTEMTIME));
 FileTimeToSystemTime(&ftCreate, &stLocal);
 strCreateTime.Format("%04d-%02d-%02d %02d:%02d:%02d", stLocal.wYear, stLocal.wMonth, stLocal.wDay,  stLocal.wHour, stLocal.wMinute, stLocal.wSecond);   // 文件创建时间
 ZeroMemory(&stLocal, sizeof(SYSTEMTIME));
 FileTimeToSystemTime(&ftModify, &stLocal);
 strModifyTime.Format("%04d-%02d-%02d %02d:%02d:%02d", stLocal.wYear, stLocal.wMonth, stLocal.wDay,  stLocal.wHour, stLocal.wMinute, stLocal.wSecond); //  文件修改时间
 ZeroMemory(&stLocal, sizeof(SYSTEMTIME));
 FileTimeToSystemTime(&ftAccess, &stLocal);
 strAccessTime.Format("%04d-%02d-%02d %02d:%02d:%02d", stLocal.wYear, stLocal.wMonth, 
```