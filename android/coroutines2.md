# 协程-线程安全

我们在使用线程的时候, 进程会遇到多个线程同时修改同一个数据, 导致数据被重复写入, 或者读取到错误的值的问题, 纠起原因就是JVM为了提速, 会在运行时对数据进行优化, 比如对数据进行缓存, 但是缓存的前提是数据不会被修改, 所以会出现线程安全问题.

协程是建立在线程之上的, 所以多协程访问同一数据的时候也会有线程安全问题.

## 第一个问题

那么先甩出一个问题, 我们在线程中经常使用的 synchronized, ReentrantLock, AtomicXXX 等, 这些可以继续在协程中使用吗? 

这得根据每种关键字的场景来:

`synchronized`: 可以在协程中使用, 但是需要注意的是, 锁的是线程, 多个协程可能共用一个线程, 相当于锁多的时候, 可能协程都被阻塞了, 对协程不友好. 最好是使用`Mutex`来对协程加锁, 只阻塞协程, 不会阻塞线程

`ReentrantLock`: 的底层机制是AQS, Atomic+队列来实现, 获取不到锁就添加到队列中. 但是加锁过程是记录了线程的(可重入), 在协程中线程又是可以共享的, 多个协程可能使用相同的线程. 那么在调度的时候是不是就会很乱, 容易出现意想不到的问题, 对协程不友好.

`AtomicXXX`: 可以在协程中使用, 是通过自旋锁实现的, 跟线程没关系. 所以协程和线程使用没有差异.

所以从这里可以看出, `synchronized`, `ReentrantLock`(包含其他几个基于AQS的锁Semphere, CountDownLatch等) 是不适合在协程中使用的, 因为它们都可能会阻塞线程, 对协程不友好.

`Atomicxxx` 可以在协程中使用, 但是需要注意的是, 它是基于CAS实现的.

## 协程中有哪些协程同步的方法

### 1. Mutex（协程专属的轻量级锁）：

使用方式跟 `ReentrantLock` 一样

```kotlin
val mutex = Mutex()
var counter = 0

suspend fun incrementCounter() {
    mutex.withLock {
        counter++ // 安全的增量操作
    }
}
```

### 2. 自定义Dispatcher

跟单线程池一样, 我们可以定义自己的单线程 Dispatcher, 那么运行在这个Dispatcher上的所有协程都是排队的, 达到线程安全的目的

```kotlin
private val singleThreadDispatcher = Dispatchers.IO.limitedParallelism(1)
private var counter = 0

suspend fun incrementCounter() = withContext(singleThreadDispatcher) {
    counter++ // 仅在一个线程上操作
}
```

### 3. 使用并发数据结构 AtomicXXX

这个在线程和协程中是通用的, 因为是使用CAS机制实现的, 没有对线程加锁

```kotlin
val counter = AtomicInteger(0)

suspend fun incrementCounter() {
    counter.incrementAndGet() // 原子操作，无需额外锁
}
```

### 4. 使用Channel和Actor

Channel 类型:
Channel() 或 Channel(UNLIMITED)：无缓冲或无限缓冲，发送不会挂起。
Channel(0)：无缓冲（Rendezvous），发送和接收必须同时发生，否则一方挂起。
Channel(n)：有缓冲，容量为 n，满了则发送挂起。
Channel(CONFLATED)：合并通道，新值覆盖旧值，接收者只获取最新值。

```kotlin
fun main() = runBlocking {
    val channel = Channel<Int>(capacity = Channel.UNLIMITED) // 无限制缓冲通道
    var counter = 0 // 共享变量

    // 消费者协程：负责接收消息并更新计数器
    val consumer = launch(Dispatchers.Default) {
        for (increment in channel) {
            counter += increment // 顺序处理，确保线程安全
        }
    }

    // 多个生产者协程：模拟并发修改
    val producers = List(10) {
        launch(Dispatchers.Default) {
            repeat(100) { // 每个协程发送 100 次增量请求，总计 1000 次
                channel.send(1)
            }
        }
    }

    // 等待所有生产者完成
    producers.forEach { it.join() }
    channel.close() // 关闭通道
    consumer.join() // 等待消费者处理完所有消息

    println("Final counter value with Channel: $counter") // 应输出 1000
}
```

```kotlin
// 定义 Actor
fun CoroutineScope.counterActor() = actor<Int> {
    var counter = 0 // Actor 内部的私有变量
    for (increment in channel) { // 接收消息
        counter += increment // 顺序处理
    }
    println("Final counter value inside Actor: $counter") // Actor 关闭时输出
}

fun main() = runBlocking {
    val actor = counterActor()

    // 多个协程并发发送消息
    val jobs = List(10) {
        launch(Dispatchers.Default) {
            repeat(100) { // 每个协程发送 100 次增量请求，总计 1000 次
                actor.send(1)
            }
        }
    }

    // 等待所有发送完成
    jobs.forEach { it.join() }
    actor.close() // 关闭 Actor

    // 注意：这里无法直接访问 counter，因为它封装在 Actor 内部
}
```
Actor 其实是对 Channel的封装, 这里就不多介绍
