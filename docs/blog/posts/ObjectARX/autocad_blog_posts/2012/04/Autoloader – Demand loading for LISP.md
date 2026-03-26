---
title: "Autoloader – Demand loading for LISP"
date: 2012-04-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - Plugin
description: "I think this is the last AutoCAD 2013 Autoloader enhancement to document now. Its more of an incremental enhancement than the others …"
author: Autodesk
---
# Autoloader – Demand loading for LISP

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/autoloader-demand-loading-for-lisp.html

## 文章内容

By Stephen Preston
I think this is the last AutoCAD 2013 Autoloader enhancement to document now. Its more of an incremental enhancement than the others …
We strongly recommend that you set your plug-ins to load on demand (usually LoadOnCommandInvocation), rather than on startup. This is so a customer who has installed lots of plug-ins doesn’t see a huge slowdown in AutoCAD startup times. That wasn’t so easy for LISP apps – until now. Here’s an example of how you set a LISP module to load on command invocation:
    <!-- LISP demand loading example -->  
    <ComponentEntry AppName="ADN_MINESWEEPER" ModuleName="./Contents/Windows/mylisp.lsp" LoadOnCommandInvocation="True">
      <Commands GroupName="ADN_MINESWEEPER">
        <Command Local="TEST" Global="TEST" Description="Simple LISP demand loading example" />
      </Commands>
    </ComponentEntry>
Which is exactly the same as you’d do it for ObjectARX or .NET.
What further Autoloader enhancements would you be interested in? Post a  comment to let us know.

## 评论

**内容**: Maxence DELANNOY said...
Make a version for older versions of AutoCAD!
Reply
04/26/2012 at 11:57 PM

---
**内容**: drg said...
I would like to have the capability to define variables, and vary default values based on the running version and/or running vertical.
Something like...
[CustomVariables]
--[Variable Name="MyDrawingVariable" Storage="Drawing" Type="String" DefaultValue="AutoCAD r%SERIES% Default"]
----[DefaultValueAlternate Platform="AutoCAD MEP" SeriesMin="19.0" Value="AutoCAD MEP 2013+ Default"/]
--[/Variable]
--[Variable Name="MyProfileVariable" Storage="Profile" Type="Integer" Min="0" Max="100" DefaultValue="50"]
[/CustomVariables]
Reply
05/03/2012 at 10:49 AM

---
