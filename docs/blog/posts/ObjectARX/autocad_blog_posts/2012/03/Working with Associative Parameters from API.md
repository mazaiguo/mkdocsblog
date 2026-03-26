---
title: "Working with Associative Parameters from API"
date: 2012-03-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C++
  - ObjectARX
description: "The associative API, the functionality managing constraints behavior, introduced in AutoCAD 2010 (for ObjectARX) and 2011 (.Net counterpart) is pre..."
author: Autodesk
---
# Working with Associative Parameters from API

发布日期: 2012-03-01

原始链接: https://adndevblog.typepad.com/autocad/2012/03/working-with-associative-parameters-from-api.html

## 文章内容

By Philippe Leefsma
The associative API, the functionality managing constraints behavior, introduced in AutoCAD 2010 (for ObjectARX) and 2011 (.Net counterpart) is pretty complex to work with at first sight.
The following post illustrates how to deal with one aspect of this framework using the .Net API, the Associative Variables, or parameters as they are called in the user interface (you display the list of existing parameters by running command PARAMETERS in AutoCAD).
The AssocParameterCmd command allows to create, modify and rename parameters. I split the code into five utility methods which names are pretty explicit to infer what they are doing:
- AddNewVariableToAssocNetwork
- GetVariableByName
- RenameVariable
- GetVariableValue
- SetVariableValue
For those interested in more advanced functionalities using the associative framework, like constraints creation, you can refer to the high level API utility we wrote on top on the framework, available for download here:
http://through-the-interface.typepad.com/through_the_interface/2011/08/a-simplified-net-api-for-accessing-autocad-parameters-and-constraints.html
  //Use:
//Illustrates use of Associative API for manipulating parameters
//Philippe Leefsma, Developer Technical Services. March 2012.
[CommandMethod("AssocParameterCmd")]
public void AssocParameterCmd()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptStringOptions pso = new PromptStringOptions(
        "Enter Parameter Name: ");
    pso.AllowSpaces = false;
      PromptResult pr = ed.GetString(pso);
      if (pr.Status != PromptStatus.OK)
        return;
      ObjectId varId = GetVariableByName(
        db.CurrentSpaceId,
        pr.StringResult,
        false);
      if (varId != ObjectId.Null)
    {
        PromptKeywordOptions pko = new PromptKeywordOptions(
            "\nThe Parameter already exist, select option:");
        pko.AllowNone = false;
        pko.Keywords.Add("Getvalue");
        pko.Keywords.Add("Rename");
        pko.Keywords.Add("Modify");
        pko.Keywords.Default = pko.Keywords[0].LocalName;
          PromptResult pkr = ed.GetKeywords(pko);
          if (pkr.Status != PromptStatus.OK)
            return;
          switch (pkr.StringResult)
        {
            case "Getvalue":
                  string name = string.Empty;
                ResultBuffer value = null;
                string expression = string.Empty;
                                        GetVariableValue(
                    varId,
                    ref name,
                    ref value,
                    ref expression);
                       ed.WriteMessage("\n" + name + " = " +
                    expression +
                    " (Evaluated: " +
                    value.AsArray()[0].Value.ToString() + ")");
                break;
              case "Rename":
                  while (true)
                {
                    try
                    {
                        PromptStringOptions psoRename =
                            new PromptStringOptions(
                                "\nEnter parameter new name:");
                          PromptResult prRename = ed.GetString(
                            psoRename);
                          if (prRename.Status != PromptStatus.OK)
                            return;
                          RenameVariable(
                            varId,
                            prRename.StringResult,
                            true);
                          break;
                    }
                    catch
                    {
                        ed.WriteMessage(
                            "\nInvalid name, please try again...");
                    }
                }
                  break;
              case "Modify":
                  while (true)
                {
                    try
                    {
                        PromptStringOptions psoExpr =
                            new PromptStringOptions(
                                "\nEnter parameter new expression:");
                          PromptResult prExpr = ed.GetString(psoExpr);
                          if (prExpr.Status != PromptStatus.OK)
                            return;
                          SetVariableValue(
                            varId, null, prExpr.StringResult);
                          break;
                    }
                    catch
                    {
                      ed.WriteMessage(
                        "\nInvalid expression, please try again...");
                    }
                }
                                        break;
              default:
                return;
        }
    }
    else
    {
        PromptKeywordOptions pko = new PromptKeywordOptions(
         "\nThe Parameter doesn't exist, do you want to create it?");
        pko.AllowNone = false;
        pko.Keywords.Add("Yes");
        pko.Keywords.Add("No");
        pko.Keywords.Default = pko.Keywords[0].LocalName;
          PromptResult pkr = ed.GetKeywords(pko);
          if (pkr.Status != PromptStatus.OK)
            return;
          if (pkr.StringResult == "No")
            return;
          varId = GetVariableByName(
            db.CurrentSpaceId,
            pr.StringResult,
            true);
          ed.WriteMessage(
           "\nParameter created [Id:" + varId.ToString() + "]");
    }
}
  ObjectId AddNewVariableToAssocNetwork(
    ObjectId networkId,
    string name,
    string expression)
{
    using (Transaction Tx =
        networkId.Database.TransactionManager.StartTransaction())
    {
        using (AssocNetwork network =
            Tx.GetObject(networkId, OpenMode.ForWrite, false)
                as AssocNetwork)
        {
            AssocVariable var = new AssocVariable();
              network.Database.AddDBObject(var);
              network.AddAction(var.ObjectId, true);
              string errMsgValidate = string.Empty;
              var.ValidateNameAndExpression(
                name,
                expression,
                ref errMsgValidate);
              var.SetName(name, true);
              var.Value = new ResultBuffer(
                new TypedValue[]
                {
                    new TypedValue((int)DxfCode.Real, 1.0)
                });
              string errMsgEval = string.Empty;
              var.SetExpression(
                expression, "", true, true, ref errMsgEval, false);
              ResultBuffer evaluatedExpressionValue =
                new ResultBuffer();
              var.EvaluateExpression(ref evaluatedExpressionValue);
              var.Value = evaluatedExpressionValue;
              Tx.AddNewlyCreatedDBObject(var, true);
            Tx.Commit();
              return var.ObjectId;
        }
    }
}
  ObjectId GetVariableByName(
    ObjectId btrId,
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
                    AssocVariable var =
                      Tx.GetObject(actionId, OpenMode.ForRead, false)
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
      return AddNewVariableToAssocNetwork(networkId, name, "1.0");
}
  void RenameVariable(
       ObjectId variableId,
       string newName,
       bool updateReferencingExpressions)
{
       using (Transaction Tx =
        variableId.Database.TransactionManager.StartTransaction())
    {
        AssocVariable var =
            Tx.GetObject(variableId, OpenMode.ForRead)
                as AssocVariable;
          string errMsgValidate = string.Empty;
          var.ValidateNameAndExpression(
            newName,
            var.Expression,
            ref errMsgValidate);
             var.UpgradeOpen();
          var.SetName(newName, updateReferencingExpressions);
          Tx.Commit();
    }
}
  void GetVariableValue(
       ObjectId variableId,
       ref string name,
    ref ResultBuffer value,
    ref string expression)
  {
       using (Transaction Tx =
        variableId.Database.TransactionManager.StartTransaction())
    {
        AssocVariable var =
            Tx.GetObject(variableId, OpenMode.ForRead)
                as AssocVariable;
             name = var.Name;
          var.EvaluateExpression(ref value);
             expression = var.Expression;
          Tx.Commit();
       }
}
  void SetVariableValue(
       ObjectId variableId,
       ResultBuffer value,
       string expression)
{
    using (Transaction Tx =
        variableId.Database.TransactionManager.StartTransaction())
    {
        AssocVariable var =
            Tx.GetObject(variableId, OpenMode.ForWrite)
                as AssocVariable;
          if (expression != string.Empty)
        {
            string errMsg = string.Empty;
              var.ValidateNameAndExpression(
                var.Name,
                expression,
                ref errMsg);
              var.SetExpression(
                expression, "", true, true, ref errMsg, true);
              ResultBuffer evaluatedExpressionValue = null;
              var.EvaluateExpression(ref evaluatedExpressionValue);
              var.Value = evaluatedExpressionValue;
        }
        else
        {
            var.Value = value;
        }
          Tx.Commit();
    }
}
  A screenshot of the command line output when running AssocParameterCmd:
Contributed by Philippe Leefsma.
Autodesk Developer Network.

