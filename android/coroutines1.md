# Kotlin协程基础用法

## 1. 协程的基本概念

协程是一种轻量级的线程，可以用来编写异步代码。Kotlin的协程具有以下特点：

- 轻量级：协程的开销很小，可以同时运行多个协程
- 内置取消支持：可以方便地取消正在运行的协程
- 结构化并发：可以在一个作用域内启动多个协程

讲人话, 协程就是封装的的运行代码块, 这个代码块可以在不同的线程中运行, 这个代码块可以被挂起, 可以被取消, 可以被恢复, 可以被等待.
至于协程到底在什么线程上执行, 你只能指定类型, 不能指定具体的线程, 协程的执行线程是由协程的调度器来决定的. 当然也可以自定义调度器来实现.

## 2. 基本使用

### 2.1 启动协程

在Kotlin中，我们可以使用以下几种方式启动协程：

```kotlin
// 1. 使用GlobalScope启动（不推荐）
GlobalScope.launch {
    delay(1000)
    println("Hello from coroutine")
}

// 2. 使用CoroutineScope创建作用域（推荐）
val scope = CoroutineScope(Dispatchers.Main)
scope.launch {
    delay(1000)
    println("Hello from coroutine scope")
}

// 3. 在Activity/Fragment中使用lifecycleScope
lifecycleScope.launch {
    delay(1000)
    println("Hello from lifecycle scope")
}
```

### 2.2 协程构建器

Kotlin提供了两种主要的协程构建器：

1. launch：启动一个新协程，不返回结果
2. async：启动一个新协程，返回Deferred对象，可以获取结果

```kotlin
// 使用launch
val job = scope.launch {
    delay(1000)
    println("Task completed")
}

// 使用async
val deferred = scope.async {
    delay(1000)
    "Task result"
}
// 获取async结果
val result = deferred.await()
```

### 2.3 协程的取消

协程的取消是结构化并发的重要特性，可以通过以下方式实现：

1. 使用Job的cancel方法
2. 使用作用域的取消
3. 处理嵌套协程的取消

```kotlin
// 1. 基本的取消操作
val job = scope.launch {
    try {
        repeat(1000) { i ->
            println("job: $i")
            delay(500L)
        }
    } finally {
        println("job: 执行清理操作")
    }
}
delay(1300L) // 延迟一段时间
job.cancel()  // 取消协程
job.join()    // 等待协程完成

// 2. 作用域取消
val scope = CoroutineScope(Job())
scope.launch {
    launch {
        delay(100)
        println("Task 1")
    }
    launch {
        delay(200)
        println("Task 2")
    }
}
scope.cancel() // 取消作用域内所有协程

// 3. 嵌套协程的取消
val parentJob = scope.launch {
    val child = launch {
        try {
            repeat(1000) { i ->
                println("child: $i")
                delay(500L)
            }
        } finally {
            println("child: 清理资源")
        }
    }
    delay(1200L)
    println("parent: 取消子协程")
    child.cancel() // 取消子协程
    child.join()   // 等待子协程完成
    println("parent: 继续执行")
}
```

在处理协程取消时需要注意以下几点：

1. 取消是协作的：协程必须协作才能被取消
2. 所有挂起函数都是可取消的
3. finally块可以用于清理资源
4. 父协程取消会导致所有子协程取消
5. 可以使用withContext(NonCancellable)执行不可取消的代码块

```kotlin
scope.launch {
    try {
        work()
    } finally {
        withContext(NonCancellable) {
            // 这里的代码即使在取消时也会执行
            delay(1000L)
            println("清理完成")
        }
    }
}
```

### 2.4 协程上下文和调度器

协程上下文（CoroutineContext）是一个重要的概念，它包含了协程运行所需的各种配置信息。主要包含以下元素：

1. Job：控制协程的生命周期
2. CoroutineDispatcher：控制协程在哪个线程运行
3. CoroutineName：为协程指定一个名称，用于调试
4. CoroutineExceptionHandler：处理未捕获的异常

这些元素可以组合使用：

```kotlin
val scope = CoroutineScope(Dispatchers.Main + Job() + CoroutineName("MyScope"))

// 基本的调度器使用
scope.launch(Dispatchers.Main) {    // UI线程
    launch { // 运行在父协程的上下文中，Main线程
        println("main runBlocking      : I'm working in thread ${Thread.currentThread().name}")
    }
    launch(Dispatchers.Unconfined) { // 不受限的——将工作在主线程中, 这里虽然打印在Main线程, 但是如果加个delay(), delay之后就可能在其他线程执行
        println("Unconfined            : I'm working in thread ${Thread.currentThread().name}")
        delay(500)
        println("Unconfined            : 这里在什么线程是不确定的 ${Thread.currentThread().name}")
    }
    withContext(Dispatchers.IO) {    // IO线程
        // 网络请求或文件操作
    }
    withContext(Dispatchers.Default) { // CPU密集型操作
        // 复杂计算
    }
}

// 自定义上下文组合
val customContext = Dispatchers.IO + CoroutineName("NetworkCall") + 
    CoroutineExceptionHandler { _, exception ->
        println("Caught $exception")
    }

scope.launch(customContext) {
    // 在IO线程执行，带有名称和异常处理
    val data = fetchData()
    withContext(Dispatchers.Main) {
        // 切换到主线程更新UI
        updateUI(data)
    }
}
```

协程上下文具有继承关系：

1. 子协程会继承父协程的上下文
2. 子协程可以覆盖继承的元素
3. Job总是会创建新的实例，确保子协程可以独立取消

```kotlin
scope.launch(Dispatchers.IO + CoroutineName("Parent")) {
    println("Parent context: $coroutineContext")
    
    launch(CoroutineName("Child")) { // 继承IO调度器，覆盖名称
        println("Child context: $coroutineContext")
    }
}
```

在实际开发中的最佳实践：

1. 在UI层使用Dispatchers.Main
2. IO操作使用Dispatchers.IO
3. CPU密集型计算使用Dispatchers.Default
4. 合理使用withContext切换上下文
5. 需要调试时添加CoroutineName
6. 在适当的范围添加异常处理器

## 3. 异常处理

### 3.1 基本异常处理

```kotlin
scope.launch {
    try {
        // 可能抛出异常的代码
    } catch (e: Exception) {
        // 处理异常
    }
}

// 使用异常处理器
val handler = CoroutineExceptionHandler { _, exception ->
    println("Caught exception: $exception")
}
scope.launch(handler) {
    throw Exception("Error")
}
```

### 3.2 supervisorScope

使用supervisorScope可以防止一个子协程的异常影响其他子协程：

```kotlin
supervisorScope {
    launch {
        delay(100)
        throw Exception("Failed")  // 不会影响其他子协程
    }
    launch {
        delay(200)
        println("This will still run")
    }
}
```

## 4. 实用操作符

### 4.1 withContext

用于切换协程上下文，常用于切换线程：

```kotlin
lifecycleScope.launch(Dispatchers.Main) {
    val result = withContext(Dispatchers.IO) {
        // 在IO线程执行耗时操作
        api.fetchData()
    }
    // 回到Main线程更新UI
    updateUI(result)
}
```

### 4.2 coroutineScope

创建一个新的协程作用域，等待所有子协程完成：

```kotlin
suspend fun loadData() = coroutineScope {
    val data1 = async { api.fetchData1() }
    val data2 = async { api.fetchData2() }
    // 等待所有数据加载完成
    data1.await() + data2.await()
}
```

## 5. 最佳实践

1. 避免使用GlobalScope，它的生命周期与应用程序相同
2. 在Android中，优先使用lifecycleScope或viewModelScope
3. 合理使用异常处理，避免异常静默传播
4. 使用适当的调度器，避免在主线程执行耗时操作
5. 及时取消不需要的协程，避免内存泄漏

## 6. 注意事项

1. 协程是非阻塞的，但suspend函数会挂起协程
2. async和launch的选择取决于是否需要返回结果
3. withContext和async的区别：withContext直接返回结果，async返回Deferred
4. 在Activity/Fragment销毁时记得取消协程
5. 使用supervisorScope时子协程的异常需要单独处理
