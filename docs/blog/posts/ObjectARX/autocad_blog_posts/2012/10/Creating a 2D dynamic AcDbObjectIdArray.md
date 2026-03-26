---
title: "Creating a 2D dynamic AcDbObjectIdArray"
date: 2012-10-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Dimension
  - ObjectARX
description: "I need to use a 2 dimensional array in my program. I would like to know if it's possible using a dynamic array (like AcDbIntArray, AcDbObjectIdArra..."
author: Autodesk
---
# Creating a 2D dynamic AcDbObjectIdArray

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/creating-a-2d-dynamic-acdbobjectidarray.html

## 文章内容

By Balaji Ramamoorthy
Issue
I need to use a 2 dimensional array in my program. I would like to know if it's possible using a dynamic array (like AcDbIntArray, AcDbObjectIdArray, ...) in 2 dimensions. How can I do this ? In C++ I can use array[][]...and in ObjectARX ? I'll need an array with 3 lines and x (dynamic) columns : [3][x]
Solution
If you had two static dimensions, then of course you could simulate the use of a 2D array with a linear array. As you have one static dimension (3), you can create a static array of AcDbObjectIDArrays (for example), which are of course dynamic. Here is some code which creates an array of IMAX x JMAX, though JMAX could be variable for each sub-array. I have populated the array with IDs from entities the user must select, and then you can see how it is simple to use the typical syntax idArray[i][j] to access the contents of the array.
#define IMAX 2
#define JMAX 3
  static void AdskTestCommand(void)
{
    AcDbEntity *pEnt = NULL;
    AcDbObjectId entId;
    AcGePoint3d pick;
      AcDbObjectIdArray idArray[IMAX];
      int i, j;
    for ( i = 0; i < IMAX; i++ )
    {
        idArray[i].setPhysicalLength( JMAX );
        for ( j = 0; j < JMAX; j++ )
        {
            pEnt = SelectEntity
                    (
                        ACRX_T("\nSelect entity: "),
                        entId,
                        pick,
                        AcDb::kForRead
                    );
            if ( NULL == pEnt)
                entId = AcDbObjectId::kNull;
            else
                pEnt->close();
              idArray[i].insertAt( j, entId );
            acutPrintf
                (
                    ACRX_T("\nObjectID %d inserted at [%d][%d]"),
                    entId,
                    i,
                    j
                );
        }
    }
      for ( i = 0; i < IMAX; i++ )
    {
        for ( j = 0; j < JMAX; j++ )
        {
            acutPrintf
                (
                    ACRX_T("\nObjectID at [%d][%d] is %d"),
                    i,
                    j,
                    idArray[i][j]
                );
        }
    }
}
  static AcDbEntity * SelectEntity
                            (
                                 const ACHAR *prompt,
                                 AcDbObjectId& id,
                                 AcGePoint3d& pick,
                                 AcDb::OpenMode openMode
                            )
{
    AcDbEntity *ent = NULL;
    ads_name ename;
      if ( RTNORM == acedEntSel(prompt, ename, (ads_real*)&pick ))
    {
        if ( Acad::eOk == acdbGetObjectId( id, ename ))
        {
            if ( Acad::eOk == acdbOpenAcDbEntity( ent, id, openMode ))
                return ent;
        }
    }
    return ent;
}

