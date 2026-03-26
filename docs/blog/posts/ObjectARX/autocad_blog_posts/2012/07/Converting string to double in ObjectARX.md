---
title: "Converting string to double in ObjectARX"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - API
  - C++
  - Database
  - ObjectARX
description: "In ObjectARX, you can use acdbDisToF API to convert the string value to a double value. This API also takes different format string input (Decimal/..."
author: Autodesk
---
# Converting string to double in ObjectARX

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/converting-string-to-double-in-objectarx.html

## 文章内容

By Virupaksha Aithal
In ObjectARX, you can use acdbDisToF API to convert the string value to a double value. This API also takes different format string input (Decimal/Engineering/Architectural/Fractional) as shown in below code and converts the string to double value.
void convertStringToDouble()
{
    //-1 to use current database units
    int unit = -1;
    // 5 is pr
    double value = 0;
    acdbDisToF(_T("15.0"), unit, &value);
    acutPrintf(_T("double is %f\n"), value);
    //for Scientific use 1
    unit = 1;
    acdbDisToF(_T("1.5000000000E+01"), unit, &value);
    acutPrintf(_T("Scientific : %f\n"), value);
      //for Decimal  use 2
    unit = 2;
    acdbDisToF(_T("15.0000000000"), unit, &value);
    acutPrintf(_T("Decimal  : %f\n"), value);
      //for Engineering   use 3
    unit = 3;
    acdbDisToF(_T("1'-3.0000000000\""), unit, &value);
    acutPrintf(_T("Engineering  : %f\n"), value);
      //for Architectural use 4
    unit = 4;
    acdbDisToF(_T("1'-3\""), unit, &value);
    acutPrintf(_T("Architectural  : %f\n"), value);
      //for Fractional use 5
    unit = 5;
    acdbDisToF(_T("15"), unit, &value);
    acutPrintf(_T("Fractional   : %f\n"), value);
}

## 评论

**内容**: Dhananjay Dixit said...
int unit = -1;
double value = 0;
acdbDisToF(_T("304.80"), unit, &value);
gives me value = 304.80000000000001
I am expecting it to be 304.8
Is this correct?
Reply
05/05/2014 at 12:00 AM

---
**内容**: electrical and infromation said...
very educative blog
Reply
01/30/2017 at 10:15 PM

---
