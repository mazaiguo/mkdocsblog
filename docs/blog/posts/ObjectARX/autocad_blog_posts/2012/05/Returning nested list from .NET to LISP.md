---
title: "Returning nested list from .NET to LISP"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoLISP
description: "I tried to create a nested list with the following code but it returned eInvalidResBuf. What's wrong with it?"
author: Autodesk
---
# Returning nested list from .NET to LISP

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/returning-nested-list-from-net-to-lisp.html

## 文章内容

By Adam Nagy
I tried to create a nested list with the following code but it returned eInvalidResBuf. What's wrong with it?
[LispFunction("GetNestedList")]
public static ResultBuffer GetNestedList(ResultBuffer resBufIn)
{
  // main result buffer
  ResultBuffer resBufOut = new ResultBuffer();
    // 5005 = RTSTR
  resBufOut.Add(new TypedValue(5005, "Main List Item 1"));
    // nested result buffer
  ResultBuffer resBufNested = new ResultBuffer();
  resBufNested.Add(new TypedValue(5005, "Nested List Item 1"));
  resBufNested.Add(new TypedValue(5005, "Nested List Item 2"));
    // 5023 = RTRESBUF
  resBufOut.Add(new TypedValue(5023, resBufNested));
    resBufOut.Add(new TypedValue(5005, "Main List Item 2"));
    return resBufOut;
}
Solution
You can find the ResultBuffer TypedValue related codes in the LispDataType enum. As you can see RTRESBUF/5023 is not in the list. You could place the nested part in a LispDataType.ListBegin/LispDataType.ListEnd section instead:
[LispFunction("GetNestedList")]
public static ResultBuffer GetNestedList(ResultBuffer resBufIn)
{
  ResultBuffer resBufOut = new ResultBuffer();
    resBufOut.Add(
    new TypedValue((int)LispDataType.Text, "Main List Item 1"));
    resBufOut.Add(new TypedValue((int)LispDataType.ListBegin));
    resBufOut.Add(
      new TypedValue((int)LispDataType.Text, "Nested List Item 1"));
    resBufOut.Add(
      new TypedValue((int)LispDataType.Text, "Nested List Item 2"));
  resBufOut.Add(new TypedValue((int)LispDataType.ListEnd));
    resBufOut.Add(
    new TypedValue((int)LispDataType.Text, "Main List Item 2"));  
    return resBufOut;
}

