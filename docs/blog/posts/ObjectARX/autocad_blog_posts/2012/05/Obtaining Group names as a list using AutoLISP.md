---
title: "Obtaining Group names as a list using AutoLISP"
date: 2012-05-01
categories:
  - AutoLISP
tags:
  - AutoLISP
description: "To obtain all the group names in an AutoLISP list variable, first get the "ACADGROUP" dictionary and then extract all the group names from it."
author: Autodesk
---
# Obtaining Group names as a list using AutoLISP

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/obtaining-group-names-as-a-list-using-autolisp.html

## 文章内容

By Balaji Ramamoorthy
To obtain all the group names in an AutoLISP list variable, first get the "ACAD_GROUP" dictionary and then extract all the group names from it.
Here is a sample code :
(defun GetGroupList ()
    (setq grp (dictsearch (namedobjdict) "ACAD_GROUP"))
    (setq grpList (list))
    (while (/= (assoc 3 grp) nil)
        (setq grpList (cons (cdr (assoc 3 grp)) grpList ))
        (setq grp (cdr (member (assoc 3 grp) grp)))
    )
    grpList
)

