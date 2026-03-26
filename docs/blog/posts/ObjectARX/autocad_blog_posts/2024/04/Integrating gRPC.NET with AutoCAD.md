---
title: "Integrating gRPC.NET with AutoCAD"
date: 2024-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Plugin
  - gRPC
description: "Microsoft deprecated WCF with the release of .NET 5 and recommends developers transition to more modern technologies. This can be a challenge for t..."
author: Autodesk
---
# Integrating gRPC.NET with AutoCAD

发布日期: 2024-04-01

原始链接: https://adndevblog.typepad.com/autocad/2024/04/integrating-grpcnet-with-autocad.html

## 文章内容

By Madhukar Moogala
Microsoft deprecated WCF with the release of .NET 5 and recommends developers transition to more modern technologies. This can be a challenge for those with existing WCF applications who want to migrate to .NET 8.0.
Recently, I received a question about integrating gRPC.NET, a popular modern alternative to WCF, with AutoCAD 2025.
In response, I've created a small application that demonstrates how to interact with a gRPC server from an AutoCAD client.
This sample provides a starting point for developers interested in exploring this integration approach.
The provided code showcases a basic example using a GreeterService.
Let's break it down:
Client-Side (AutoCAD Plugin):
The TestGrpc method establishes a gRPC channel to a server running on localhost:8080.
It creates a GreeterClient object to interact with the gRPC service.
An asynchronous SayHelloAsync call is made, sending a HelloRequest message with the name "GreeterClient".
The response (HelloReply) containing the server's greeting is received and written to the active AutoCAD document.
gRPC Service Definition (Protobuf):
Defines a Greeter service with a SayHello RPC method.
Clients send a HelloRequest message with their name.
The server responds with a HelloReply containing a greeting.
Server-Side:
Exposes the GreeterService as a gRPC service.
The SayHello method receives a HelloRequest, extracts the name, and constructs a personalized greeting in the HelloReply message.
Running the Application
This code creates a combined gRPC and HTTP server. Clients can use gRPC to interact with the GreeterService, while a basic HTTP endpoint provides a simple test or informational message.
Source Code : https://github.com/MadhukarMoogala/GrpcToAcad/blob/main/README.md

