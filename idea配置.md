1.
2. 在 idea 中使用阿里巴巴代码规范插件及快捷注释的配置https://www.jianshu.com/p/8e4423744231?utm_campaign

```groovy
groovyScript(
    "def result='';
    def params=\"${_1}\".replaceAll('[\\\\[|\\\\]|\\\\s]', '').split(',').toList();
    for(i = 0; i < params.size(); i++) {
        if(i==0){
            result += '\+\" ' + params[i] + ' :\"\+'+params[i];}
        else{
            result+=' \+\"\; ' + params[i] + ' :\"\+'+params[i];}
    };
    return result;",
    methodParameters()
);

groovyScript(
        "def result='';
        def params=\"${_1}\".replaceAll('[\\\\[|\\\\]|\\\\s]', '').split(',').toList();
        for(i = 0; i < params.size(); i++) {
            result +=' * @param ' + params[i] + ((i < params.size() - 1) ? '\\n' : '')};
            return result ", methodParameters());

    groovyScript("if(\"${_1}\".length() == 2) {return '';} else {def result=''; def params=\"${_1}\".replaceAll('[\\\\[|\\\\]|\\\\s]', '').split(',').toList();for(i = 0; i < params.size(); i++) {if(i==0){result+='* @Param ' + params[i] + ': '}else{result+='\\n' + ' * @Param ' + params[i] + ': '}}; return result;}", methodParameters());

    groovyScript("def returnType = \"${_1}\"; def result = '* @return: ' + returnType; return result;", methodReturnType());

```

# 配置代码模板

1. 日志

   ```java
   private static final Logger logger = LoggerFactory.getLogger($class$.class);

   logger.info("$CLASS_NAME$ $METHOD_NAME$ request = ", $ARGUMENTS$);

   ```


# 注册表
1. 添加markdown新建
```
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\.md]
@="TyporaMarkdownFile"
"PerceivedType"="text"
"Content Type"="text/plain"

[HKEY_CLASSES_ROOT\.md\ShellNew]
"NullFile"=""
```

将md加入到右键新建中


   ```
   Windows Registry Editor Version 5.00
   [HKEY_CLASSES_ROOT\.md\ShellNew]
   "NullFile"=""
   "FileName"="template.md"
   ```

IDEA激活码生成   https://zhile.io/custom/license

IDEA激活https://zhile.io/
