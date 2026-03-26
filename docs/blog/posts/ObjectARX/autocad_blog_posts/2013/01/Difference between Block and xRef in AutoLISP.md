---
title: "Difference between Block and xRef in AutoLISP"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Block
  - XREF
description: "After you know the name of the block, For example:"
author: Autodesk
---
# Difference between Block and xRef in AutoLISP

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/difference-between-block-and-xref-in-autolisp.html

## 文章内容

By Augusto Goncalves
After you know the name of the block, For example:
(setq blkname (cdr (assoc 2 (entget (car (entsel))))))
you can pass it into (tblsearch), get the details of the block table record (whether for a normal block or an xref) using:
(tblsearch "BLOCK" blkname)
This returns information from the block table, including the path of the xref (if applicable). The 70 group code differentiates blocks from xrefs, and the 1 group code gives you the path information.

