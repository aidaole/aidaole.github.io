# 学习资料

#### 学习算法 hello-Algo: https://github.com/krahets/hello-algo

#### 老刷题地址：https://github.com/aidaole/Algorithm

## Python刷题常用数据结构

### 数组

```python
nums = List[int] //数组int定义
num = nums[index] // 取数
```

### 链表

```python
class ListNode:
    def __init__(self, val = 0, next = None):
      self.val = val
      self.next = next

linedList : Optional[ListNode] /// Optional 表示可为ListNode, 也可为None, 
```

### map (dict)

```python
map = {}
map = {"key": "value"}

if (key in map) /// 判断map中有某个key
if (value in map.values()) /// 判断map中有某个value
```