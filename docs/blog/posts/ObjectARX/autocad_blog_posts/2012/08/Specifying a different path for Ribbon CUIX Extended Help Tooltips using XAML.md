---
title: "Specifying a different path for Ribbon CUIX Extended Help Tooltips using XAML"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - CUI
description: "It’s possible to supply your own XAML Tooltips by supplying a loose WPF XAML file as the ContentSource"
author: Autodesk
---
# Specifying a different path for Ribbon CUIX Extended Help Tooltips using XAML

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/specifying-a-different-path-for-ribbon-cuix-extended-help-tooltips-using-xaml.html

## 文章内容

by Fenton Webb
It’s possible to supply your own XAML Tooltips by supplying a loose WPF XAML file as the ContentSource
e.g.
<Header>
  <FileReferences>
    <ToolTipFileReferences>
      <ContentSources>
        <ContentSource>toolTips.xaml</ContentSource>
      </ContentSources>
    </ToolTipFileReferences>
  </FileReferences>
</Header>
The ContentSource is actually a Uri which means you can use the Uri pack format to specify different paths or even XAML files packaged into your own resource DLLs…
e.g. a DLL Resource locator
<Header>
  <FileReferences>
    <ToolTipFileReferences>
      <ContentSources>
        <ContentSource>pack://application:,,,/MyApplicationDLL;resources/Tooltip.xaml</ContentSource>

      </ContentSources>
    </ToolTipFileReferences>
  </FileReferences>
</Header>

