---
title: FTP上传下载文件
date: 2024-01-20
categories:
  - CPP
  - 网络编程
  - libcurl
tags:
  - FTP
  - libcurl
  - cpp
  - 文件传输
description: 使用libcurl库实现FTP文件上传下载功能的CPP实现
author: JerryMa
---

# ftp上传下载文件

## libcurl从ftp上获取文件列表信息，包含中文

```cpp
inline std::wstring to_wstring(std::string const& str)
{
    std::wstring ustr;
    int const length = MultiByteToWideChar(
        CP_UTF8, 0,
        str.c_str(), static_cast<int>(str.length()),
        nullptr, 0);
    if (length <= 0)
        return ustr;
    ustr.resize(static_cast<size_t>(length));
    int const result = MultiByteToWideChar(
        CP_UTF8, 0,
        str.c_str(), static_cast<int>(str.length()),
        const_cast<wchar_t*>(ustr.data()), length);
    if (result != length)
        ustr.clear();
    return ustr;
}

std::wstring_convert<std::codecvt_utf8<wchar_t>> utf8Converter;

size_t WriteCallback(char* contents, size_t size, size_t nmemb, std::string* userp)
{
    size_t totalSize = size * nmemb;
    userp->append(contents, totalSize);
    return totalSize;
}
bool GetFtpFileList(const char* ftpUrl, const char* username, const char* password, CString& strResult)
{
    CURL* curl;
    CURLcode res;

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if (curl)
    {
        std::string response;

        struct curl_slist* headers = NULL;
        headers = curl_slist_append(headers, "Accept: */*");
        string strUserName = username;
        string strPassWord = password;
        curl_easy_setopt(curl, CURLOPT_URL, ftpUrl);
        curl_easy_setopt(curl, CURLOPT_USERPWD, (strUserName + ":" + strPassWord).c_str());  // 密码和用户名以":"连接，如："username:password"
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
        curl_easy_setopt(curl, CURLOPT_FTP_USE_EPRT, 1L);  // 使用更安全的EPR命令（如果支持）
        curl_easy_setopt(curl, CURLOPT_FTPLISTONLY, 1L);   // 只列出文件，不下载

        res = curl_easy_perform(curl);

        if (res != CURLE_OK)
        {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        }
        else
        {
            // 尝试将字符串转换为宽字符串以便正确显示中文等非ASCII字符
            std::wstring wideResponse = utf8Converter.from_bytes(response);
            std::wcout << L"FTP directory listing:\n";
            std::wcout << wideResponse.c_str() << std::endl;
            strResult = wideResponse.c_str();
        }

        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    }

    curl_global_cleanup();

    return (res == CURLE_OK);
}
int GetFtpDirectoryList(const char* ftpUrl, const char* username, const char* password, const char* strRemotePath, vector<CString>& fileList)
{
    CURL* curl;
    CURLcode res;
    CString strRemote = strRemotePath;
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if (curl)
    {
        std::string response;

        curl_slist* headers = NULL;
        headers = curl_slist_append(headers, "Accept: */*");
        string strUserName = username;
        string strPassWord = password;
        curl_easy_setopt(curl, CURLOPT_URL, ftpUrl);
        curl_easy_setopt(curl, CURLOPT_USERPWD, (strUserName + ":" + strPassWord).c_str());  // 密码和用户名以":"连接，如："username:password"
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
        curl_easy_setopt(curl, CURLOPT_FTP_USE_EPRT, 1L);  // 使用更安全的EPR命令（如果支持）
        curl_easy_setopt(curl, CURLOPT_DIRLISTONLY, 1L);   // 只列出目录内容

        res = curl_easy_perform(curl);

        if (res == CURLE_OK)
        {
            // 解析响应字符串，提取文件和子目录名
            // 这里假设FTP服务器返回的是NLST格式，每行一个条目
            std::wstring wideResponse = utf8Converter.from_bytes(response);
            CString strResult = wideResponse.c_str();
            vector<CString> dirVec;
            dirVec.clear();
            int nFind = strResult.Replace(_T("\r\n"), _T("\r\n"));
            if (nFind > 0)
            {
                // 使用CString::Find()函数找到第一个\r\n的位置
                int pos = strResult.Find(_T("\r\n"));
                // 循环遍历所有\r\n分隔符，并将字符串拆分成一个一个的
                while (pos != -1)
                {
                    // 获取当前分隔符之前的子串
                    CString subStr = strResult.Left(pos);
                    if ((subStr.CompareNoCase(_T(".")) == 0)
                        ||(subStr.CompareNoCase(_T("..")) == 0))
                    {
                        continue;
                    }

                    if (subStr.GetAt(subStr.GetLength() - 1) == _T('/'))
                    {
                        dirVec.push_back(strRemote + subStr);
                    }
                    strRemote.Replace(_T("/"), _T("\\"));

                    fileList.push_back(strRemote + subStr);
                    // 将字符串指针移动到下一个分隔符的位置
                    strResult = strResult.Mid(pos + 2);
                    // 重新获取分隔符的位置
                    pos = strResult.Find(_T("\r\n"));
                }
                // 处理最后一个子串

                if (!strResult.IsEmpty())
                {
                    if (strResult.GetAt(strResult.GetLength() - 1) == _T('/'))
                    {
                        dirVec.push_back(strRemote + strResult);
                    }
                    fileList.push_back(strRemote + strResult);
                }
            }
            else
            {
                fileList.push_back(strRemote + strResult);
            }
            // 对于每个子目录，进行递归调用

            for (auto entry : dirVec)
            {
                string strFtp = ftpUrl;
                string strEntry = (LPCSTR)(CStringA)(entry);
                strEntry += +"/";
                string subDirUrl = strFtp + strEntry;
                GetFtpDirectoryList(subDirUrl.c_str(), username, password, strEntry.c_str(), fileList);
            }
        }
        else
        {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        }

        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    }

    curl_global_cleanup();

    return (res == CURLE_OK);
}
```

CPP

具体调用函数为：

```cpp
static void ADSKMyGroupTEST() {

        //const char* ftpServer = "ftp://127.0.0.1:21/";
        //const char* ftpUsername = "ftp";
        //const char* ftpPassword = "ftp";

        CString strFtpSerVer = CUtility::getValueByKey(INI_SETTING_FTPSETTING, INI_NODE_FTPSERVER);
        CString ftpServer = _T("ftp://") + strFtpSerVer;
        CString ftpUsername = CUtility::getValueByKey(INI_SETTING_FTPSETTING, INI_NODE_FTPUSER);
        CString ftpPassword = CUtility::getValueByKey(INI_SETTING_FTPSETTING, INI_NODE_FTPPASSWD);
        CString strLocal = CUtility::getValueByKey(INI_SETTING_FTPSETTING, INI_NODE_FTPLOCALPATH);
        std::vector<CString> allFileList;

        GetFtpDirectoryList((LPCSTR)(LPCTSTR)ftpServer, (LPCSTR)(LPCTSTR)ftpUsername, (LPCSTR)(LPCTSTR)ftpPassword, "", allFileList);

        FtpManage ftp;
        ftp.ConnectFtp();
        for (const auto& item : allFileList)
        {
            CString localPath = strLocal + item;  // 设置本地存储路径

            if (localPath.Find(_T(".")) < 0)  // 如果是目录
            {
                ::CreateDirectory(localPath, NULL);
            }
            else  // 如果是文件
            {
                CString ftpFilePath = _T("/") + item;
                string outputfile = (LPCSTR)(CStringA)(localPath);
                ftp.GetFileFromFtp(ftpFilePath, localPath);
            }
        }
        ftp.CloseFtpConnect();
    }
```

CPP

## 从ftp下载文件

ftpmanage.h

```cpp
#pragma once
#include <afxinet.h>
#include <vector>
using namespace std;

//对 ftp文件进行下载及相关的操作类
class FtpManage
{
public:
    FtpManage();
    ~FtpManage();
private:
    void InitFtpSetting();

    CString	m_strFTPServer;//ftp服务器
    CString m_strFTPPassive;//passive标记
    CString m_strFTPRoot;//ftp根目录
    CString m_strFTPUser;//ftp账号
    CString m_strFTPPassWd;//ftp密码

    CInternetSession* m_pInetSession;
    CFtpConnection* m_pFtpConnection;
    vector<CString> getSplitStringVector(CString strFtpPath, LPCTSTR param2 = _T("/"));
public:

    
    int ConnectFtp();

    //从ftp下载文件
    int GetFileFromFtp(/*CString strFtpPath, */CString strFtpFileName, CString strDwgSavePath);

    //上传文件到ftp
    int PutFileToFtp(CString strLocalFilePath, CString strFtpPath);
    int PutFileToFtpEx(CString strLocalFilePath, CString strFtpPath, CString strFtpFileName);

    //分级设置ftp dir 
    int SetCurrentFtpDir(CString strFtpPath);

    //关闭ftp连接
    int CloseFtpConnect();
    //获取ftp目录中的所有文件//获取中文文件名乱码，不可用
    vector<CString> getAllFileFromFtpServer();
};
```

CPP

ftpmanage.cpp

```cpp
#include "stdafx.h"
#include "FtpManage.h"
#include <xlocbuf>
#include <codecvt>

FtpManage::FtpManage():m_pInetSession(NULL),m_pFtpConnection(NULL)
{
    InitFtpSetting();
}

FtpManage::~FtpManage()
{

}

void FtpManage::InitFtpSetting()
{
    m_strFTPServer = CUtility::getValueByKey(INI_SETTING_FTPSETTING, INI_NODE_FTPSERVER);
    m_strFTPPassive = CUtility::getValueByKey(INI_SETTING_FTPSETTING, INI_NODE_FTPPASSIVE);
    m_strFTPRoot = CUtility::getValueByKey(INI_SETTING_FTPSETTING, INI_NODE_FTPROOT);
    m_strFTPUser = CUtility::getValueByKey(INI_SETTING_FTPSETTING, INI_NODE_FTPUSER);
    m_strFTPPassWd = CUtility::getValueByKey(INI_SETTING_FTPSETTING, INI_NODE_FTPPASSWD);
}

std::vector<CString> FtpManage::getSplitStringVector(CString strFtpPath, LPCTSTR param2 /*= _T("/")*/)
{
    vector<CString> retVec;
    retVec.clear();
    int nFind = strFtpPath.Replace(_T("/"), _T("/"));
    if (nFind <= 0)
    {
        retVec.push_back(_T("/"));
        return retVec;
    }
    for (int i=0; i<=nFind; i++)
    {
        retVec.push_back(CUtility::SubString(strFtpPath, _T("/"), i) + _T("/"));
    }
    return retVec;
}

int FtpManage::GetFileFromFtp(/*CString strFtpPath, */CString strFtpFileName, CString strDwgSavePath)
{
    //if (SetCurrentFtpDir(strFtpPath)<0)
    //{
    //	return -1;
    //}
    CFtpFileFind findFile(m_pFtpConnection);
    if (findFile.FindFile(strFtpFileName, INTERNET_FLAG_DONT_CACHE))
    {
        if (!m_pFtpConnection->GetFile(strFtpFileName,strDwgSavePath, FALSE, FILE_ATTRIBUTE_NORMAL, FTP_TRANSFER_TYPE_BINARY, 1))
        {
            DWORD dw = GetLastError();
            CString sError;
            AfxMessageBox(_T("ftp getfile error :%d"), dw);
            return -3;
        }
    }
    else
    {
        return -2;
    }

    return 0;
}

int FtpManage::ConnectFtp()
{
    CWaitCursor wait;

    CString m_sDomainName(m_strFTPServer);
    CString m_ftpUser(m_strFTPUser);
    CString m_ftpPassword(m_strFTPPassWd);

    m_pFtpConnection = NULL;
    m_pInetSession = new CInternetSession(_T("ESAPP"), 1, PRE_CONFIG_INTERNET_ACCESS, NULL, NULL, INTERNET_FLAG_DONT_CACHE);
    if (!m_pInetSession)
    {
        return -1;
    }

    CString strFtpSite = m_sDomainName;
    CString strServerName;
    CString strObject;
    INTERNET_PORT nPort;
    DWORD dwServiceType;

    //检查URL是否正确
    if (!AfxParseURL(strFtpSite, dwServiceType, strServerName, strObject, nPort) || dwServiceType == AFX_INET_SERVICE_UNK)
    {
        CString strFtpURL = _T("ftp://");
        strFtpURL += strFtpSite;

        if (!AfxParseURL(strFtpURL, dwServiceType, strServerName, strObject, nPort))
        {
            return -2;
        }
    }

    if ((dwServiceType == INTERNET_SERVICE_FTP) && !strServerName.IsEmpty())
    {
        try
        {
            //AfxMessageBox(strServerName + _T("\r") + m_ftpUser + _T("\r") + m_ftpPassword);
            if (m_strFTPPassive == _T("TRUE"))
            {
                m_pFtpConnection = m_pInetSession->GetFtpConnection(strServerName, m_ftpUser, m_ftpPassword, nPort, TRUE);
            }
            else
            {
                m_pFtpConnection = m_pInetSession->GetFtpConnection(strServerName, m_ftpUser, m_ftpPassword, nPort, FALSE);
            }
        }
        catch (CInternetException* pEx)
        {
            CString strInteError = _T("");
            TCHAR szErr[1024];
            if (pEx->GetErrorMessage(szErr, 1024))
            {
                strInteError.Format(_T("%s"), szErr);
                pEx->Delete();
            }
            AfxMessageBox(strInteError);
            return -3;
        }
    }
    return 0;
}

int FtpManage::PutFileToFtp(CString strLocalFilePath, CString strFtpPath)
{
    CString sFileName;
    int nFind = strLocalFilePath.ReverseFind(_T('\\'));
    sFileName = strLocalFilePath.Mid(nFind+1);

    return PutFileToFtpEx(strLocalFilePath, strFtpPath, sFileName);
}

int FtpManage::PutFileToFtpEx(CString strLocalFilePath, CString strFtpPath, CString strFtpFileName)
{
    int nRes = SetCurrentFtpDir(strFtpPath);
    if (nRes!=0)
    {
        return -1;
    }
    CFtpFileFind findFile(m_pFtpConnection);
    if (findFile.FindFile(strFtpFileName,INTERNET_FLAG_DONT_CACHE))
    {
        m_pFtpConnection->Remove(strFtpFileName);
    }
    if (!m_pFtpConnection->PutFile(strLocalFilePath,strFtpFileName))
    {
        DWORD dw = GetLastError();
        int nError = (int)dw;
        CString strInterError;
        strInterError.Format(_T("%d"), nError);
        AfxMessageBox(strInterError);
        return -2;
    }
    return 0;
}

int FtpManage::SetCurrentFtpDir(CString strFtpPath)
{
    if (m_pFtpConnection==NULL)
    {
        return -1;
    }
    //会存在多级 然后一次设置下去 如果失败了 就返回问题
    strFtpPath.Replace(_T("\\"), _T("/"));

    vector<CString> vecCatalogue;
    //gMyString.Split(strFtpPath, _T("/"), vecCatalogue);
    vecCatalogue = getSplitStringVector(strFtpPath, _T("/"));
    for (int i=0;i<vecCatalogue.size();i++)
    {
        CString sTempCatalogue = vecCatalogue[i];
        if (sTempCatalogue==_T(""))
        {
            continue;
        }
        if (!m_pFtpConnection->SetCurrentDirectory(sTempCatalogue))
        {
            if (!m_pFtpConnection->CreateDirectory(sTempCatalogue))
            {
                return -2;
            }
            if (!m_pFtpConnection->SetCurrentDirectory(sTempCatalogue))
            {
                return -3;
            }
        }
    }
    return 0;
}

int FtpManage::CloseFtpConnect()
{
    if (m_pFtpConnection!=NULL)
    {
        m_pFtpConnection->Close();
        delete m_pFtpConnection;
        m_pFtpConnection = NULL;
    }
    if (m_pInetSession!=NULL)
    {
        m_pInetSession->Close();
        delete m_pInetSession;
        m_pInetSession = NULL;
    }
    return 0;
}
wchar_t * ANSIToUnicode(const char* str)
{
    int textlen;
    wchar_t * result;
    textlen = MultiByteToWideChar(CP_ACP, 0, str, -1, NULL, 0);
    result = (wchar_t *)malloc((textlen + 1) * sizeof(wchar_t));
    memset(result, 0, (textlen + 1) * sizeof(wchar_t));
    MultiByteToWideChar(CP_ACP, 0, str, -1, (LPWSTR)result, textlen);
    return result;
}

//获取中文文件名乱码
std::vector<CString> FtpManage::getAllFileFromFtpServer()
{
    vector<CString> tmpVec;
    tmpVec.clear();
    if (SetCurrentFtpDir(m_strFTPServer) < 0)
    {
        return tmpVec;
    }
    try
    {
        // use a file find object to enumerate files
        CFtpFileFind findFile(m_pFtpConnection);
        CString strName, strDirectory;
        m_pFtpConnection->GetCurrentDirectory(strDirectory);
        // start looping
        BOOL bWorking = findFile.FindFile(_T("*"));

        //while (bWorking)
        //{
        //	bWorking = findFile.FindNextFile();
        //	tmpVec.push_back(findFile.GetFileURL());
        //	//_tprintf_s(_T("%s\n"), (LPCTSTR)findFile.GetFileURL());
        //}

        BOOL bFind = findFile.FindFile(_T("/"), INTERNET_FLAG_EXISTING_CONNECT);
        bool flag = false;
        while (bFind)
        {
            bFind = findFile.FindNextFile();

            if (findFile.IsDots())
            {
                continue;
            }
            CString remoteFileName = findFile.GetFileName();
            // 转换为 UTF-8 编码
            std::string fileNameUtf8 = std::wstring_convert<std::codecvt_utf8<wchar_t>>().to_bytes(findFile.GetFileName());

            CString strName = fileNameUtf8.c_str();
            
    /*		CString remoteFilePath = remoteDir + remoteFileName;
            CString localFilePath = localDir + remoteFileName;*/
            //flag = 1为获取目录下的子文件，flag = 0为获取当前文件夹下的所有子文件。
            if (flag)
            {
                if (findFile.IsDirectory())
                {
                    // 如果是目录，递归下载其中的文件和子目录
                    //CreateDirectory(localFilePath, nullptr);

                    strDirectory = strDirectory + _T("/") + strName;
                    tmpVec.push_back(strName);
                }
            }
            else
            {
                tmpVec.push_back(strName);
            }
        }

        findFile.Close();
    }
    catch (CInternetException* pEx)
    {
        TCHAR sz[1024];
        pEx->GetErrorMessage(sz, 1024);
        _tprintf_s(_T("ERROR!  %s\n"), sz);
        pEx->Delete();
    }
    return tmpVec;
}
```