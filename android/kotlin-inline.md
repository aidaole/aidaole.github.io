# Kotlin 的 inline, noinline, crossinline

# 1. inline

inline关键字告诉编译器将函数的代码直接嵌入到调用处，而不是通过普通函数调用的方式执行。它主要用于带有Lambda参数的函数。

```kotlin
inline fun performAction(action: () -> Unit) {
    println("Starting action")
    action()
    println("Action completed")
}

fun main() {
    performAction {
        println("This is the action")
    }
}
```

编译后函数调用会被直接替换成函数中的代码

```kotlin
fun main() {
    println("Starting action")
    println("This is the action")
    println("Action completed")
}
```

## 使用场景

性能优化：当函数体很小且频繁调用时，使用inline可以避免函数调用的开销（如栈帧分配）。
Lambda参数：如果函数接受Lambda表达式，inline可以将Lambda的代码直接嵌入调用处，减少对象分配。
高阶函数：常用于工具类函数或DSL设计，例如repeat、let等Kotlin标准库函数。
注意事项

不建议对大型函数使用inline，因为内联会增加生成代码的体积，可能导致性能反而下降。
仅对公共API使用inline时需谨慎，因为内联函数的实现会暴露给调用者，可能影响库的二进制兼容性。

# 2. noinline

在inline函数中，如果某个Lambda参数不希望被内联，可以用noinline修饰。被noinline修饰的参数会保持普通函数调用行为，生成一个Function对象。

```kotlin
inline fun doSomething(
    action1: () -> Unit,
    noinline action2: () -> Unit
) {
    println("Start")
    action1() // 内联
    val func = action2 // 不内联，可以赋值给变量
    func()
    println("End")
}

fun main() {
    doSomething(
        { println("Action 1") },
        { println("Action 2") }
    )
}
```

action1会被内联到调用处。
action2不会内联，会被包装成一个Function0对象。

## 使用场景

需要将Lambda存储或传递：如果Lambda需要作为对象被存储（如赋值给变量或传递给其他函数），必须用noinline，因为内联的Lambda无法独立存在。
部分内联优化：在inline函数中，只想内联部分参数以优化性能，同时保留其他参数的灵活性。

注意事项
noinline只能用在inline函数的Lambda参数上。
使用noinline会增加少量运行时开销（生成Function对象）。

# 3. crossinline

crossinline用于解决inline函数中Lambda参数的非局部返回（non-local return）问题。它要求Lambda中不能使用return直接跳出调用函数，确保代码行为符合预期。

```kotlin
inline fun execute(crossinline task: () -> Unit) {
    val runnable = Runnable { task() } // task不能有非局部返回
    runnable.run()
}

fun main() {
    execute {
        println("Task running")
        // return // 编译错误：crossinline禁止非局部返回
    }
    println("Main continues")
}
```

## 使用场景

Lambda被传递到其他作用域：当inline函数将Lambda传递给另一个非内联的上下文（如Runnable、线程、回调）时，使用crossinline确保Lambda不会意外返回到外层函数。
异步或回调场景：避免因内联导致的控制流混乱。


## 实际开发中的建议

| 特性    | inline   | noinline     | crossinline    |
|-------|----------|--------------|----------------|
| 内联行为  | 完全内联     | 不内联，生成对象     | 内联但限制返回        |
| 适用场景  | 性能优化、DSL | Lambda需存储或传递 | Lambda用于非内联上下文 |
| 非局部返回 | 允许       | 不涉及          | 禁止             |
| 开销    | 无函数调用开销  | 有对象分配开销      | 无函数调用开销        |

小函数用inline：如果函数简单且频繁调用（如工具函数），推荐使用inline。
需要灵活性用noinline：当Lambda需要被存储或延迟执行时，使用noinline。
异步场景用crossinline：涉及线程、回调或非内联上下文时，使用crossinline确保行为可控。

优劣:
内联可能增加APK体积，建议在性能敏感场景下对比测试。
但是inline也可以优化对象生成，减少内存占用。比如说在一个 for 循环中调用 带有 lambda 的函数, 每次调用都会生成 lambda的对象, 将高级函数修改为inline之后, 可以避免对象的生成