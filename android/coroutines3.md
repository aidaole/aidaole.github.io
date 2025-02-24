# 协程-Flow

协程中的Flow, 是借鉴Rx的框架, 在协程中开发的流式框架.

在android使用中, Flow其实跟 LiveData 很像, 但是其实他们也是有区别的, 下文会提到.

## 冷流和热流

先看看 Flow 的第一个问题.  什么是 `冷流`, 什么是 `热流`

冷流: 没有人订阅就不发送, 每次都全部发送
热流: 不管有没有人订阅, 只要数据来就发送, 绑定上的时候就可以收到最新数据

看到这个解释是不是很懵逼. 举个例子:

冷流:

```kotlin
// 这里定义一个冷流, 定义在这里, 只要我这个老师没有到位, 他们就都不会躁动
private val students = flow<String> { 
    for (i in 1..100) {
        emit("student: $i")
    }
}

// 只要老师一点名, 每次全部学生都报数一遍
lifecycleScope.launch {
    students.collect { s ->
        Log.d(TAG, "点名: $s")
    }
}
```

热流:

```kotlin
private val count = MutableStateFlow(0)

for (i in 1..10){
    count.emit(i)
}

lifecycleScope.launche {
    count.collect { 
        print(it) // 这里收到就是10, 不会从1..10重新来一遍
    }
}
```

那么为什么要有热流呢?  其实可以看做是冷流的一种补充, 它可以看做是 状态管理, 事件订阅分发的一种实现.

## 流的用处

### 流式数据

比如我有一个即时通讯应用, 连接了服务端的 web socket, 数据一直从服务端过来, 我需要在ui中显示.

这种场景是不是就很适合使用流来实现, websocket把输入都怼到Flow上, 下面的内容就通过Flow监听数据到ui显示

### Flow支持链式调用

可以使用关键字过滤流程, 将代码简化. 而且Flow也支持切线程的操作, 非常方便

```kotlin
fun main() = runBlocking {
    flowOf(1, 2, 3, 4)
        .filter { it % 2 == 0 } // 过滤偶数
        .map { it * it }       // 平方
        .collect { println(it) } // 输出 4, 16
}
```

### 有LiveData了, 为什么还要使用Flow

LiveData其实是基于Android的, Flow是Kotlin的不依赖Android

LiveData可以看做是热流(监听最新的状态), Flow可以使用SharedFlow和StateFlow来实现状态更新

| 特性     | Flow                   | LiveData                     |   
|:------:|:----------------------:|:----------------------------:|
| 设计目标   | 通用异步数据流                | UI 驱动的状态管理                   |   
| 依赖性    | Kotlin 协程，无 Android 依赖 | Android 架构组件，依赖 Lifecycle    |   
| 数据流类型  | 冷流（默认），支持热流变种          | 热流，始终保持最新值                   |  
| 生命周期感知 | 无（需手动结合 Lifecycle）     | 内置，支持 Activity/Fragment 生命周期 |  
| 线程支持   | 灵活（flowOn 切换线程）        | 主线程更新（需手动切换线程）               |   
| 操作符    | 丰富（map、filter 等）       | 有限（需借助 map、switchMap）        |   
| 异常处理   | 支持 catch 等操作符          | 无内置异常处理                      |   
| 使用场景   | 通用（网络、数据库、UI 等）        | 主要用于 UI 数据绑定                 |   
| 语法风格   | 函数式，基于协程挂起             | 观察者模式，基于 observe             |   

### 背压问题

流式数据经常遇到一个问题就是, 发送者的速度很快, 接收者处理很慢, FLow可以根据自己要的场景很容易的处理. 例如:

1. 要求发送太多数据之后, 就阻塞发送者, 让它发慢一点
2. 如果我只关心最新的数据, 那么我可以丢弃中间的结果, 每次收集都处理最新的数据

这个就对应了 MultiSharedFlow 中的配置

```kotlin
// 场景1
private val sharedCounter =
MutableSharedFlow<Int>(onBufferOverflow = BufferOverflow.SUSPEND)

// 场景2
private val sharedCounter =
MutableSharedFlow<Int>(onBufferOverflow = BufferOverflow.DROP_OLDEST)  
```

当然MutableSharedFlow还有其他配置

`replay`: 当订阅的时候, 可以收到之前的几个数据

`extraBufferCapacity`: 额外的缓存容量, 订阅者处理不过来的时候, 可以优先放到buffer中

`onBufferOverflow`: 拒绝策略

```kotlin
private val sharedCounter =
    MutableSharedFlow<Int>(replay = 10, extraBufferCapacity = 5, onBufferOverflow = BufferOverflow.DROP_OLDEST)
```