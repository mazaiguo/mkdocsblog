---
title: "Using AutoLISP to read an access database via ADO"
date: 2013-04-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
  - Database
description: "How can you access the data in a database rows using Visual LISP functions ?"
author: Autodesk
---
# Using AutoLISP to read an access database via ADO

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/using-autolisp-to-read-an-access-database-via-ado.html

## 文章内容

By Xiaodong Liang
Issue
How can you access the data in a database rows using Visual LISP functions ?
Solution
Although there are no direct Visual LISP functions to read databases, you can use Microsoft's ActiveX ADO technology from AutoLISP to do this.
The following code illustrates how to read the Customer table from the NorthWind sample database in the Office products using either the Microsoft Access drivers or ODBC.
  (vl-load-com)

(defun ADOreadNorWndDB ( / MDB_File SQLStatement ADO_DLLPath ConnectionObject
aCommandObject supp rsState
          recno RecordSetObject aBOF aEOF fieldsObj reccnt afield i
fvalue coState)

;; You'll Need To Change the Path to the Northwind.mdb file
;;  L:\Program Files\Microsoft Office\Office\Samples 
;;; Set MDB_File to a locatable Access Database file ->
 
(if (setq MDB_File (findfile "c:\\Northwind.mdb"))
    (setq MDB_File "c:\\Northwind")
    (progn
     (princ "\nNorthWind Database was not found, Exiting.")
     (exit)
    )
)
   
;;; Setup a SQL statement ->
 (setq SQLStatement "SELECT * FROM CUSTOMERS")

;;; Normal path to the ADO DLL, change as needed:
(setq ADO_DLLPath "c:\\program files\\common files\\system\\ado\\")

(if (null adom-Append)
 (if (findfile (strcat ADO_DLLPath "msado15.dll"))
   (vlax-import-type-library
     :tlb-filename
     (strcat ADO_DLLPath "msado15.dll")
     :methods-prefix
     "adom-"
     :properties-prefix
     "adop-"
     :constants-prefix
     "adok-"
   )
   (progn
     (alert (strcat "Exiting - Can't find \"" ADO_DLLPath "msado15.dll\""))
     (exit)
   )
 )
)

;;; Proceed if Type Library has been loaded.
 (if adom-Append
   (progn
;;; Create A Connection Object
     (setq ConnectionObject (vlax-create-object "ADODB.Connection"))

;;; Check the mode of the Connection Object
     (setq coMode (vlax-get-property ConnectionObject 'Mode)) ; = 0
;;; Valid Mode values are:
;;;  adok-adModeUnknown = 0
;;;  adok-adModeRead = 1
;;;  adok-adModeWrite = 2
;;;  adok-adModeReadWrite = 3
;;;  adok-adModeShareDenyRead = 4
;;;  adok-adModeShareDenyWrite = 8
;;;  adok-adModeShareExclusive = 12
;;;  adok-adModeShareDenyNone = 16

     (setq coState (vlax-get-property ConnectionObject 'State))

    (if (= coState adok-adStateClosed)
       (vlax-put-property ConnectionObject 'Mode adok-adModeReadWrite)
    )
 
;;; Use the direct Microsoft Access Drivers Creates a LDB Locking file here after this executes
;;;    (vlax-invoke-method
;;;     ConnectionObject
;;;    "Open"
;;;    (strcat "Driver={Microsoft Access Driver (*.mdb)};DBQ="
;;;       MDB_File
;;;    )
;;;    "admin"
;;;    ""
;;;    adok-adConnectUnspecified
;;;    )

;;; Or Use a ODBC Connection, but set it up first ->
  (vlax-invoke-method ConnectionObject
               "Open"
               "DSN=myMDB;"
               "admin"
               ""
               adok-adConnectUnspecified
  )

 
;;; Create the RecordSet Object

    (setq RecordSetObject (vlax-create-object "ADODB.RecordSet"))

;;; Set the CursorType, and Locking Type

    (vlax-put-property RecordSetObject 'CursorType adok-adOpenDynamic)
;;; Where the property values are:
     
;;;    adok-adOpenForwardOnly = 0
;;;    adok-adOpenKeyset = 1
;;;    adok-adOpenDynamic = 2
;;;    adok-adOpenStatic = 3

    (vlax-put-property RecordSetObject 'LockType   adok-adLockOptimistic)
;;; Where the property values are:

;;;  adok-adLockReadOnly = 1
;;;  adok-adLockPessimistic = 2
;;;  adok-adLockOptimistic = 3
;;;  adok-adLockBatchOptimistic = 4

;;; The following code will not work, do not use it.
;(setq RecordSetObject
;;; The following fails with a "Type mismatch" error
;      (vlax-invoke-method
;        ConnectionObject "Execute" SQLStatement 'RecordsAffected
;        adok-adCmdText
;       )
;  )

;;; Create a Command Object and Connect it to the Connection Object
    (setq aCommandObject (vlax-create-object "ADODB.Command"))
    (vlax-put-property aCommandObject 'ActiveConnection ConnectionObject)

;;; Setup the Command Object, and Execute the SQL query
    (vlax-put-property aCommandObject 'CommandText SQLStatement)
    (vlax-put-property aCommandObject 'CommandType adok-adCmdText)
;;; adok-adCmdText = 1
;;; adok-adCmdTable = 2
;;; adok-adCmdTableDirect = 512
;;; adok-adCmdStoredProc = 4
;;; adok-adCmdUnknown = 8
;;; adok-adCommandFile = nil
;;; adok-adExecuteNoRecords = 182
 
    (setq RecordSetObject (vlax-invoke-method aCommandObject "Execute" nil nil
nil))
    (setq supp (vlax-invoke-method RecordSetObject 'Supports adok-adAddNew))

;;; Check to see that the RecordSet is available here ->
    (setq rsState (vlax-get-property RecordSetObject 'State))
;;;   adok-adStateClosed = 0
;;;   adok-adStateOpen = 1
;;;   adok-adStateConnecting = 2
;;;   adok-adStateExecuting = 4
;;;   adok-adStateFetching = 8
 
    (if (= rsState adok-adStateOpen)
      (progn
     (setq recno 0)
     (while (and
          (=
            (setq aBOF (vlax-get-property RecordSetObject 'BOF))
             :vlax-false
            )
          (=
            (setq aEOF (vlax-get-property RecordSetObject 'EOF))
            :vlax-false
          )
        )
        (setq fieldsObj (vlax-get-property RecordSetObject 'Fields))

        (setq reccnt (vlax-get-property fieldsObj 'Count) i 0)
        (princ (strcat "\nRecord " (itoa recno) ":\n"))
        (while (< i reccnt)
           (setq afield (vlax-get-property fieldsObj 'Item i))
           (princ (setq fvalue (vlax-variant-value (vlax-get-property
afield 'Value))))
           (princ "\t")
           (setq i (1+ i))
        )
        (princ "\n")
        (setq recno (1+ recno))
        (vlax-invoke-method RecordSetObject 'MoveNext)
     )
      )
      (princ (strcat "\nRecord Set NOT Available, Record Set State = " (itoa
rsState)))
    )

;;; Close only works if it's Opened !, this can usually be tested by checking if
a LDB file exists.
;;; Check to see that the Connection Object is open here ->
    (setq coState (vlax-get-property ConnectionObject 'State))
    (if (and (findfile (strcat MDB_File ".ldb")) (= coState adok-adStateOpen))
      (vlax-invoke-method ConnectionObject "Close")
      (princ "\nConnection Object is not Open, please delete the LDB file if
needed.")
    )
    (Clean_Up)
   )
;;; Exit if Type Library has NOT been loaded.
   (progn
     (alert (strcat "Exiting - Type Library was Not Loaded: \"" ADO_DLLPath
"msado15.dll\""))
     (exit)
   )
 )
)


(defun Clean_Up ()
 (if (and aField (null (vlax-object-released-p aField)))
      (vlax-release-object aField)
 )
 (if (and fieldsObj (null (vlax-object-released-p fieldsObj)))
      (vlax-release-object fieldsObj)
 )
 (if (and aCommandObject (null (vlax-object-released-p aCommandObject)))
      (vlax-release-object aCommandObject)
 )
 (if (and RecordSetObject (null (vlax-object-released-p RecordSetObject)))
      (vlax-release-object RecordSetObject)
 )
 (if (and ConnectionObject (null (vlax-object-released-p ConnectionObject)))
      (vlax-release-object ConnectionObject)
 )
 (setq ConnectionObject nil RecordSetObject nil aCommandObject nil fieldsObj
nil aField nil)
 (princ "\n\nRemoving and Releasing Connection Objects.")
 (princ)
)

(princ "\nADOreadNorWndDB loaded, type (ADOreadNorWndDB) to run.")
(princ)

## 评论

**内容**: TomFerstein said...
Work with access databases by the use of access file repair
Read it here http://www.access.repairtoolboxx.com/
Reply
10/14/2013 at 04:22 AM

---
**内容**: Admir said...
Hi,
I am looking at a way to link to a database or excel sheet from .net. Is there a way to do this?
Reply
05/12/2016 at 02:23 AM

---
**内容**: Carlos said...
To use stored procedures, how would I add a parameter to the parameters collection of the command object?
Reply
11/14/2024 at 09:48 AM

---
