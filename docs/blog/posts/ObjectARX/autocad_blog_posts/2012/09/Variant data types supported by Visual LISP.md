---
title: "Variant data types supported by Visual LISP"
date: 2012-09-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
description: "Although there are many different variant data types available in ActiveX, Visual LISP does not use all of them. What variant data types are suppor..."
author: Autodesk
---
# Variant data types supported by Visual LISP

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/variant-data-types-supported-by-visual-lisp.html

## 文章内容

By Xiaodong Liang
Issue
Although there are many different variant data types available in ActiveX, Visual LISP does not use all of them. What variant data types are supported by Visual LISP?
Solution
The following code demonstrates the different data types and constants available to Visual LISP. Please note that to convert between actual values and variants, the following functions are used:
(vlax-make-variant [value] [type])
(vlax-variant-change-type var type)
(vlax-variant-type var)
(vlax-variant-value var)
For more information on converting the data types, see DevNote #53397 and the product documentation.
(defun VariantValues ()
  (if (car (atoms-family 1 '("vl-load-com"))) (vl-load-com))
  (princ "\nConstant ActiveX Variant Values Available to Lisp:")
  (SupportedVarType 'vlax-vbEmpty)           ;0
  (SupportedVarType 'vlax-vbNull)           ;1
  (SupportedVarType 'vlax-vbInteger)           ;2
  (SupportedVarType 'vlax-vbLong)           ;3
  (SupportedVarType 'vlax-vbSingle)           ;4
  (SupportedVarType 'vlax-vbDouble)           ;5
  (SupportedVarType 'vlax-vbString)           ;8
  (SupportedVarType 'vlax-vbObject)           ;9
  (SupportedVarType 'vlax-vbBoolean)           ;11
  (SupportedVarType 'vlax-vbArray)           ;8192
  (SupportedVarType 'vlax-vbCurrency)           ;6
  (SupportedVarType 'vlax-vbDate)           ;7
  (SupportedVarType 'vlax-vbError)           ;10
  (SupportedVarType 'vlax-vbVariant)           ;12
  (SupportedVarType 'vlax-vbDataObject)       ;13
  (SupportedVarType 'vlax-vbDecimal)           ;14 
  (SupportedVarType 'vlax-vbByte)           ;17
  (SupportedVarType 'vlax-vbUserDefinedType)  ;18
(princ)
)

(defun SupportedVarType (varTsym / msg )

   (setq msg "")
   (setq varT (eval varTsym))
   (setq msg (strcat "\n" (vl-princ-to-string varTsym)  " = "))
   (setq msg (AddSpaces msg 25))
 
   (if (null varT)
     (setq msg (strcat msg "nil    - UnSupported Data Type"))
     (progn
        (setq msg (strcat msg (vl-princ-to-string varT)))
        (setq msg (AddSpaces msg 33))
        (cond
           ((= varT vlax-vbBoolean)
          (setq msg (strcat msg "- Supported Data Type = SYM"))
           )
           ((or (= varT vlax-vbInteger)(= varT vlax-vbLong))
          (setq msg (strcat msg "- Supported Data Type = INTEGER"))
           )
           ((or (= varT vlax-vbDouble) (= varT vlax-vbSingle))
          (setq msg (strcat msg "- Supported Data Type = REAL"))
           )
           ((= varT vlax-vbString)
          (setq msg (strcat msg "- Supported Data Type = STRING"))
           )
           ((= varT vlax-vbObject)
          (setq msg (strcat msg "- Supported Data Type = VLA-OBJECT"))
           )
           ((= varT vlax-vbArray)
          (setq msg (strcat msg "- Supported Data Type = SAFEARRAY"))
           )
           ((= varT vlax-vbVariant)
          (setq msg (strcat msg "- Supported Data Type = VARIANT"))
           )
           ((= varT vlax-vbDataObject)
          (setq msg (strcat msg "- UnSupported Data Type"))
           )
           (T
          (setq msg (strcat msg "- UnSupported Data Type"))
           )
        )
     )
  )
 
  (princ msg)
  (princ)
)

(defun AddSpaces (aStr aLen / newStr)
  (setq newStr aStr)
  (repeat aLen 
     (setq newStr (strcat newStr " "))
  )
  (setq newStr (substr newStr 1 aLen))
)

(princ "\nVariantValues loaded, type (VariantValues) to run.")
(princ)
Run the code in AutoCAD 2013, the result is:
Command: (VariantValues)
Constant ActiveX Variant Values Available to Lisp:
vlax-vbEmpty =          0       - UnSupported Data Type
vlax-vbNull =           1       - UnSupported Data Type
vlax-vbInteger =        2       - Supported Data Type = INTEGER
vlax-vbLong =           3       - Supported Data Type = INTEGER
vlax-vbSingle =         4       - Supported Data Type = REAL
vlax-vbDouble =         5       - Supported Data Type = REAL
vlax-vbString =         8       - Supported Data Type = STRING
vlax-vbObject =         9       - Supported Data Type = VLA-OBJECT
vlax-vbBoolean =        11      - Supported Data Type = SYM
vlax-vbArray =          8192    - Supported Data Type = SAFEARRAY
vlax-vbCurrency =       6       - UnSupported Data Type
vlax-vbDate =           7       - UnSupported Data Type
vlax-vbError =          10      - UnSupported Data Type
vlax-vbVariant =        12      - Supported Data Type = VARIANT
vlax-vbDataObject =     13      - UnSupported Data Type
VLAX-VBDECIMAL =        nil    - UnSupported Data Type
VLAX-VBBYTE =           nil    - UnSupported Data Type
VLAX-VBUSERDEFINEDTYPE =nil    - UnSupported Data Type

## 评论

**内容**: ekko said...
Hello, please tell me how I need to use the constant vlax-vbByte corresponding to vlax-make-safearray 17, but vlax-vbByte is invalid in CAD. So how can I create the data type of vlax-make-safearray 17?
Reply
09/25/2023 at 11:22 PM

---
