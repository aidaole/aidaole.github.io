from typing import List, Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def quickSort(nums, low, high):
    if low < high:
        p = partion(nums, low, high)
        quickSort(nums, low, p - 1)
        quickSort(nums, p + 1, high)
    return nums

def partion(nums, low, high):
    pivot = nums[high]
    i = low - 1
    for j in range(low, high):
        if nums[j] < pivot:
            i += 1
            nums[i], nums[j] = nums[j], nums[i]
    nums[i + 1], nums[high] = nums[high], nums[i + 1]
    return i + 1

if __name__ == "__main__":
    nums = [3, 2, 1, 5, 8, 9, 1, 2, 4]
    result = quickSort(nums, 0, len(nums) - 1)
    print(result)
