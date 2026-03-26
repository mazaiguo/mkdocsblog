---
title: "Explaining the ObjectARX CDocData class"
date: 2012-04-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Plot
description: "If you are new to ObjectARX or have never seen it, the CDocData class may appear a little confusing to some. We use this class in some of our Objec..."
author: Autodesk
---
# Explaining the ObjectARX CDocData class

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/please-explain-objectarx-cdocdata-class.html

## 文章内容

By Fenton Webb
If you are new to ObjectARX or have never seen it, the CDocData class may appear a little confusing to some. We use this class in some of our ObjectARX sample code to handle document specific data.
What is document specific data? The best way to explain it is to show you some code and the results of running the code…
First, lets input an integer and have a static variable that offers a default value…
static int defaultValue = 0;
void myCmd()
{
  TCHAR printBuffer[256];
  _stprintf(printBuffer, _T("\nEnter value <%d> : "), defaultValue);
  acedGetInt(printBuffer, &defaultValue);
}
If you load this code into AutoCAD and run it, it will first offer a default value of 0, and then offer any value you type in as the following default. If you create a new drawing, that default value is shown for each drawing.
Now to create some document specific data…
class CDocData {
public:
  CDocData ()
  {
    defaultValue = 0;
  };
  CDocData (const CDocData &data)
  {
    defaultValue = data.defaultValue;
  }
  ~CDocData () ;
    int defaultValue;
} ;
  AcApDataManager<CDocData> DocVars ;
void myCmd()
{
  TCHAR printBuffer[256];
  _stprintf(printBuffer, _T("\nEnter value <%d> : "), DocVars.docData().defaultValue);
  acedGetInt(printBuffer, &DocVars.docData().defaultValue);
}
  If you load this code into AutoCAD and run it, it will first offer a default value of 0, and then offer any value you type in as the following default. However, this time, if you create a new drawing, you will be offered a 0 default and any value that you type in will be stored separately to any other document. Pretty cool.
As you can see this data is not persisted, and my example is very basic – where would this class really become useful? The answer is for document specific reactors, here’s an example..
class CDocData
{
public:
  CDocData();
  CDocData(const CDocData &data) ;
  ~CDocData();
    asdkMyDatabaseReactor* m_pasdkMyDatabaseReactor;
};
//
// Implementation of the document data class.
//
CDocData::CDocData()
{
  m_pasdkMyDatabaseReactor = NULL;
}
  CDocData::CDocData(const CDocData &data)
{
  m_pasdkMyDatabaseReactor = NULL;
}
  CDocData::~CDocData()
{
  if (m_pasdkMyDatabaseReactor) delete m_pasdkMyDatabaseReactor;
}
//
// setting up the reactor – now it is contained by the document data, don’t need to worry about it anymore
//
DocVars
.docData().m_pasdkMyDatabaseReactor = new asdkMyDatabaseReactor();
cuDoc()->database()->addReactor(DocVars.docData().m_pasdkMyDatabaseReactor);

## 评论

**内容**: Dan said...
There doesn't seem to be much info around on using this.
Can you use a specific specialisation class, so that my DataManager is also my DocManagerReactor?
i.e. can I declare my DocManager class like this:
class MyDocDataManager : public AcApDataManager
Reply
07/28/2014 at 06:46 PM

---
**内容**: Dan said...
Try again, with escaping!
There doesn't seem to be much info around on using this.
Can you use a specific specialisation class, so that my DataManager is also my DocManagerReactor?
i.e. can I declare my DocManager class like this:
class MyDocDataManager : public AcApDataManager<MyDocData>
Reply
07/28/2014 at 06:49 PM

---
