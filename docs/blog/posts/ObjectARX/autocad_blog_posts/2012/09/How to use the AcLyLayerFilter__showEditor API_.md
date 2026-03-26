---
title: "How to use the AcLyLayerFilter::showEditor API?"
date: 2012-09-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - Layer
  - ObjectARX
description: "I am trying to call from my own arx application the "AcLyLayerFilter::showEditor" method in order to display the native AutoCAD layer filter editor..."
author: Autodesk
---
# How to use the AcLyLayerFilter::showEditor API?

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/how-to-use-the-aclylayerfiltershoweditor-api.html

## 文章内容

By Philippe Leefsma
Q:
I am trying to call from my own arx application the "AcLyLayerFilter::showEditor" method in order to display the native AutoCAD layer filter editor, but it doesn't seem to work, nothing is displayed.
A:
Unfortunately displaying this native dialog from API is not possible. The purpose of this method is to be called by AutoCAD itself on a custom filter that would derive from AcLyLayerFilter. Depending on the return type that you define in your overriden showEditor method you can display your own filter editor dialog or the native one, when the user is double clicking or invoking this editor on the custom filter.
The attached sample illustrates this behavior. To test it run command "MyCommand1": it will add a new custom layer filter called "CustomFilter". When you invoke the properties editor on this filter, the overriden showEditor method will be called.
Below is the code of the command method. It shows how to insert the custom filter in the filter list:
static void asdkArxProject1_MyCommand1(void)
{
    AcLyLayerFilterManager* pFilterMgr =
        aclyGetLayerFilterManager(acdbCurDwg());
      if (!pFilterMgr)
    {
        acutPrintf(L"\nUnable to get Layer Filter Manager...");
        return;
    }
      Acad::ErrorStatus es;
      AcLyLayerFilter* pRoot;
    AcLyLayerFilter* pCurrent;
      es = pFilterMgr->getFilters(pRoot, pCurrent);
      //create our custom layer filter
    asdkCustomFilter* pNew = new asdkCustomFilter();
      //set filter properties
    es = pNew->setName(L"CustomFilter");
    es = pNew->setFilterExpression(L"NAME==\"*lay*\" AND COLOR==\"10\"");
      if( pRoot->allowNested() == true)
    {
        //add our filter to the root as nested
        es = pRoot->addNested(pNew);
        es = pFilterMgr->setFilters(pRoot, pNew);
    }
}
  _ArxLayerFilter.zip

