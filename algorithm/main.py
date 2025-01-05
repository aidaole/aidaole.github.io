from typing import List, Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    pass



if __name__ == "__main__":
    result = Solution().threeSum(nums = [1,2,3,4,5], target = 5)
    print(result)
