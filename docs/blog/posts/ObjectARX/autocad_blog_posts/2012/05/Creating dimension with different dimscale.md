---
title: "Creating dimension with different dimscale"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Database
  - Dimension
  - ObjectARX
description: "When creating dimensions through ObjectARX, the dimension variables that you need to overide can be passed through Extended Entity Data (xdata). He..."
author: Autodesk
---
# Creating dimension with different dimscale

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/creating-dimension-with-different-dimscale.html

## 文章内容

By Balaji Ramamoorthy
When creating dimensions through ObjectARX, the dimension variables that you need to overide can be passed through Extended Entity Data (xdata). Here is a sample code that creates a dimension with a different scale than the one set using the DIMSCALE system variable.
static void ADSProjectDimScale(void)
{
    AcDbDatabase *pDb
            = acdbHostApplicationServices()->workingDatabase();
    AcDbObjectId dimStyleId = pDb->dimstyle();
      // Create a dimension with a dimscale of  50
    double dimscale = 50.0;
    double rotation = 0.0;
    AcGePoint3d xLine1Point (0, 0, 0),
                xLine2Point (100, 0, 0),
                dimLinePoint (10, 0, 0);
      AcDbRotatedDimension *pDim
                    = new AcDbRotatedDimension (
                                                    0.0,
                                                    xLine1Point,
                                                    xLine2Point,
                                                    dimLinePoint,
                                                    NULL,
                                                    dimStyleId
                                               );
      // Set XData for the dimension.
    // (1001 . "ACAD")
    // (1000 . "DSTYLE")    
    // (1002 . "{")    
    // (1070 . 40)    
    // (1040 . dimscale)    
    // (1002 . "}")
    resbuf *p = acutBuildList(
                                AcDb::kDxfRegAppName, L"ACAD",
                                AcDb::kDxfXdAsciiString, L"DSTYLE",
                                AcDb::kDxfXdControlString, L"{",
                                AcDb::kDxfXdInteger16, 40,
                                AcDb::kDxfXdReal, dimscale,
                                AcDb::kDxfXdControlString, L"}",
                                0
                             );
    pDim->setXData (p) ;
    acutRelRb(p) ;
      AcDbBlockTableRecordPointer pBTR
                    (
                        acdbSymUtil()->blockModelSpaceId(pDb),
                        AcDb::kForWrite
                    );
      pBTR->appendAcDbEntity(pDim);
      pBTR->close() ;
    pDim->close () ;
}

## 评论

**内容**: Oleg said...
Hi Balaji,
Can you check this code?
[CommandMethod("cdim")]
public static void ADSProjectDimScale()
{
Database db = HostApplicationServices.WorkingDatabase;
ObjectId dimStyleId = db.Dimstyle;
using (Transaction tr = db.TransactionManager.StartTransaction())
{
// Create a dimension with a dimscale of 50
double dimscale = 50.0;
double rotation = 0.0;
Point3d xLine1Point = new Point3d(0, 0, 0);
Point3d xLine2Point = new Point3d(1000, 0, 0);
Point3d dimLinePoint = new Point3d(500, 100, 0);
RotatedDimension dim = new RotatedDimension(rotation, xLine1Point, xLine2Point, dimLinePoint, null, dimStyleId);
try
{
// Set XData for the dimension.
// (1001 . "ACAD")
// (1000 . "DSTYLE")
// (1002 . "{")
// (1070 . 40)
// (1040 . dimscale)
// (1002 . "}")
//dim.XData = new ResultBuffer(new TypedValue(1001, "ACAD"),
// new TypedValue(1000, "DSTYLE"),
// new TypedValue(1002, "{"),
// new TypedValue(1070, 40),
// new TypedValue(1040, dimscale),
// new TypedValue(1002, "}"));
// The same as:
dim.XData = new ResultBuffer(
new TypedValue((int)DxfCode.ExtendedDataRegAppName, "ACAD"),
new TypedValue((int)DxfCode.ExtendedDataAsciiString, "DSTYLE"),
new TypedValue((int)DxfCode.ExtendedDataControlString, "{"),
new TypedValue((int)DxfCode.ExtendedDataInteger16, 40),
new TypedValue((int)DxfCode.ExtendedDataReal, dimscale),
new TypedValue((int)DxfCode.ExtendedDataControlString, "}")
);

BlockTableRecord btr = tr.GetObject(db.CurrentSpaceId, OpenMode.ForWrite) as BlockTableRecord;
btr.AppendEntity(dim);
tr.AddNewlyCreatedDBObject(dim, true);
tr.Commit();
}
catch (System.Exception ex)
{
Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage(ex.Message);
}
}
}
Thanks,
Oleg
Reply
05/18/2012 at 11:26 PM

---
**内容**: Balaji said...
Hi Oleg,
I dont see any problem with the .Net code that you shared. May I know the issue that you are having with it ?
Instead of the fixed value for dimscale, you can a value that can be input at runtime. This will help you try with different values and see the difference.
For ex :
PromptDoubleResult pdr = ed.GetDouble(new PromptDoubleOptions("Enter a dimscale"));
if (pdr.Status != PromptStatus.OK)
return;
double dimscale = pdr.Value;
Now, you can try with 50, 100, 200 etc for the dim scales.
If this does not help, please let me know the AutoCAD version that you trying it with and any other info that can help reproduce the same issue at my end.
Thanks
Balaji
Reply
05/20/2012 at 07:42 AM

---
**内容**: Oleg said in reply to Balaji...
Thanks so much Balaji,
I like your codes, especially if these are in
two parts: C+/C#,
this is very useful for me
Regards,
Oleg
Reply
05/20/2012 at 08:26 AM

---
**内容**: Balaji said...
Hi Oleg,
I include C++ and C# codes in most of the posts. This one was an exception. I will try to include both wherever relevant in future posts.
Thanks for your suggestion.
Balaji
Reply
05/20/2012 at 09:54 AM

---
