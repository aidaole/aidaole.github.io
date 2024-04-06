# Kotin 泛型，协变+逆变

泛型大家都理解，我们用一个例子来说明：比说说集合类 `List<T>`， 我们不仅可以放 `List<Int>` 也可以放 `List<String>`，这是泛型给我们带来的方便之处。

如果我们有一个类 `Person`, `Student`和`Teacher`都继承于`Person`类。 然后 `SimpleData` 定义如下

```
open class Person(
    val name: String
) {
    override fun toString(): String {
        return "Person(name='$name')"
    }
}

class Student(name: String) : Person(name)

class Teacher(name: String) : Person(name)

// 泛型类
class SimpleData<T> {

    private var t: T? = null

    fun set(t: T) {
        this.t = t
    }

    fun get(): T? = t
}
```

如果这时候我们写一个

```
val data: SimpleData<Person> = SimpleData<Student>()
```

这是不允许的，虽然 `Student` 是 `Person` 的子类，但是 `SimpleData<Student>` 不是 `SimpleData<Person>` 的子类，如果要让它支持这种操作，就需要在 `SimpleData<T>` 改成 `SimpleData<out T>`，这就是协变

相反，如果我希望 `SimpleData<Person>` 是 `SimpleData<Student>` 的子类，需要将 `SimpleData<T>` 改为 `SimpleData<in T>`，这就是逆变

那么 协变 和 逆变 到底有什么作用呢？

## 协变

接着刚才的例子，定义一个方法:

```
fun handleDatas(data: SimpleData<Person>) {
    "handleDatas-> $data".logi(TAG)
}
```

如果这时候 `SimpleData` 是不支持 协变，那么这个 `handleDatas(SimpleData<Student>())` 是不允许的，虽然 `handleDatas` 中做的操作其实传 Student 进来也是可以的。

如果改成协变：

```
class SimpleData<out T> {

    private var t: T? = null 
    
//  协变， T只能放在参出的位置，所以set 方法不允许
//    fun set(t: T) {
//        this.t = t
//    }

    fun get(): T? = t
}
```

首先注意，这时候 set方法会报错，因为它将T放在了输入的位置，这是不允许的。这个时候 `handleDatas(SimpleData<Student>())` 就是允许的，所以接受范围扩大了

## 逆变

```
fun handleDatas2(datas: SimpleData<Student>) {
    "handleDatas2-> $datas".logi(TAG)
}
```

如果这时候 `SimpleData` 是不支持 逆变，那么这个 `handleDatas(SimpleData<Person>())` 是不允许的，虽然 `handleDatas` 中做的操作其实传 Person 进来也是可以的。

如果改成逆变

```
class SimpleData<in T> {

    private var t: T? = null

    fun set(t: T) {
        this.t = t
    }

// 逆变，T只能放在输入的位置，不能放在输出位置
//    fun get(): T? = t
}
```

这个时候 `handleDatas2(SimpleData<Person>())` 就是允许的，所以接受范围扩大了

## 总结

> 所以不管是协变还是逆变，他们的作用都是一种约定，有这个约定之后，就可以扩大值的接受范围，提高扩展性。

那么约定的内容是什么呢？


**out**: T 只能放在输出位置

**in**:  T 只能放在输入位置

```
fun test(t1: T): T {
    // xxx
}
```

t1 就是输入位置 in， 返回T 就是输出位置 out

## 在方法中使用

再看看一种情况，如果 `SimpleData<T>` 就是不支持协变或者逆变，那么可以修改 `handleDatas(data: SimpleData<out Person>)` 和 `handleDatas2(datas: SimpleData<in Student>)` 让这两个方法支持协变和逆变。

这样定义在方法上的有什么效果呢？

```
fun handleDatas(data: SimpleData<out Person>): Person? {
    // 不能使用set方法，修改data中的person，只能使用get方法
    // data.set(Person("p1"))
    return data.get()
}
```
协变之后，data的set方法是不允许调用的，只能使用data

```
fun handleDatas2(data: SimpleData<in Student>): Any? {
    "handleDatas2-> $data".logi(TAG)
    data.set(Student("s3"))
    // 这里不能返回 Student，只能返回 Any
    return data.get()
}
```
逆变之后，get方法是不能使用的，除非将返回值修改为 Any，因为Any是所有类的父类

## List默认是支持协变的

我们平时在使用的时候 `List<Person>` 一般我们都是可以传 `List<Student>` 的，为什么呢？

```
public interface List<out E> : Collection<E> {
    override val size: Int
    override fun isEmpty(): Boolean
    override fun contains(element: @UnsafeVariance E): Boolean
    override fun iterator(): Iterator<E>
    // xxx
}
```

因为集合类默认就是支持协变的

但是又有一个问题，`contains` 方法为什么可以将 E 放在输入的位置上，因为它加了注解 `@UnsafeVariance`，表示忽略输入位置的检查，方法自己会保证不对 element 做修改，这也是一种约定。

