---
title: "How to check if a given string is a valid name for an item in a symbol table?"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Block
  - C++
description: "I want to check if a string provided by the user is suitable for a block name or for a layer name. Is there any function that can validate the string?"
author: Autodesk
---
# How to check if a given string is a valid name for an item in a symbol table?

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/how-to-check-if-a-given-string-is-a-valid-name-for-an-item-in-a-symbol-table.html

## 文章内容

By Marat Mirgaleev
Issue
I want to check if a string provided by the user is suitable for a block name or for a layer name. Is there any function that can validate the string?
Solution
You are right, not every name is acceptable, for example, for a block. When creating a block in the AutoCAD UI, the user can get the following error message:
As you may know, there is a number of Symbol Tables in an dwg file, like Block table, Linetype table etc.
To check if a given string is a valid symbol table name or not, in ObjectARX you can use acdbSNValid() function.
AutoCAD .NET API provides the SymbolUtilityServices.ValidateSymbolName() for the same purpose. The method throws an exception when the name is invalid. Here is an example:
string[] names = { "lk3j4!@ #`$>%", // will cause an exception
                   "lk3j4!@ #$%" }; // will work fine
foreach (string s in names)
{
  try
  {
    // Validate the provided symbol table name
    SymbolUtilityServices.ValidateSymbolName( s, false);
      System.Windows.Forms.MessageBox.Show( s + " is a valid name." );
  }
  catch
  {
    // An exception has been thrown, indicating that
    //    the name is invalid
    System.Windows.Forms.MessageBox.Show( s +" is an invalid name.");
  }
} // foreach
The 2nd parameter of the ValidateSymbolName() is a flag that allows or disallows the '|' symbol (so called "pipe" symbol).

## 评论

**内容**: Andrey said...
>The method throws an exception when the name is invalid.
And for this reason it is better not to use this method because the exception essentially influences productivity.
It is better to use the regular expressions, because it will allow not only to check a line on existence of inadmissible characters, but also to check a name for the rule of name building (if the company approved such rules).
Reply
08/27/2012 at 02:15 AM

---
**内容**: Geburtstag Einladung said...
ku berntanti dan kubernyanyi lagu tentang cerita asma ra kira
Reply
02/08/2017 at 07:36 AM

---
