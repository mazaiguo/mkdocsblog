---
title: "Access drawing properties outside AutoCAD"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - COM
  - DWG
description: "We can use either MFC or ATL to create a client VC++ application of the COM server to access that information. In the attached sample, MFC is used...."
author: Autodesk
---
# Access drawing properties outside AutoCAD

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/access-drawing-properties-outside-autocad.html

## 文章内容

By Augusto Goncalves
We can use either MFC or ATL to create a client VC++ application of the COM server to access that information. In the attached sample, MFC is used. We should add a class Iproperties which wraps the methods and properties of the COM server from DwgPropsX.DLL with MFC class wizard into the project skeleton. Then we may find the ProgID of the COM server from Windows registry and find the CLSID with function CLSIDFromProgID. Of course, please make sure the COM server has been registered. The most common way to register Windows services is to use RegSvr32.Exe. We can also register them programmatically by calling it as a system command or with other APIs. Please find more information regarding this from MSDN.
The project supports multiple documents. When we open a DWG file with a view available, if it contains drawing properties, they will display in the current view. We can display properties of more drawings in multiple view windows. Anyway, the most important part is the following appended global function which contains COM initialization, ProgID to CLSID conversion, dispatch interface creation, properties retrieve, and COM clean up.
Full sample project.
// Global function to retrieve the drawing properties.
// In
//  LPCTSTR szFileName: Full path and name of a DWG file
// Output
//  LPCTSTR: A string containing all the property information
//  delimited by new line symbol '\n'
LPTSTR getSummaryInformation(LPCTSTR szFileName)
{
  LPTSTR szSummInfo = NULL;
  CString str;
  IProperties dwgProp;
  HRESULT hr = NOERROR;
  CLSID clsid;
  LPDISPATCH pDisp=NULL;
    hr = CoInitialize(NULL);
  if (FAILED(hr))
    return NULL;
    hr = ::CLSIDFromProgID(L"DwgPropsX.Properties", &clsid);
  if(FAILED(hr))
    return NULL;
    VERIFY(dwgProp.CreateDispatch(clsid) == TRUE);
    dwgProp.Load(szFileName);
    str = "Drawing Summary Information:\n";
  str = str + (CString)"\nTitle: " +
    (CString)dwgProp.GetTitle();
  str = str + (CString)"\nSubject: " +
    (CString)dwgProp.GetSubject();
  str = str + (CString)"\nAuthor: " +
    (CString)dwgProp.GetAuthor();
  str = str + (CString)"\nComments: " +
    (CString)dwgProp.GetComments();
  str = str + (CString)"\nKeywords: " +
    (CString)dwgProp.GetKeywords();
  str = str + (CString)"\nLast Saved By: " +
    (CString)dwgProp.GetLastSavedBy();
  str = str + (CString)"\nRevision Number: " +
    (CString)dwgProp.GetRevisionNumber();
  str = str + (CString)"\nHyperlink Base: " +
    (CString)dwgProp.GetHyperlinkBase();
  for(int i=0; i<10; i++)
  {
    CString tempStr;
    tempStr.Format("\nCustom %d: %s", i+1,
      (LPCTSTR)dwgProp.GetCustom(i));
    str = str + tempStr;
  }
    DATE date;
  BSTR strDate;
    date = dwgProp.GetEditingTime();
  VarBstrFromDate(date, LOCALE_SYSTEM_DEFAULT,
    LOCALE_NOUSEROVERRIDE, &strDate);
  str = str + (CString)"\nEditing Time: " + (CString)strDate;
    date = dwgProp.GetCreated();
  VarBstrFromDate(date, LOCALE_SYSTEM_DEFAULT,
    LOCALE_NOUSEROVERRIDE, &strDate);
  str = str + (CString)"\nCreated Time: " + (CString)strDate;
    date = dwgProp.GetLastUpdated();
  VarBstrFromDate(date, LOCALE_SYSTEM_DEFAULT,
    LOCALE_NOUSEROVERRIDE, &strDate);
  str = str + (CString)"\nLast Updated Time" + (CString)strDate;
    szSummInfo = (LPTSTR)malloc(str.GetLength()+1);
  _tcscpy(szSummInfo, str.GetBuffer(str.GetLength()));
    CoUninitialize();
    return szSummInfo;
}

## 评论

**内容**: Yan Sid said...
Simple question but I have not been able to find a simple solution.
In windows explorer I can right click on a .dwg file and view, under the "Custom" tab, all of the custom Drawing Properties I've added (in AutoCAD Drawing Utilites -> Drawing Properties). Its great I can copy info from outside autocad with my mouse.
What I really want to do is extract that information, read only, with a vba or powershell script, and send it to a text file with the same name as the drawing. Unfortuantely I do not currently have visual studio and can't compile the above.
How can you, outside autocad, pipe a custom property to a text file? Something like
cmd> customApp A-Test.dwg "custom Title" "target output directory"
Creates A-Test.txt with text "my custom title here"
Reply
06/12/2015 at 11:28 AM

---
**内容**: Augusto Goncalves said in reply to Yan Sid...
Hi Yan Sid
Without Visual Studio you cannot compile this code... sorry. But the same should be available via VBA/VB6 COM Automation, just add DwgProps component.
If you like more features, then try the AutoCAD Console, you can automate it with BAT files and some scripts (.scr files).
Regards,
Augusto Goncalves
Reply
06/12/2015 at 12:50 PM

---
**内容**: Yan Sid said in reply to Augusto Goncalves...
Thanks!
Reply
06/16/2015 at 09:46 AM

---
**内容**: Rodrigo_V said...
I compiled your code in Visual Studio Community. It crashes whenever trying to open a Autocad 2015 file. Is there a package I'm missing? Not too familiar to this blog, I'm guessing your code is built upon assuming you already have another package installed?
Reply
05/03/2016 at 06:00 AM

---
**内容**: Augusto Goncalves said in reply to Rodrigo_V...
Rodrigo, this sample is in C++ (so it doesn't uses packages), but you need to compile it using the COM references. It also should not require you to start AutoCAD (as it uses only the COM API for Dwg Props). Finally the VS Community doesn't include MFC (I believe) that is required for CString (among other Windows features).
Reply
05/03/2016 at 06:06 AM

---
