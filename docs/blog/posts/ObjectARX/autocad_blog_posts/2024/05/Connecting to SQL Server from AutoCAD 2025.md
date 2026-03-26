---
title: "Connecting to SQL Server from AutoCAD 2025"
date: 2024-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Database
  - NuGet
  - SQL
description: "With the advent of the modern .NET platform, we've received queries from customers about loading SQL data client libraries onto the AutoCAD runtime."
author: Autodesk
---
# Connecting to SQL Server from AutoCAD 2025

发布日期: 2024-05-01

原始链接: https://adndevblog.typepad.com/autocad/2024/05/connecting-to-sql-server-from-autocad-2025.html

## 文章内容

By Madhukar Moogala
With the advent of the modern .NET platform, we've received queries from customers about loading SQL data client libraries onto the AutoCAD runtime.
This post aims to address those queries and guide you on how to connect to SQL Server from an AutoCAD application.
Microsoft SQL Data Client Library
The Microsoft SQL Data Client Library is a brand new library for accessing SQL Server databases from modern .NET client applications. It also provides a common core set of features accessible on both .NET Framework and .NET Core.
As evidenced by this blog post, Microsoft recommends this library over System.Data.SqlClient.
We recommend using the latest LTS version of Microsoft.Data.SqlClient, which is currently 5.2.0 as it's the latest stable version that will be actively maintained for another 3 years. You can find it on the Life Cycle page. If you were previously using System.Data.SqlClient, we also have a guide to ease that process. You can also refer to the FAQ. Hope that helps with your decision on which library to use.
Let's use this NuGet package to write an AutoCAD client application to access SQL Server.
When built along with an AutoCAD plugin, this package produces various artifacts for different runtimes. We only need the Windows 64-bit runtime module, which is supported on AutoCAD.
To ensure this, we need to explicitly tell the build system by setting the following property group in the project file:
    
```html
<PropertyGroup>
<RuntimeIdentifier>win-x64</RuntimeIdentifier>
</PropertyGroup>
```


​    
Alternatively, you can use the dotnet cli:
​    
​      dotnet publish -r win-x64 –c Debug

Once the build is successful, you can see the artifacts in the `x64\Debug\net8.0-windows\win-x64` folder.
Now let's write a simple AutoCAD plugin to connect to SQL Server and query data.
Setup Database
Let's write a Database Manager class to access the `connectionstring`, test the connection, and query data.
We will inject `IConfiguration` to load the `connectionString` from `secret.json`, which is a secure way of accessing database connection strings.
    

```csharp
    public DatabaseManager()
    {
      // Target this class for user secrets
      var builder = new ConfigurationBuilder()
                     .AddUserSecrets();
    
      IConfiguration configuration = builder.Build();
      _connectionString = configuration.GetConnectionString("mssqlserver");
    }
    
```


Now let's write a method to test the connection:
```csharp
    public bool TestSqlServerConnection()
    {
      try
      {
        using (var connection = new SqlConnection(_connectionString))
        {
          connection.Open();
          return true;
        }
      }
      catch (System.Exception ex)
      {
        Console.WriteLine($"Cannot connect to Database server: {ex.Message});
        return false;
      }
    }  

```

​    
Now let's write a method to query the data:
```csharp
  using (var cmd = new SqlCommand(queryString, connection))
  {
    using (var reader = cmd.ExecuteReader())
    {
      if (reader.HasRows)
      {
        while (reader.Read())
        {
          string city = reader.GetString(0); // assuming city is the first column (index 0)
          int customerCount = reader.GetInt32(1); // assuming number of customers is the second column (index 1)
          ed.WriteMessage($"\nCity: {city}, Customer Count: {customerCount}");
        }
      }
      else
      {
        ed.WriteMessage("\nNo results found.");
      }
    }
  }

```

Now let's write a command to test the connection and query the data:
```csharp
  using (var data = new DatabaseManager())
  {
    try
    {
      data.TestSqlServerConnection();
      ed.WriteMessage("\nConnected to SQL Server database successfully!");
      data.RunQueryAndWriteToEditor(ed);
    }
    catch (System.Exception ex)
    {
      ed.WriteMessage($"\nConnecting to SQL Server database failed!\n{ex.Message}");
    }
  }

```


Build the code and load the compiled module in AutoCAD 2025.
Run the command "ConnectDB".
It should connect to SQL Server and query the data.
Full source code is provided on Github: Click Here
Hope this helps you connect to SQL Server from AutoCAD.

## 评论

**内容**: Mia said...
The enneagram test is part of the process of helping you gain self-awareness about who you are and what you're working towards. It is not a predetermined statement about your personality or behavior.
Reply
05/15/2024 at 02:12 AM

---
**内容**: Izhar Azati said...
If you change to OdbcConnection, and try to run on Civil3D, you get:
"System.Data.ODBC is not supported on this platform."
The "C:\Program Files\Autodesk\AutoCAD 2025\C3D\System.Data.Odbc.dll"
The reason for the problem is that the file that is installed is incorrect.
need the file:
"C:\Users\user3\.nuget\packages\system.data.odbc\8.0.0\runtimes\win\lib\net8.0\System.Data.Odbc.dll"
and not the file:
"C:\Users\user3\.nuget\packages\system.data.odbc\8.0.0\lib\net8.0\System.Data.Odbc.dll"
Reply
06/09/2024 at 11:53 PM

---
**内容**: MC said...
Have you been successful connecting to SQL Server using entity framework 6 inside AutoCAD 2025? Every time I use EF6 with a SQL connection, it fails to initialize.
Reply
06/18/2024 at 08:53 AM

---
