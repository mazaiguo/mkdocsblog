---
title: 雪花算法ID到前端之后精度丢失问题
date: 2024-02-20
categories:
  - Java
  - 前端
  - 问题解决
tags:
  - 雪花算法
  - 精度丢失
  - Java
  - JSON
description: 解决雪花算法生成的Long类型ID在前端显示时精度丢失问题的多种方案
author: JerryMa
---

# 雪花算法ID到前端之后精度丢失问题

前后端交互的时候，数据的ID字段采用的雪花ID，Long类型，返回给前端时，由于数值过大，会导致精度丢失，后面几位会变成0，这时候就需要把ID字段转成[String类](https://so.csdn.net/so/search?q=String类&spm=1001.2101.3001.7020)型的返回给前端页面。

## @JSONField

采用@JSONField注解，在ID字段上加上如下的注解，即可返回前端字符串的ID数据

```java
@JSONField(serializeUsing = ToStringSerializer.class)
```

Java

>  缺点：很明显，每个返回实体 model，只要有ID，就需要添加注解，太过于繁琐

## 方式二、Long.class转成String.class

在全局配置中，将Long类型的字段转成String类型

```java
@Configuration
public class CustomFastJsonConfig {
    @Bean
    FastJsonHttpMessageConverter fastJsonHttpMessageConverter() {
        //1.需要定义一个convert转换消息的对象
        FastJsonHttpMessageConverter converter = new FastJsonHttpMessageConverter();
        
        //2.添加fastJson的配置信息
        FastJsonConfig fastJsonConfig = new FastJsonConfig();
        //3.设置Long为字符串
        SerializeConfig serializeConfig = SerializeConfig.globalInstance;
        serializeConfig.put(Long.class, ToStringSerializer.instance);
        serializeConfig.put(Long.TYPE, ToStringSerializer.instance);
        fastJsonConfig.setSerializeConfig(serializeConfig);

        //4.在convert中添加配置信息.
        converter.setFastJsonConfig(fastJsonConfig);
        return converter;
    }
}
```

Java

>  缺点：也很明显，后端返回的数据，只要是Long类型的字段，都会被转成String返回，导致扩大了转换范围

## SerializeFilter

利用[FastJson](https://so.csdn.net/so/search?q=FastJson&spm=1001.2101.3001.7020)内置的SerializeFilter，有很多，如下

- PropertyPreFilter 根据PropertyName判断是否序列化；
- PropertyFilter 根据PropertyName和PropertyValue来判断是否序列化；
- NameFilter 修改Key，如果需要修改Key，process返回值则可；
- ValueFilter 修改Value；
- BeforeFilter 序列化时在最前添加内容；
- AfterFilter 序列化时在最后添加内容。

这里主要用到的SerializeFilter为ValueFilter，如下：

```java
public HttpMessageConverter fastJsonHttpMessageConverters() {
        //1.需要定义一个Convert转换消息的对象
        FastJsonHttpMessageConverter fastConverter = new FastJsonHttpMessageConverter();
        FastJsonConfig fastJsonConfig = new FastJsonConfig();
        fastJsonConfig.setSerializerFeatures(SerializerFeature.PrettyFormat);
        fastJsonConfig.setDateFormat("yyyy-MM-dd HH:mm:ss");

        SerializeConfig.globalInstance.put(Long.class, ToStringSerializer.instance);

        fastJsonConfig.setSerializeConfig(SerializeConfig.globalInstance);

        //3.设置id字段为字符串
        fastJsonConfig.setSerializeFilters((ValueFilter) (object, name, value) -> {
            if ("id".equalsIgnoreCase(name)){
                return value + "";
            }
            return value;
        });
        fastConverter.setFastJsonConfig(fastJsonConfig);
        HttpMessageConverter<?> converter = fastConverter;
        return converter;
    }
```

Java

> 很明显，这个处理方式是最好的，这里是将ID字段转成String，需要转换其他字段时，只需要新增相应的逻辑判断即可

## 其它Jackson的解决方案

前端用String类型的雪花ID保持精度，后端及数据库继续使用Long(BigINT)类型不影响数据库查询执行效率。

剩下的问题就是：在Spring Boot应用中，使用Jackson进行JSON序列化的时候怎么将Long类型ID转成String响应给前端。方案如下：

```java
@Configuration
public class JacksonConfig {

  @Bean
  @Primary
  @ConditionalOnMissingBean(ObjectMapper.class)
  public ObjectMapper jacksonObjectMapper(Jackson2ObjectMapperBuilder builder)
  {
    ObjectMapper objectMapper = builder.createXmlMapper(false).build();

    // 全局配置序列化返回 JSON 处理
    SimpleModule simpleModule = new SimpleModule();
    //JSON Long ==> String
    simpleModule.addSerializer(Long.class, ToStringSerializer.instance);
    objectMapper.registerModule(simpleModule);
    return objectMapper;
  }
}
```