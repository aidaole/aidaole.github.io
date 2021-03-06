---
layout: page
title: 算法4-排序总结
key: algorithm4-sort
tag: algorithm
sidebar:
  nav: algorithm
permalink: /algorithm/alogrithm4-sort
---

# 排序模板

根据算法4中，对排序公用的方法抽象出模板方法：

主要包含：

1. 所有排序数组以 `Comparable[]` 作为入参，不跟具体的类型想关联
2. sort抽象方法，每种排序自己实现
3. less（小于）和lessEqual （小于等于）排序中比较大小用这两个方法，不做值的对比

```java
/**
 * Sort用到的公用方法
 */
public abstract class AbstractSort {

    /**
     * 每种排序实现
     * @param arr
     */
    public abstract void sort(Comparable[] arr);

    /**
     * a和b比较，如果a小于b返回true，否则false
     * @param a
     * @param b
     * @return
     */
    protected boolean less(Comparable a, Comparable b) {
        return a.compareTo(b) < 0;
    }

    /**
     * a和b小于等于比较，如果a小于等于b返回true
     * @param a
     * @param b
     * @return
     */
    protected boolean lessEqual(Comparable a, Comparable b) {
        return a.compareTo(b) <= 0;
    }

    /**
     * 交换数组中index为i和j位置的元素
     * @param arr
     * @param i
     * @param j
     */
    protected void exch(Comparable[] arr, int i, int j) {
        if (i == j) return;
        Comparable a = arr[i];
        arr[i] = arr[j];
        arr[j] = a;
    }

    /**
     * 打印数组
     * @param arr
     */
    public void show(Comparable[] arr) {
        for (Comparable c : arr) {
            System.out.printf(c + " ");
        }
        System.out.println();
    }

    /**
     * 判断数组是否从小打到排序
     * @param arr
     */
    public void isSorted(Comparable[] arr) {
        for (int i = 1; i < arr.length; i++) {
            if (less(arr[i], arr[i - 1])) {
                System.out.println(false);
            }
        }
        System.out.println(true);
    }
}
```



# 冒泡排序

```java
public class BubbleSort extends AbstractSort {
    @Override
    public void sort(Comparable[] arr) {
        // 2. i递增直到数组最后
        for (int i = 0; i < arr.length; i++) {
            // 1. 从后往前依次比较，如果当前元素小于前一个元素则交换位置
            // 每次循环结束一个最小的元素放到 arr[i]的位置
            for (int j = arr.length - 1; j > i; j--) {
                if (less(arr[j], arr[j - 1])) {
                    exch(arr, j, j - 1);
                }
            }
        }
    }
}
```



# 选择排序

```java
public class SelectionSort extends AbstractSort {
    @Override
    public void sort(Comparable[] arr) {
        for (int i = 0; i < arr.length; i++) {
            int minIndex = i;
            // 1. 每次遍历数组，选择数组中值最小的minIndex元素，与第i个元素交换
            for (int j = i; j < arr.length; j++) {
                if (less(arr[j], arr[minIndex])) {
                    minIndex = j;
                }
            }
            // 2. 交换第i和minIndex元素
            exch(arr, i, minIndex);
        }
    }
}
```



# 插入排序

```java
public class InsertSort extends AbstractSort {
    @Override
    public void sort(Comparable[] arr) {
        for (int i = 1; i < arr.length; i++) {
            // 1. 从j开始往前比较，如果小于前一个数就交换。
            // 只需要与前一个数比较，如果数组基本是有序的，插入排序非常高效
            for (int j = i; j > 0 && less(arr[j], arr[j - 1]); j--) {
                exch(arr, j, j - 1);
            }
        }
    }
}
```



# 希尔排序

```java
// 希尔排序是插入排序的升级，先使数组在步长区间有序，减少插入排序的比较。在数据大的时候非常有效
public class ShellSort extends AbstractSort {
    @Override
    public void sort(Comparable[] arr) {
        int h = 1;
        while (h < arr.length / 3) h = h * 3 + 1; // 1, 4, 13, 40...
        // 步长依次递减，最终降为1
        while (h >= 1) {
            // 以步长h做插入排序
            for (int i = h; i < arr.length; i++) {
                for (int j = i; j >= h && less(arr[j], arr[j - h]); j -= h) {
                    exch(arr, j, j - h);
                }
            }
            h /= 3;
        }
    }
}
```



# 归并排序

```java
// 归并排序的优势在于对于任何数组都能保证n*log(n)的排序复杂度，缺点是需要使用额外的空间
public class MergeSort extends AbstractSort {

    // 使用同一个暂存交换空间
    private Comparable[] temp;

    @Override
    public void sort(Comparable[] arr) {
        temp = new Comparable[arr.length];
//        sort(arr)
        sort2(arr);
    }

    // 自顶向下（递归）
    private void sort(Comparable[] arr, int left, int right) {
        if (left >= right) return;
        int mid = left + (right - left) / 2;
        sort(arr, left, mid);
        sort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }

    // 自底向上
    public void sort2(Comparable[] arr) {
        for (int sz = 1; sz < arr.length; sz *= 2) {
            for (int lo = 0; lo < arr.length - sz; lo += sz * 2) {
                merge(arr, lo, lo + sz - 1, Math.min(lo + sz * 2 - 1, arr.length - 1));
            }
        }
    }

    /**
     * merge过程是将两个已经排序的数组合并到长度更长的一个数组中，时间复杂度为 n
     */
    private void merge(Comparable[] arr, int left, int mid, int right) {
        int i = left;
        int j = mid + 1;
        // 如果左边区域最大的arr[mid]小于右边区域最小的arr[j]，则不需要继续比较
        if (less(arr[mid], arr[j])) return;
        for (int k = left; k <= right; k++) {
            if (i > mid) temp[k] = arr[j++];
            else if (j > right) temp[k] = arr[i++];
            else temp[k] = less(arr[i], arr[j]) ? arr[i++] : arr[j++];
        }
        for (i = left; i <= right; i++) {
            arr[i] = temp[i];
        }
    }
}
```



# 快速排序

```java
// 三点优化：
// 1. 为避免数组是有序的，选取最后一个元素作为标准，最好是经过随机选择的数然后和最后一个交换作为标准
// 2. 如果数组中包含大量重复的数，应该在partition中分为三个部分，小于，等于，大于的三个部分。然后将小于和大于两部分继续切分。荷兰国旗问题
// 3. 当切分是小数组的时候，使用插入排序替换
public class QuickSort extends AbstractSort {
    @Override
    public void sort(Comparable[] arr) {
        sort(arr, 0, arr.length - 1);
    }

    // 常规分治递归
    private void sort(Comparable[] arr, int left, int right) {
        if (left >= right) return;
        // 优化1：选择随机值作为标准
        int randomIndex = new Random().nextInt(right - left) + left;
        exch(arr, left, randomIndex);
        // 优化3：替换为插入排序
        // if (right <= left+M) {InsertSort.sort(arr, left, right); return;}
        int lo = left;
        for (int i = lo; i <= right; i++) {
            if (lessEqual(arr[i], arr[right])) {
                exch(arr, i, lo++);
            }
        }
        int mid = lo - 1;
        sort(arr, left, mid - 1);
        sort(arr, mid + 1, right);
    }

    // 优化2：解决大量重复数据导致的效率低下，三切分
    private void sort2(Comparable[] arr, int left, int right) {
        if (left >= right) return;
        int lo = left, i = left + 1, gt = right;
        // 以第一个元素作为基准
        Comparable v = arr[left];
        while (i <= gt) {
            int cmp = arr[i].compareTo(v);
            if (cmp < 0) exch(arr, lo++, i++);
            if (cmp > 0) exch(arr, i, gt--);
            if (cmp == 0) i++;
        }
        sort(arr, left, lo - 1);
        sort(arr, gt + 1, right);
    }
}
```



# 堆排序

```java
// 堆排序是唯一一个保证查找和空间复杂度均衡的排序 N*log(N)
public class HeapSort extends AbstractSort {
    @Override
    public void sort(Comparable[] arr) {
        int N = arr.length - 1;
        // 构建大顶堆
        for (int k = N / 2; k >= 0; k--) {
            sink(arr, k, N);
        }
        // 将堆顶放到最后，0~N-1的位置继续构建成堆
        while (N > 0) {
            exch(arr, 0, N--);
            sink(arr, 0, N);
        }
    }

    // 下沉操作：在 i*2+1和i*2+2中选择一个更大的更位置i的交换，如果交换成功则继续下沉
    private void sink(Comparable[] arr, int i, int len) {
        while (i * 2 + 1 <= len) {
            int j = i * 2 + 1;
            if (j + 1 <= len && less(arr[j], arr[j + 1])) j++;
            if (!less(arr[i], arr[j])) break;
            exch(arr, i, j);
            i = j;
        }
    }
}
```

