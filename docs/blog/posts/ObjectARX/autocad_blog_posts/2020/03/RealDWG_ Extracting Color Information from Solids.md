---
title: "RealDWG: Extracting Color Information from Solids"
date: 2020-03-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - DWG
  - Solid
description: "Using RealDWG SDK,  following code extracts the color information of 3d solids in AutoCAD drawings."
author: Autodesk
---
# RealDWG: Extracting Color Information from Solids

发布日期: 2020-03-01

原始链接: https://adndevblog.typepad.com/autocad/2020/03/realdwg-extracting-color-information-from-solids.html

## 文章内容

By Madhukar Moogala
Using RealDWG SDK,  following code extracts the color information of 3d solids in AutoCAD drawings.
To extract color from sub elements of Solid we will use BREP api, you need to refer AcDbMgdBrep.dll module from sdk.
You can use – Testdrawing 
        private void DumpSolid3d(Transaction tr, ObjectId solId)
        {
            using (OpenCloseTransaction oct = new OpenCloseTransaction())
            {
                Solid3d solid = tr.GetObject(solId, OpenMode.ForRead) as Solid3d;

                ObjectId[] ids = new ObjectId[] { solid.ObjectId };

                FullSubentityPath path =
                  new FullSubentityPath(
                    ids,
                    new SubentityId(SubentityType.Null, IntPtr.Zero)
                  );

                // For storing SubentityIds of cylindrical faces

                List subentIds = new List();

                using (Brep brep = new Brep(path))
                {
                    foreach (Autodesk.AutoCAD.BoundaryRepresentation.Face face in brep.Faces)
                    {
                        /*
                        // How to get colors of only cylinderical
                         
                        Autodesk.AutoCAD.Geometry.Surface surf = face.Surface;
                        var ebSurf = surf as Autodesk.AutoCAD.Geometry.ExternalBoundedSurface;
                        if (ebSurf != null && ebSurf.IsCylinder)
                        {
                            subentIds.Add(face.SubentityPath.SubentId);
                        }
                        
                         */
                        subentIds.Add(face.SubentityPath.SubentId);
                    }
                }

                if (subentIds.Count > 0)
                {
                    List> ColorSubEntityPairs
       = GetColors(solid, subentIds);
                    foreach (var item in ColorSubEntityPairs)
                    {
                        var color = item.Key as Color;
                        SubentityId id = item.Value;
                        Console.WriteLine($"\nColor - {color.ColorNameForDisplay}
      | SubEntity Index - {id.IndexPtr}");
                    }
                }
               oct.Commit();
            }
        }

        List< KeyValuePair< Color,SubentityId >> 
 GetColors(Solid3d solid, List subentIds)
        {
            List < KeyValuePair < Color, SubentityId >> ColorSubEntityPairs
  = new List< KeyValuePair >();
            foreach (SubentityId subentId in subentIds)
            {
                try
                {
                    Color col = solid.GetSubentityColor(subentId);
                    ColorSubEntityPairs.Add(new KeyValuePair(col, subentId));
                }
                catch (Autodesk.AutoCAD.BoundaryRepresentation.Exception ex)
                {
                    if(ex.ErrorStatus == ErrorStatus.NotApplicable)
                    continue;
                }
                

                
            }
            return ColorSubEntityPairs;
        }
Output
SolidColors.exe "C:\rd2020\RealDWG 2020\Samples\SolidColors\testBox.dwg"

BlockTable -*Model_Space

Color - 250 | SubEntity Index - 1

Color - 250 | SubEntity Index - 2

Color - 250 | SubEntity Index - 3

Color - 250 | SubEntity Index - 4

Color - 250 | SubEntity Index - 5

Color - 250 | SubEntity Index - 6

Color - 250 | SubEntity Index - 7

Color - 50 | SubEntity Index - 8

Color - 50 | SubEntity Index - 9

Color - 50 | SubEntity Index - 10

Color - 50 | SubEntity Index - 11

Color - 50 | SubEntity Index - 12

Color - 50 | SubEntity Index - 13

BlockTable -*Paper_Space

BlockTable -*Paper_Space0
Source code

## 评论

**内容**: Karley Rath said...
I appreciate your kind words and continued support for my blog. Thank you for regularly reading and engaging with the content. I'm glad to hear that you find geometry dash 23 enjoyable and valuable. If there are any specific topics or areas you'd like me to cover in future blog posts, please feel free to let me know. I'm here to provide helpful and informative content to enhance your experience.
Reply
11/30/2023 at 12:35 AM

---
