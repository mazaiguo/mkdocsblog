---
title: "Find all available OLEDB data providers supported by ASI in AutoCAD"
date: 2013-03-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
description: "How can I discover what tables are available AutoLISP?"
author: Autodesk
---
# Find all available OLEDB data providers supported by ASI in AutoCAD

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/find-all-available-oledb-data-providers-supported-by-asi-in-autocad.html

## 文章内容

By Xiaodong Liang
Issue
How can I discover what tables are available AutoLISP?
Solution
There are two ASILISP functions that help here. Both return cursors to system tables so you can step through the records to find what you need. For example, this code will return all the available providers:

(defun c:getprov ( / fasi_kword fasi_curs fasi_row)
  ;;; Note that ASILISP *must* be loaded first.
  (verify_arxapp_loaded "asilisp") 
(setq fasi_curs (asi_providers))
(if (asi_open fasi_curs)
   (prompt "\nasi_open successful.")
   (prompt "\nasi_open failed!")
)
(print fasi_curs)
(while (/= fasi_kword "eXit")
 (initget 1 "First Last Next Prior eXit")
 (setq fasi_kword (getkword "\nDisplay Row: (First Last Next Prior eXit)"))
 (if (/= fasi_kword "eXit")
     (progn (setq fasi_row (asi_fetch fasi_curs fasi_kword))
         (if fasi_row (print fasi_row)
            (prompt "\nNothing to fetch or asi_fetch failed.")
         )
      )
 )
)
(if (asi_close fasi_curs)
   (prompt "\nasi_close successful.")
   (prompt "\nasi_close failed!")
)
(princ)
)
Typical results after stepping through the table (using the 'next' option above) might be:
("SQLOLEDB"
"{0C7FF16C-38E3-11d0-97AB-00C04FC2AD98}"
"Microsoft OLE DB Provider for SQL Server" 1.0 0.0
"{0C7FF16C-38E3-11d0-97AB-00C04FC2AD98}")
 
("MSDataShape"
"{3449A1C8-C56C-11D0-AD72-00C04FC29863}"
"MSDataShape" 1.0 0.0
"{3449A1C8-C56C-11D0-AD72-00C04FC29863}")
("SQLNCLI11"
"{397C2819-8272-4532-AD3A-FB5E43BEAA39}"
"SQL Server Native Client 11.0" 1.0 0.0
"{397C2819-8272-4532-AD3A-FB5E43BEAA39}")
("SQLNCLI Enumerator"
"{4898AD37-FE05-42df-92F9-E857DDFEE730}"
"SQL Native Client Enumerator" 2.0 0.0
"{4898AD37-FE05-42df-92F9-E857DDFEE730}")
… …. etc

