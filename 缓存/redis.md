# 1 简单动态字符串

redis采用的是简单动态字符串（simple dynamic string， SDS）的抽象类，SDS定义为

```c
struct sdshdr{
    // SDS中保存的字符串的长度
    // buf数组中的字节数
    int len;
    // buf数组中未使用的字节数
    int free;
    // 字节数组，保存字符串 遵循C字符串
    char buf[]
} sdshdr;
```

C语言中长度N字符串时通过N+1长度的字符数组来表示，最后一个字符通常为‘\n’。如果需要计算某个字符串的长度或者字节数，C字符串的时间复杂度为O(N)，而SDS的只需要访问len属性就可得到，时间复杂度仅为O(1)。**确保了redis的性能的提升**。SDS的更新与设置有api执行时自动完成。

## 1.1 避免缓存区溢出

C字符串不记录字符串的长度，**易造成缓冲区溢出**。例如两个字符串strcat时，如果已经分配好内存空间，如果内存不够用，就会产生缓存区溢出。

SDS api需要对SDS进行修改时，api会检查SDS空间是否够用，够用直接使用free空间，如果不够api会动态扩展，

1. 避免缓冲区溢出。
2. 复杂度从一定N变为最多N

## 1.2 减少修改字符串时内存重新分配内存的次数

C字符串：

> 1.append时，需要重新分配内存空间，否则造成缓冲区溢出
>
> 2.trim时，重新分配来释放**不在使用**的那部分空间，否则会造成内存泄漏

SDS：

> sds中包含了free属性，即**未使用的字节数**，
>
> 1. 空间预分配：优化字符串append，除了分配必要的空间，还会分配未使用的空间，
>    1. 长度小于1MB时，len=free，char数组的长度为len+free+1（1表示字符串的结尾符号）
>    2. 长度大于等于1MB时，free会分配1MB
> 2. 惰性空间释放
>    1. trim时，释放的空间会放在free中，等待后续的使用

## 1.3 二进制安全

C字符串：

1. 除了字符串末尾，不能保存空字符，不适合保存二进制数据

SDS：

1. 二进制安全的数据结构，可以保存任意格式的二进制文件 

## 1.4 总结

|              C字符串               |                    SDS                     |
| :--------------------------------: | :----------------------------------------: |
|           作为字面量使用           |               作为字符串使用               |
|   获取字符串的长度的复杂度为O(N)   |       获取字符串的长度的复杂度为O(N)       |
|    api不安全，易造成缓冲区溢出     |        api安全，不会造成缓冲区溢出         |
| 修改长度N字符串需要执行N次内存分配 | 修改长度N字符串需要**最多执行N次**内存分配 |
|          只能保存文本数据          |          可以保存文本，二进制数据          |
|    可以使用所有<string.h>的方法    |                可以使用部分                |

# 2 链表

redis并没有内置链表的数据结构。自己构建。广泛使用在**列表键，发布与订阅，慢查询，监视器**等

## 2.1 链表节点与链表

```c
typedef struct listNode {
    struct listNode *prev;
    struct listNode *next;
    void *value;
}listNode;
```

```c
typedef struct list {
    listNode *head;
    listNode *tail;
    unsigned long len;
    void *(*dup)(void *ptr);// 节点值复制函数
    void (*free)(void *ptr);// 节点值释放函数
    int (*match)(void *ptr, void *key);// 节点值比对函数
}list;
```

**特点：**

- **双端：**获取前后两个节点的复杂度为O(1)
- **无环：**头节点的prev与尾节点的next指向null，可以以null来判断为终点
- **带表头和表尾指针：**list结构包含表头表尾的指针，获取表头和表尾的负责度为O(1)
- **带链表长度计数器：**len属性代表链表的长度，获取链表长度或者节点数据的复杂度为O(1)
- **多态：**包含了dup，free，match函数，链表可以保存不同类型的数据

# 3 字典

```c++
typedef struct dictht {
    dictEntry **table; // 哈希表数组
    unsigned long size;// 哈希表大小
    unsigned long sizemask;// 大小掩码 计算索引值 = size-1
    unsigned long used;// 已有的节点数量
} dictht;
```

```c++
typedef struct dictEntry {
    void *key; // 
	union{
        void *val;
        uint64_tu64;
        int64_ts64;
    } v;
    struct dictEntry *next;
} dictht;
```

参考java的HashMap















