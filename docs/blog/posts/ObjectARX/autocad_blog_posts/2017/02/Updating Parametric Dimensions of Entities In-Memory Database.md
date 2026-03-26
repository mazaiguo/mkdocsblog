---
title: "Updating Parametric Dimensions of Entities In-Memory Database"
date: 2017-02-01
categories:
  - AutoCAD
tags:
  - Database
  - Dimension
description: "I have received a query from ADN  on how to update the parameters of a drawing which is not an active document but read as in-memory database."
author: Autodesk
---
# Updating Parametric Dimensions of Entities In-Memory Database

发布日期: 2017-02-01

原始链接: https://adndevblog.typepad.com/autocad/2017/02/updating-parametric-dimensions-of-entities-in-memory-database.html

## 文章内容

By Madhukar Moogala
I have received a query from ADN  on how to update the parameters of a drawing which is not an active document but read as in-memory database.
For active drawing, we can use DIMREGEN in case if associated dimensions are updated, associated dimension may not act automatically in certain workflows, where a manual dimension regen is required.
But, for in-memory database, after modifying Parameter values(AcDbAssocVariable), to take effect on underlying entities of dimensions it is preferable to always evaluate the top level network of the database by calling AcDbAssocManager::evaluateTopLevelNetwork(). Evaluation of the whole top level network guarantees that all actions that need to be evaluated, are evaluated. There is no performance penalty by always evaluating the whole top level network of the database even if it contains many sub networks and many actions.
Following code assumes, user is trying to update dimensions on parametric rectangle of 20.0 and 30.0, test drawing and test project is appended at the bottom.
namespace filer
{
    ///<Summary>
    /// How to update Parameters on entities  of in-memory database
    ///</Summary>
public class TestFiler
{
    ///<Summary>
    /// How to update Parameters on entities  of in-memory database
    ///</Summary>
    ///
[CommandMethod("DIMUPDATE")]
public static void testDimUpdate()
{
Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
try
{
    string drawingFile = getDrawingLocation();
    using (Database db = new Database(false, true))
    {
        db.ReadDwgFile(drawingFile,
                        FileOpenMode.OpenForReadAndWriteNoShare,
                        false, null);
        db.CloseInput(true);
        using (Transaction tr = db.TransactionManager.StartTransaction())
        {
            BlockTableRecord btr = 
            (BlockTableRecord)tr.GetObject(SymbolUtilityServices.GetBlockModelSpaceId(db),
                                            OpenMode.ForRead);
            /*Width*/
            ObjectId wActionId = GetVariableByName(btr.ObjectId, "Width", false);
            string name = string.Empty;
            ResultBuffer rbuf = null;
            string expression = string.Empty;
            GetVariableValue(wActionId, ref name, ref rbuf, ref expression);
            expression = "30";//Width Value
            SetVariableValue(wActionId, null, expression);
                /*Check  if our values Got reflected in DB*/
            GetVariableValue(wActionId, ref name, ref rbuf, ref expression);
            if (String.Compare(expression, "30"/*hardCoded For Width*/).Equals(0))
                Application.ShowAlertDialog("Hey Success!");
            else //Quit processing further
                return;
            /*Length*/
            ObjectId lActionId = GetVariableByName(btr.ObjectId,
                                                    "Length", false);
            rbuf = null;
            GetVariableValue(lActionId, ref name, ref rbuf, ref expression);
            expression = "40";//height Value
            SetVariableValue(lActionId, null, expression);
            tr.Commit();
        }

        bool isEvaluationSuccess = AssocManager.EvaluateTopLevelNetwork(db, null, 0);
        if (isEvaluationSuccess)
        {
            //Now Check if the Values Updated in Entity
            using (Transaction tr = db.TransactionManager.StartTransaction())
            {
                BlockTableRecord btr = 
                (BlockTableRecord)tr.GetObject(SymbolUtilityServices.GetBlockModelSpaceId(db),
                                                OpenMode.ForRead);
                foreach (ObjectId id in btr)
                {
                    Entity ent = (Entity)tr.GetObject(id, OpenMode.ForRead);
                    Polyline pline = ent as Polyline;
                    if (pline != null)
                    {
                        //stream the points to Editor Console
                        for (int i = 0; i < pline.NumberOfVertices; i++)
                            ed.WriteMessage("\n" + 
                                            pline.GetPoint3dAt(i).ToString());
                    }


                }
                tr.Commit();
            }
        }
        else return; //We will quit

        //Now save the in-memory DB to Disk.
        db.SaveAs(new StringBuilder(drawingFile).Replace(".dwg",
                                                        "_new.dwg").ToString(),
                                                        DwgVersion.Current);


    }
}
catch (System.Exception ex)
{
    ed.WriteMessage(ex.ToString());
}

}

private static string getDrawingLocation()
{
    /*
    SolutionFolder
    │   
   |───bin
    └───Debug
    │
    assembly.dll

    */
    var assemblyLoc = Assembly.GetExecutingAssembly().Location;
    var debugFolder = Path.GetDirectoryName(assemblyLoc);
    var binFolder = Path.GetDirectoryName(debugFolder);
    var solutionFolder = Path.GetDirectoryName(binFolder);
    var drawingLocationFilePath = solutionFolder + 
                                "\\TestParameters.dwg";
    return Path.GetFullPath(drawingLocationFilePath);
}

///<Summary>
/// Get Variable Name for Given variableId
///</Summary>
///
private static ObjectId GetVariableByName(ObjectId btrId,
string name,
bool createIfDoesNotExist)
{
    if (name.Length == 0)
        throw new Autodesk.AutoCAD.Runtime.Exception(
        ErrorStatus.InvalidInput);

    ObjectId networkId = AssocNetwork.GetInstanceFromObject(
    btrId,
    createIfDoesNotExist,
    true,
    "ACAD_ASSOCNETWORK");

    if (networkId == ObjectId.Null)
        return ObjectId.Null;

    using (Transaction Tx =
    btrId.Database.TransactionManager.StartTransaction())
    {
        using (AssocNetwork network =
        Tx.GetObject(networkId, OpenMode.ForRead, false)
        as AssocNetwork)
        {
            foreach (ObjectId actionId in network.GetActions)
            {
                if (actionId == ObjectId.Null)
                    continue;

                if (actionId.ObjectClass.IsDerivedFrom(
                RXObject.GetClass(typeof(AssocVariable))))
                {
                    //Check if we found our guy
                    AssocVariable var = Tx.GetObject(actionId, 
                                                    OpenMode.ForRead,
                                                    false)
                    as AssocVariable;

                    if (var.Name == name)
                        return actionId;
                }
            }
        }
    }

    //If we don't want to create a new variable, returns an error
    if (!createIfDoesNotExist)
        return ObjectId.Null;

    return ObjectId.Null;//We didnt find what we are looking
}
private static void GetVariableValue(ObjectId variableId,
ref string name,
ref ResultBuffer value,
ref string expression)

{
    using (Transaction Tx =
    variableId.Database.TransactionManager.StartTransaction())
    {
        AssocVariable assocV =
        Tx.GetObject(variableId, OpenMode.ForRead)
        as AssocVariable;

        name = assocV.Name;

        assocV.EvaluateExpression(ref value);

        expression = assocV.Expression;

        Tx.Commit();
    }
}
///<Summary>
/// Set Expression for Given variableId
///</Summary>
///
private static void SetVariableValue(ObjectId variableId,
ResultBuffer value,
string expression)
{
    using (Transaction Tx =
    variableId.Database.TransactionManager.StartTransaction())
    {
        AssocVariable assocV =
        Tx.GetObject(variableId, OpenMode.ForWrite)
        as AssocVariable;

        if (expression != string.Empty)
        {
            string errMsg = string.Empty;

            assocV.ValidateNameAndExpression(
            assocV.Name,
            expression,
            ref errMsg);

            assocV.SetExpression(
            expression, "", true, true, ref errMsg, true);

            ResultBuffer evaluatedExpressionValue = null;

            assocV.EvaluateExpression(ref evaluatedExpressionValue);

            assocV.Value = evaluatedExpressionValue;
        }
        else
        {
            assocV.Value = value;
        }

        Tx.Commit();
    }
}
}
}
Sample Project with Drawings.
UpdateParameters

## 评论

**内容**: Yuri Venenkovich said...
You may want to consider avoiding the use of 'var' as a variable identifier, as it is a C# keyword.
While doing that may be legal, it is also very confusing.
Reply
03/16/2017 at 06:57 PM

---
**内容**: Madhukar Moogala said in reply to Yuri Venenkovich...

Typepad HTML Email

Hi Yuri,
 
Thanks for pointing out, I edited the variable name accordingly.
I agree using C# keyword as variable identifier, the code readability getting compromised.
  Thanks,
Madhu.
  Reply
03/17/2017 at 12:12 AM

---
