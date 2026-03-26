---
title: "Formats a floating-point value as a string"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - API
  - C++
  - Database
  - ObjectARX
description: "In ObjectARX, you can use acdbRToS API to convert the double values to string value. This API also takes care of converting the string required for..."
author: Autodesk
---
# Formats a floating-point value as a string

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/formats-a-floating-point-value-as-a-string.html

## 文章内容

By Virupaksha Aithal
In ObjectARX, you can use acdbRToS API to convert the double values to string value. This API also takes care of converting the string required format (Decimal/Engineering/Architectural/Fractional) as shown in below code.
void convertDoubleToString()
{
    ACHAR valStr[50];
    //-1 to use current database units
    int unit = -1;
    // 5 is pr
    int prec = 5;
    acdbRToS(15.20024, unit, prec, valStr);
      acutPrintf(_T("double is %s\n"), valStr);
    //for Scientific use 1
    unit = 1;
    acdbRToS(15.20024, unit, prec, valStr);
    acutPrintf(_T("Scientific : %s\n"), valStr);
      //for Decimal  use 2
    unit = 2;
    acdbRToS(15.20024, unit, prec, valStr);
    acutPrintf(_T("Decimal  : %s\n"), valStr);
      //for Engineering   use 3
    unit = 3;
    acdbRToS(15.20024, unit, prec, valStr);
    acutPrintf(_T("Engineering  : %s\n"), valStr);
      //for Architectural use 4
    unit = 4;
    acdbRToS(15.20024, unit, prec, valStr);
    acutPrintf(_T("Architectural  : %s\n"), valStr);
      //for Fractional use 5
    unit = 5;
    acdbRToS(15.20024, unit, prec, valStr);
    acutPrintf(_T("Fractional   : %s\n"), valStr);
}

## 评论

**内容**: TJ said...
does something similiar for the .net API exist?
Reply
04/25/2013 at 02:36 AM

---
**内容**: Viru said in reply to TJ...
Hi,
please use Autodesk.AutoCAD.Runtime.Converter.DistanceToString(), API in .NET
regards
Viru
Reply
04/25/2013 at 04:51 AM

---
**内容**: TJ said in reply to Viru...
Thank you very much!
Reply
04/25/2013 at 07:27 AM

---
**内容**: Scott said...
What is a safe string length to use with acdbRToS()? I notice the sample allocates 50 bytes, but I would like to verify what the upper limit should be, to avoid overruns.
Reply
09/06/2013 at 09:15 AM

---
