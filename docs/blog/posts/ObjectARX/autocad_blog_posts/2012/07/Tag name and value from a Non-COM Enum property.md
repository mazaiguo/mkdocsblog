---
title: "Tag name and value from a Non-COM Enum property"
date: 2012-07-01
categories:
  - AutoCAD COM
tags:
  - COM
  - Plot
  - Plugin
description: "Here is a blog post by my colleague Adam on displaying a list of values for a property using the Non-COM Property system. When the user changes the..."
author: Autodesk
---
# Tag name and value from a Non-COM Enum property

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/here-isa-blog-post-by-my-colleague-adam-on-displaying-a-list-of-values-for-a-property-using-the-non-com-property-system-when.html

## 文章内容

By Balaji Ramamoorthy
Here is a blog post by my colleague Adam on displaying a list of values for a property using the Non-COM Property system. When the user changes the property value in the combo-box, it might be required for the plug-in to know the tag name and value of the selected item in the combo-box. Here is a sample code that retrieves the "AcRxEnumTag" from the "AcRxValue" and displays this information.
void PrintPropertyValue(AcDbEntity *pEntity, ACHAR* pPropertyName)
{
    AcRxMemberIterator * iter
        = AcRxMemberQueryEngine::theEngine()->newMemberIterator(pEntity); 
    if(iter == NULL)
        return;
      AcRxProperty * prop = AcRxProperty::cast(iter->find(pPropertyName));
    if (prop != NULL)
    {
        Acad::ErrorStatus err = Acad::eOk;
        AcRxValue value;
          if ((err = prop->getValue(pEntity, value)) == Acad::eOk)
        {
            // Value type name
            acutPrintf(
                        ACRX_T("\nValue Type Name : %s"),
                        value.type().name()
                      );
              // Value
            ACHAR * szValue = NULL;
            int buffSize = value.toString(NULL, 0);
            if (buffSize > 0)
            {
                buffSize++;
                szValue = new ACHAR[buffSize];
                value.toString(szValue, buffSize);
            }
            acutPrintf (
                        ACRX_T("\nValue : %s"),
                        (szValue == NULL) ? _T("none") : szValue
                       );
            if (szValue)
                delete szValue;
              // Enum Tag name (only for enum properties)
            const MyEnum *val = rxvalue_cast<MyEnum>(&value);
            if (val != NULL)
            {
                const AcRxEnumTag *pEnumTag = value.getEnumTag();
                if(pEnumTag != NULL)
                {
                    acutPrintf(
                                ACRX_T("\nTag : %s"),
                                pEnumTag->name()
                              );
                    // OR
                    /*acutPrintf(
                                ACRX_T("\nTag : %s"),
                                pEnumTag->localName()
                                );*/
                }
            }
        }
        else
        {
            acutPrintf(ACRX_T("Error Code = %d"), err);
        }
    }
    delete iter;
}

