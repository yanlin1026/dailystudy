# 1、发送短信验证码resp为什么需要实现序列化接口

<img src = "code.assets/1557710001399.png" style = "zoom:0.75">

# 2、Boolean和boolean区别？包装类与基本数据类型区别？

<img src="code.assets/1557710137358.png" style="zoom:0.75">

请求参数使用包装类，因为请求参数可能为null，

返回参数无所谓，因为返回参数一般数据结构定义好之后，一般布尔变量要么是true要么false。