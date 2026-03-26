---
title: "Integrating an ARX application with SQLite"
date: 2023-11-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - SQL
description: "A brief introduction to SQLite:"
author: Autodesk
---
# Integrating an ARX application with SQLite

发布日期: 2023-11-01

原始链接: https://adndevblog.typepad.com/autocad/2023/11/integrating-an-arx-application-with-sqlite.html

## 文章内容

By Sreeparna Mandal
A brief introduction to SQLite:
SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured SQL database engine. For programs that have a lot of data that must be sifted and sorted in diverse ways, it is often easier and quicker to load the data into an in-memory SQLite database and use queries with joins and ORDER BY clauses to extract the data in the form and order needed.
What can an ARX Application integrated with SQLite do?
The ARX application can create a new database and add tables to it by defining the structure of each table and adding data to it through INSERT statements. If a database containing tables already exists, the ARX can fetch the necessary data from it using SELECT statements combined with other clauses, store the records in a data structure and use it to create a drawing in AutoCAD.
How to create an ARX Application integrated with SQLite?
Step 1:
Download the C source code of SQLite as an amalgamation from its website.
Step 2:
Create a new project with "ARX/DBX Project for AutoCAD" template. Add shell.c and sqlite3.c to Source Files in the project.
Step 3:
Set Project->Properties->C/C++->Code Generation->Smaller Type Check to No
Step 4:
Set Properties->C/C++->Pre Compiled Header->Pre Compiled Header to NOT USING
Step 5:
To create a table by adding it to a database:
Define the table structure(s) as members of the class.
struct LineCoord 
{
 int x_coord;
 int y_coord;
};
Open the particular database using sqlite3_open() function.
sqlite3* db;
if (sqlite3_open("LineCoordDB.db", &db) != SQLITE_OK)
{
 sqlite3_close(db);
 return;
}
Store the CREATE TABLE query as a string. Prepare the sql query from this string using sqlite3_prepare() and execute this query using sqlite3_step().
std::string createTableQuery = "CREATE TABLE LINECOORD ("
   "ID INT PRIMARY KEY NOT NULL,"
   "XCOORD INT NOT NULL,"
   "YCOORD INT NOT NULL);";

//prepare sql statement from the string containing the query
sqlite3_stmt* createTableStmt;
sqlite3_prepare(db, createTableQuery.c_str(), static_cast(createTableQuery.size()), &createTableStmt, nullptr);
  
//execute sql query to create table
if (sqlite3_step(createTableStmt) != SQLITE_DONE)
{
 sqlite3_close(db);
}
Step 6:
Inserting data into table:
Store the INSERT query into a string or in case of multiple INSERT statements, use a vector of string.
std::vector insertStmtList;
insertStmtList.emplace_back("INSERT INTO LINECOORD ('ID', 'XCOORD', 'YCOORD') VALUES ('101', '1', '1');");
Prepare the sql query from the string using sqlite3_prepare() and execute this query using sqlite3_step().
for (const auto& insertQueryStr : insertStmtList)
{
 sqlite3_stmt* insertStmt;
 sqlite3_prepare(db, insertQueryStr.c_str(), static_cast(insertQueryStr.size()), &insertStmt, nullptr);

 //execute each sql stmt
 if (sqlite3_step(insertStmt) != SQLITE_DONE)
 {
  sqlite3_close(db);
  return;
 }
}
Close the database using sqlite3_close().
The created table and its data can be checked by installing 'DB Browser (SQLite)' from official website of SQLite.
Step 7:
To fetch data from an existing table
Open the particular database using sqlite3_open() function.
Define the following where each variable of Record type will hold data of a tuple(row) and a variable of Records type will hold the data of the entire table:
using Record = std::vector;
using Records = std::vector;
We call a user defined function with string parameter containing the sql SELECT query to fetch all the data and return it to a variable of Records type. Inside the user defined function, we use a callback. SQLite will call this callback function for each record processed in each SELECT statement executed within the SQL argument.
For a very basic understanding, you may refer to the example shown in SQLite website. Kindly refer to the methods ADSKMyGroupGetLineCoord(), select_callback() and exec_select_stmt() from the complete source code to see the full implementation.
Step 8:
To create a drawing using the data stored in the table
In this case, extract data of each record(an X-coordinate and a Y-coordinate) from the data structure used to store the table values and use them to draw a line.
Complete sample with source code is available at Github : Arx_SQLite_2DLineCoordinates

## 评论

**内容**: Dan said...
It’s really handy. I’ve been embedding SQLite in my ARX apps for years. great for storing settings,
but you can also store files i.e .dwg blocks or, block Icons
one such module is SQLite for AutoLisp
https://www.theswamp.org/index.php?topic=28286.0
Reply
11/12/2023 at 04:36 AM

---
**内容**: dino game said...
Dino Game is a speed game that was first made for Google Chrome. The game was added to Google Chrome in 2014 as a "Easter egg" to keep people busy when they can't get online. Every month, more than 270 million people play a game called "Chrome Dino" that has a T-Rex in it. The Dinosaur Game can be played in full screen, even when you are online.
Reply
12/12/2023 at 08:25 PM

---
**内容**: Annata Evan said...
Integrating an ARX (Augmented Reality) application with SQLite involves using SQLite as the database management system for storing and retrieving data related to your AR experience.
Reply
01/30/2024 at 01:21 AM

---
**内容**: Pokerogue said...
In the realm of digital gaming, innovation is the key to capturing the attention of avid players. Enter Pokerogue, a groundbreaking game that masterfully blends the strategic depth of poker with the thrilling unpredictability of a roguelike adventure.
Reply
06/03/2024 at 05:46 PM

---
