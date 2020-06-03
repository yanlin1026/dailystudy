# 1. [深入理解Java中的String](https://www.cnblogs.com/xiaoxi/p/6036701.html)

# 2.集合

---

```JAVA
package java.util;
public class List {
    public static void main(String[] args) {
        System.out.println("a");
    }
}
```

Q：上述代码执行main方法会发生什么？

A：违反java沙箱安全机制

```tex
错误: 在类 java.util.List 中找不到 main 方法, 请将 main 方法定义为:
   public static void main(String[] args)
否则 JavaFX 应用程序类必须扩展javafx.application.Application
```

---



