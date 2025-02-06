# 学习资料

#### 学习算法 hello-Algo: https://github.com/krahets/hello-algo

#### 老刷题地址：https://github.com/aidaole/Algorithm

## Python刷题常用数据结构

### 数组

```python
nums = [] # 一维数组
nums = [0] * n # 一维数组, 带初始化
nums = [[0]*n for _ in range(n)] # 二维数组
num = nums[index] # 取

nums.append(10) # 末尾添加
nums.insert(1, 10) # 指定位置插入
nums.extend([1,2,3]) # 数组合并

del nums[1] # 删除指定位置数字
nums.remove(10) # 删除数字, 只删除第一个匹配上的
num = nums.pop(1) # 删除位置1数字, 并返回
nums.clear() # 清理数组

n = len(nums) # 数组长度
if 10 in nums: # 判断10 是否在数组中
slice_list = nums[1:3] # 取索引 1, 2 的数字, 后面是开区间
reverseList = nums.reverse() # 反转
nums[::-1] # 反转, 同reverse
nums.sort() # 升序
nums.sort(reverse=True) # 降序
sorted(nums) # 使用排序函数
nums[2:6] = sorted(nums[2:6]) # 只对数组中2~5索引的位置进行排序

nums.copy() # 浅拷贝
nums[:] # 切片, 等同于浅拷贝
copy.deepcopy(nums) # 深拷贝

float('-inf') # 负无穷大
float('inf') # 正无穷大
```

### 字符串

```python
sorted_s = "".join(sorted(s)) # 将字符串按字典序排序
```

### 链表

```python
class ListNode:
    def __init__(self, val = 0, next = None):
      self.val = val
      self.next = next

linedList : Optional[ListNode] # Optional 表示可为ListNode, 也可为None, 
```

### map (dict)

```python
map = {}
map = {"key": "value"}

if (key in map) # 判断map中有某个key
if (value in map.values()) # 判断map中有某个value
```

### set

```
s = set()
s.put(value)
s.remove(value)
```