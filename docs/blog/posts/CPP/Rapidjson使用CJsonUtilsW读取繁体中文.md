---
title: Rapidjson使用CJsonUtilsW读取繁体中文
date: 2024-04-22
categories:
  - windows程序
tags:
  - cpp
  - RapidJSON
  - UTF-8
  - 繁体中文
description: 使用RapidJSON和CJsonUtilsW处理包含繁体中文的UTF-8编码JSON文件
author: JerryMa
---

# Rapidjson使用CJsonUtilsW读取繁体中文

## 先要确保json文件格式为utf-8

## 文件内容如下所示：

```json
{
  "TABLE_PARAMETER": {
    "TitleHeight": 6.0,
    "TitleCol1": 8.0,
    "TitleCol2": 28.0,
    "TitleCol3": 12.0,
    "TitleCol4": 24.0,
    "RowHeight": 6.0,
    "ColWidth": 12.0,
    "TitleTextHeight":3.0,
    "ThirdTextHeight":3.5,
    "CellTextHeight":3.2
  },
  "EXCEL_CONFIG": {
        "RowHeight": 15, 
        "ColWidth": 2, 
        "SmallWidth": 2, 
        "MergeRows": 2, 
        "DiagonalText":"序號               數值"
    }
}
```

## 处理文件数据的读取

### 读取utf-8文件内容

```cpp
std::wstring  CGlobalHelper::read_utf8_file(const std::string &path)
{
    std::locale::global(std::locale("en_US.UTF-8"));

    // 打开文件
    std::ifstream file(path.c_str());

    if (!file.is_open()) {
        return L"";
    }

    // 读取文件内容并存储到wstring中
    /*std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
    std::wstring content((std::istreambuf_iterator<char>(file)),
        std::istreambuf_iterator<char>());
    file.close();*/
    std::wstring content;
    file.seekg(0, std::ios::end);
    content.reserve(file.tellg());
    file.seekg(0, std::ios::beg);

    content.assign((std::istreambuf_iterator<char>(file)),
        std::istreambuf_iterator<char>());

    // 关闭文件
    file.close();
    return content;
}
```

### utf8转unicode

```cpp
std::wstring CGlobalHelper::utf8ToUnicode(const char *pszU8)
{
    int    n = MultiByteToWideChar(CP_UTF8, 0, pszU8, -1, NULL, 0);
    WCHAR *pwsz = new WCHAR[n + 1];
    memset((void *)pwsz, 0, (n + 1) * sizeof(WCHAR));
    MultiByteToWideChar(CP_UTF8, 0, pszU8, -1, pwsz, n);

    std::wstring wstr = pwsz;
    delete[] pwsz;

    return wstr;
}
```

```
gbk可以正常显示中文，utf8-bom可以正常显示中文，utf8无bom中文显示乱码，需要转为unicode字符
```

### 处理具体的数据读取

#### wstring转string

- **使用迭代方式：**

```cpp
#include <string>
#include <locale>

std::wstring wide = L"wide";
std::string str(wide.begin(), wide.end());
```

-  **使用 Windows API：**

```cpp
#include <comdef.h>
#include <string>
#include <windows.h>

std::string Wstring2String(const std::wstring& wstr) {
int len = WideCharToMultiByte(CP_ACP, 0, wstr.c_str(), wstr.size(), nullptr, 0, nullptr, nullptr);
if (len <= 0) {
return "";
}
char* buffer = new char[len + 1];
WideCharToMultiByte(CP_ACP, 0, wstr.c_str(), wstr.size(), buffer, len, nullptr, nullptr);
buffer[len] = '\0';
std::string res(buffer);
delete[] buffer;
return res;
}

std::wstring String2Wstring(const std::string& str) {
int len = MultiByteToWideChar(CP_ACP, 0, str.c_str(), str.size(), nullptr, 0);
if (len < 0) {
return L"";
}
wchar_t* buffer = new wchar_t[len + 1];
MultiByteToWideChar(CP_ACP, 0, str.c_str(), str.size(), buffer, len);
buffer[len] = '\0';
std::wstring res(buffer);
delete[] buffer;
return res;
}
```

- **使用 `std::wstring_convert`（CPP11 及更高版本）：**

```cpp
#include <locale>
#include <codecvt>
#include <string>

std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;

// wstring to string
std::string wstringToString(const std::wstring& wstr) {
return converter.to_bytes(wstr);
}

// string to wstring
std::wstring stringToWstring(const std::string& str) {
return converter.from_bytes(str);
}
```

#### 读取具体数据

读取utf-8数据后，需要将utf8乱码数据转成unicode，才能显示正确的繁体中文

```cpp
CString strFileName = CUtility::GetAppPath() + CONFIG_JSON_FILE;

CString strContent;
wstring str;
str = CGlobalHelper::read_utf8_file(string(CW2A(strFileName))).c_str();
strContent = str.c_str();

CJsonUtilsW json;
json.Parse(strContent);
m_dRowHeight = json[JSON_NODE_EXCEL_CONFIG][JSON_KEY_Row_Height];
m_dRColWidth = json[JSON_NODE_EXCEL_CONFIG][JSON_KEY_Col_Width];
m_nSmallWidth = json[JSON_NODE_EXCEL_CONFIG][JSON_KEY_SMALL_WIDTH];
m_nMergeRows = json[JSON_NODE_EXCEL_CONFIG][JSON_KEY_MergeRows];
wstring strRet1 = json[JSON_NODE_EXCEL_CONFIG][JSON_KEY_DIAGONAL_TEXT];
string strmid(strRet1.begin(), strRet1.end());
wstring wstrRet = CGlobalHelper::utf8ToUnicode(strmid.c_str());
m_strDiagonalText = wstrRet.c_str();
```

## 其它转换代码

```cpp
void unicodeToUTF8(const wstring &src, string& result)
{
    int n = WideCharToMultiByte(CP_UTF8, 0, src.c_str(), -1, 0, 0, 0, 0);
    result.resize(n);
    ::WideCharToMultiByte(CP_UTF8, 0, src.c_str(), -1, (char*)result.c_str(), result.length(), 0, 0);
}
void unicodeToGB2312(const wstring& wstr, string& result)
{
    int n = WideCharToMultiByte(CP_ACP, 0, wstr.c_str(), -1, 0, 0, 0, 0);
    result.resize(n);
    ::WideCharToMultiByte(CP_ACP, 0, wstr.c_str(), -1, (char*)result.c_str(), n, 0, 0);
}
void utf8ToUnicode(const string& src, wstring& result)
{
    int n = MultiByteToWideChar(CP_UTF8, 0, src.c_str(), -1, NULL, 0);
    result.resize(n);
    ::MultiByteToWideChar(CP_UTF8, 0, src.c_str(), -1, (LPWSTR)result.c_str(), result.length());
}
 
void gb2312ToUnicode(const string& src, wstring& result)
{
    int n = MultiByteToWideChar(CP_ACP, 0, src.c_str(), -1, NULL, 0);
    result.resize(n);
    ::MultiByteToWideChar(CP_ACP, 0, src.c_str(), -1, (LPWSTR)result.c_str(), result.length());
}
string WCharToMByte(LPCWSTR lpcwszStr)
{
    string str;
    DWORD dwMinSize = 0;
    LPSTR lpszStr = NULL;
    dwMinSize = WideCharToMultiByte(CP_OEMCP, NULL, lpcwszStr, -1, NULL, 0, NULL, FALSE);
    if (0 == dwMinSize)
    {
        return FALSE;
    }
    lpszStr = new char[dwMinSize];
    WideCharToMultiByte(CP_OEMCP, NULL, lpcwszStr, -1, lpszStr, dwMinSize, NULL, FALSE);
    str = lpszStr;
    delete[] lpszStr;
    return str;
}
void Wchar_tToString(std::string& szDst, wchar_t *wchar)
{
    wchar_t * wText = wchar;
    DWORD dwNum = WideCharToMultiByte(CP_OEMCP, NULL, wText, -1, NULL, 0, NULL, FALSE);// WideCharToMultiByte的运用
    char *psText; // psText为char*的临时数组，作为赋值给std::string的中间变量
    psText = new char[dwNum];
    WideCharToMultiByte(CP_OEMCP, NULL, wText, -1, psText, dwNum, NULL, FALSE);// WideCharToMultiByte的再次运用
    szDst = psText;// std::string赋值
    delete[]psText;// psText的清除
}
```