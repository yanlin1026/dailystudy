# 1. JSONObject的toString()和toJSONString()的区别？

```java
public String toString() {
    return this.toJSONString();
}

public String toJSONString() {
    SerializeWriter out = new SerializeWriter();

    String var2;
    try {
        (new JSONSerializer(out)).write(this);
        var2 = out.toString();
    } finally {
        out.close();
    }

    return var2;
}
```

根据以上代码可见，toString()方法实际调用的是toJSONString()方法，因此两者一样







1.午餐：代餐棒+一个鸡腿+蔬菜（绿叶菜）

2.晚餐：代餐棒+一个鸡腿+蔬菜（绿叶菜）

3.每天早上体重