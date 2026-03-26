---
title: "AutoCAD 2018: Unexpected Behavior Dealing with wchar_t"
date: 2017-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Plot
  - Unicode
description: "Recently I had a request from an ADN partner troubleshooting a problem with reading values from a text file."
author: Autodesk
---
# AutoCAD 2018: Unexpected Behavior Dealing with wchar_t

发布日期: 2017-07-01

原始链接: https://adndevblog.typepad.com/autocad/2017/07/autocad-2018-unexpected-behavior-dealing-with-wchar_t.html

## 文章内容

By Madhukar Moogala
Recently I had a request from an ADN partner troubleshooting a problem with reading values from a text file.
Assume we have a text file with following contents
Helloworld|Autodesk.
And, user would like to split string with pipe delimitation, so expected output would be
Helloworld and Autodesk.

#define wprintf acutPrintf
void readFile()
{
       const wchar_t  textFile[] = _T("C:\\Temp\\TFile\\helloworld.txt");
       FILE * pFile = NULL;
       wchar_t f1[20], f2[20];
       f1[0] = '\0'; f2[0] = '\0';

       if (_wfopen_s(&pFile, textFile, L"r") != 0 && pFile != NULL)
       {
             wprintf(L"failure opening file %s !\n", textFile);
             return;
       }
       /*
       %[^|] = store everything before '|' in place holder

       */
       while (fwscanf(pFile, L"%[^|]|%s\n", f1, f2) != EOF)
       {
             wprintf(L"I have read f1 as : %s  \n", f1);
             wprintf(L"I have read f2 as : %s  \n", f2);

       }
       fclose(pFile);
}
This gives garbage values in the placeholders, like shown in below pic
The root cause of this problem lies in the preprocess macro define
_CRT_STDIO_ISO_WIDE_SPECIFIERS =1
in ObjectARXSDK 2018\inc\rxsdk_common.props
To tackle issue with Visual Studio 2015, AutoCAD made a workaround, it is not a case anymore unfortunately this define lies in SDK and causing some other issues like I stated above.
You can remove this define from your SDK to avoid unnecessary issues while dealing with strings.

## 评论

**内容**: Alexander Rivilis said...
Hi, Madhukar!
I've checked my ObjectARXSDK 2018\inc\rxsdk_common.props but did not found _CRT_STDIO_ISO_WIDE_SPECIFIERS definition in it. What wrong with my ObjectARX SDK 2018?
Best Regads,
Alexander Rivilis
Reply
07/24/2017 at 01:58 PM

---
**内容**: Madhukar Moogala said...
Hi Alexander,
Is your SDK latest download from website ?.
Possible that correction might have included.
Developers who are having SDK from beta days are finding this issue.
Reply
07/24/2017 at 08:17 PM

---
**内容**: Alexander Rivilis said in reply to Madhukar Moogala...
Yes! I have ObjectARX SDK 2018 from Autodesk website (not beta). File rxsdk_common.props has such line:
_WIN32_IE=0x0600;WIN;WIN32;_CRT_SECURE_CPP_OVERLOAD_STANDARD_NAMES=1;_CRT_SECURE_CPP_OVERLOAD_STANDARD_NAMES_COUNT=1;_AFXDLL;_UNICODE;UNICODE;%(PreprocessorDefinitions)
There is no others preprocessor definitions.
So it is look like best offer - download and install the latest version of the ObjectARX SDK 2018 from Autodesk website: http://usa.autodesk.com/adsk/servlet/item?siteID=123112&id=785550
Reply
07/25/2017 at 03:10 PM

---
**内容**: hurdle said...
It's a wonderful piece. In my opinion, this is one of the best blog posts ever. I admire and am inspired by your work. That's really kind of you.
Reply
04/12/2023 at 01:57 AM

---
