---
title: "Access to selected entity while displaying ContextualTab"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Database
  - Selection
  - Unicode
description: "The contextual tab selector rule can be associated with a method in a .Net assembly that you can implement. To access the properties of the selecte..."
author: Autodesk
---
# Access to selected entity while displaying ContextualTab

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/access-to-selected-entity-while-displaying-contextualtab.html

## 文章内容

By Balaji Ramamoorthy
The contextual tab selector rule can be associated with a method in a .Net assembly that you can implement. To access the properties of the selected entity from within this dll, it is important NOT to use “Database.TransactionManager.StartTransaction”. Using the regular database transactions can result in weird behavior such as entities that cannot be moved / erased etc.
Instead, use the “IDataItem.StartTransaction” as demonstrated in the following code snippet.
Please note that these transactions also have to be committed and disposed properly just as regular database transactions.
bool PeekSelection(Selection^ sel)
{
    try
    {
        for (Int32 i = 0; i < sel->Count; ++i)
        {
            IDataItem^ item = (IDataItem^)(sel[i]);
              if (!item)
                return false;
              IDataItemTransaction^ trans
                    = item->StartTransaction(OpenMode::ForRead);
            DBObject^ obj = static_cast<DBObject^>(trans->Item);
              if (obj != nullptr)
            {
                // Selected object is now open.
                // Use it find more about it.
            }
              if (trans)
            {
                trans->Commit();
                trans->~IDataItemTransaction();
            }
        }
        return true;
    }
    catch (System::Exception^ e)
    {
      }
    __finally
    {
    }
    return true;
}
Posted at 06:01 PM in .NET, AutoCAD, Balaji Ramamoorthy | Permalink

