---
title: "Linking attributes and table using DataExtraction API"
date: 2013-04-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Block
  - DWG
  - Unicode
description: "The "EATTEXT" command in AutoCAD can extract data such as attribute text and display it inside a table. Here is a sample code to do it programmatic..."
author: Autodesk
---
# Linking attributes and table using DataExtraction API

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/linking-attributes-and-table-using-dataextraction-api.html

## 文章内容

By Balaji Ramamoorthy
The "EATTEXT" command in AutoCAD can extract data such as attribute text and display it inside a table. Here is a sample code to do it programmatically using the DataExtraction API and to create a table that links with the data.
To try this,
1) Copy the attached "MyBlock.dwg" to "C:\Temp" folder.
2) Start AutoCAD and open the drawing
3) Run the command and select a point when prompted for the insertion point of the table.
4) Change the attribute values to a different value
5) Right-click on the table and select "Update Table Data Links" option to refresh the values.
// Add the AcDx.dll reference from the inc folder
using Autodesk.AutoCAD.DataExtraction;
  Document doc = Application.DocumentManager.MdiActiveDocument;
Editor ed = doc.Editor;
Database db = doc.Database;
  // Copy the attached "MyBlock.dwg" to C:\Temp for testing
// The Dxe file will be created at runtime in C:\Temp if not found
const string dxePath = @"C:\Temp\MyData.dxe";
const string dwgFolder = @"C:\Temp\";
const string dwgName = "MyBlock.dwg";
  if (System.IO.File.Exists(dxePath) == false)
{
    // Create the DXE file with the information that we want to extract
    DxExtractionSettings setting = new DxExtractionSettings();
      IDxFileReference dxFileReference
        = new DxFileReference(dwgFolder, dwgFolder + dwgName);
      setting.DrawingDataExtractor.Settings.DrawingList.AddFile
                                            (dxFileReference);
      setting.DrawingDataExtractor.DiscoverTypesAndProperties
                                        (dwgFolder + dwgName);
      List<IDxTypeDescriptor> types
        = setting.DrawingDataExtractor.DiscoveredTypesAndProperties;
      List<string> selectedTypes = new List<string>();
    List<string> selectedProps = new List<string>();
    foreach (IDxTypeDescriptor td in types)
    {
        if (td.GlobalName.Equals("BlockReferenceTypeDescriptor.Test"))
            selectedTypes.Add(td.GlobalName);
          foreach (IDxPropertyDescriptor pd in td.Properties)
        {
            if (pd.GlobalName.Equals("AcDxObjectTypeGlobalName") ||
                pd.GlobalName.Equals("AcDxObjectTypeName") ||
                pd.GlobalName.Equals("BlockReferenceAttribute.NAME") ||
                pd.GlobalName.Equals("BlockReferenceAttribute.PLACE"))
            {
                if (!selectedProps.Contains(pd.GlobalName))
                    selectedProps.Add(pd.GlobalName);
            }
        }
    }
      setting.DrawingDataExtractor.Settings.ExtractFlags
                    = ExtractFlags.Nested | ExtractFlags.Xref;
      setting.DrawingDataExtractor.Settings.SetSelectedTypesAndProperties
                        (types, selectedTypes, selectedProps);
      setting.OutputSettings.DataCellStyle = "Data";
    setting.OutputSettings.FileOutputType = AdoOutput.OutputType.xml;
    setting.OutputSettings.HeaderCellStyle = "Header";
    setting.OutputSettings.ManuallySetupTable = true;
    setting.OutputSettings.OuputFlags = DxOuputFlags.Table;
    setting.OutputSettings.TableStyleId = db.Tablestyle;
    setting.OutputSettings.TableStyleName = "Standard";
    setting.OutputSettings.TitleCellStyle = "Title";
    setting.OutputSettings.UsePropertyNameAsColumnHeader = false;
      setting.Save(dxePath);
}
  //Create a DataLink
ObjectId dlId = ObjectId.Null;
DataLinkManager dlm = db.DataLinkManager;
using (DataLink dl = new DataLink())
{
    String dataLinkName = "MyDataLink2";
    dlId = dlm.GetDataLink(dataLinkName);
      if(dlId.IsNull)
    {
        // create a datalink
        dl.ConnectionString = dxePath;
        dl.ToolTip = "My Data Link";
        dl.Name = dataLinkName;
          DataAdapter da
            = DataAdapterManager.GetDataAdapter
            ("Autodesk.AutoCAD.DataExtraction.DxDataLinkAdapter");
          if (da != null)
            dl.DataAdapterId = da.DataAdapterId;
        dlId = dlm.AddDataLink(dl);
    }
}
  // Ask for the table insertion point
PromptPointResult pr = ed.GetPoint("\nEnter table insertion point: ");
if (pr.Status != PromptStatus.OK)
    return;
  // Create a table
ObjectId tableId = ObjectId.Null;
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    Table table = new Table();
      // 2 rows and 4 columns
    table.SetSize(2, 4);
      table.Position = pr.Value;
      //Add the Table to the drawing database
    BlockTable bt = tr.GetObject(
                                    db.BlockTableId,
                                    OpenMode.ForWrite
                                ) as BlockTable;
      BlockTableRecord btr = tr.GetObject
                            (
                                bt[BlockTableRecord.ModelSpace],
                                OpenMode.ForWrite
                            ) as BlockTableRecord;
      tableId = btr.AppendEntity(table);
    tr.AddNewlyCreatedDBObject(table, true);
      //table.Cells.SetDataLink(dlId, false);
    table.SetDataLink(1, 0, dlId, true);
      //Generate the layout
    table.GenerateLayout();
      tr.Commit();
}
Download MyBlock

## 评论

**内容**: Oleg said...
Thnaks so much for your article, Balaji,
this code is working like a sharm on my A2010
with no changes,
Regards,
Oleg
Reply
04/25/2013 at 08:16 AM

---
**内容**: Balaji said in reply to Oleg...
Thanks Oleg :)
Reply
04/25/2013 at 09:39 PM

---
**内容**: George said...
Code extracted table, but the entire table is locked. How does one unlock the table? Thanks.
Reply
05/02/2013 at 03:25 AM

---
**内容**: Balaji said...
Hi George,
To unlock the table for editing, traverse the cells in the table and set its state as
table.Cells[row, col].State = CellStates.ContentModifiedAferUpdate |
CellStates.FormatModifiedAfterUpdate |
CellStates.Linked
As AutoCAD treats the cell content as modified, the next time the table content is updated, a messagebox will appear before overwriting its contents using the DataLink.
Reply
05/03/2013 at 03:20 AM

---
**内容**: Brent said...
This code is fantastic. Can you rename the columns from their SelectedPropertyNames?
Thanks,
Brent
Reply
05/05/2013 at 09:47 PM

---
**内容**: Balaji said in reply to Brent...
Hi Brent,
Before the dxe is saved, the display names of the columns can be changed.
Here is a sample code :
for (int col = 0; col < setting.Report.Count; col++)
{
DxColumn2 dxColumn = setting.Report[col] as DxColumn2;

// If you want to hide a column.
//dxColumn.Flags = dxColumn.Flags | DxColumnFlags.Hidden;
// To change its display name
dxColumn.DisplayName = String.Format("Column-{0}", col + 1);
}
Regards,
Balaji
Reply
05/06/2013 at 01:51 AM

---
**内容**: Brent said...
Thanks Balaji!!
Reply
05/09/2013 at 07:46 AM

---
**内容**: Karl said...
Congratulations for such a great webpage.
My concern is about to turn a text box of a value in the attribute window into a combo box, and relate that combo box to an Access database. Is it possible?
Thanks in advance.
Reply
09/09/2013 at 04:18 AM

---
**内容**: Karl said in reply to Karl...
PS: ... in the attribute window OF A BLOCK...
Reply
09/09/2013 at 04:24 AM

---
**内容**: Balaji said in reply to Karl...
Hi Karl,
Sorry, I did not understand your question.
Do you mean in the Attibute editor that AutoCAD displays ?
Since this query may not be directly related to this blog post, my kind request is to post this query in the AutoCAD discussion forum with as much information required to understand your query.
If you can provide me the link to the forum post, I will be glad to help.
The experts in the forum will also provide solutions to your query.
Regards,
Balaji

Reply
09/09/2013 at 06:52 AM

---
**内容**: Gregory S Robinson said...
Balaji Ramamoorthy can you please reach out to me via email
Reply
03/10/2015 at 02:25 AM

---
**内容**: Gregory S Robinson said...
gregoryx.robinson@intel.com
Reply
03/10/2015 at 02:25 AM

---
**内容**: Balaji said...
Hi Gregory,
I have sent you an email.
If it is not confidential, you can share it here as well.
Regards,
Balaji
Reply
03/11/2015 at 09:36 AM

---
**内容**: ramalakshmi said...
hi,
can you please tell me if any other installations needed to do with this example, because iam using this example and failed to create a DXE file.. its getting error.
Please help to give the solution

Thanks & Regards
Ramalakshmi
Reply
05/13/2015 at 09:10 PM

---
**内容**: hamza said...
Great job
thank you very much
Reply
05/14/2016 at 03:30 AM

---
**内容**: Olivier Eckmann said...
Hi,
Thanks so much for your article, Balaji, it works great, but I've a problem when modifing your code. Instead of using your first part to create DXE file, I just copy a fine DXE created by AutoCAD wizard.
When I execute your code, I obtain an error message (eDataLinkAdapterNotFound) with this line
DataAdapter da
= DataAdapterManager.GetDataAdapter
("Autodesk.AutoCAD.DataExtraction.DxDataLinkAdapter");
It seems that AcDx.dll is not loaded when executing this line. Because if my drawing has a DXE link or if I execute AutoCAD Dataextraction Command before launching the code, it's OK, but if I just open a file without any DXE link, error appears.
If I add only this line
DxExtractionSettings setting = new DxExtractionSettings();
execution is OK.
Is there any solution to solve this problem without adding an unsed line?
Olivier
Reply
11/16/2016 at 11:28 PM

---
**内容**: oumaima aatef said...
my project is to extract the database from a step file using windws form and C #.
my problem is that I do not know how to extract the geometric coordinates of each vertex of the piece and its location on the piece.
cordially
Reply
12/04/2019 at 04:53 AM

---
