from typing import List, Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        jinwei = 0
        result = ListNode(-1)
        p = result
        sum = 0
        while l1 or l2 or jinwei > 0:
            if l1:
                sum += l1.val
                l1 = l1.next
            if l2:
                sum += l2.val
                l2 = l2.next
            sum += jinwei
            if sum > 0:
                p.next = ListNode(sum // 10)
                p = p.next
                jinwei = sum % 10
        return result.next



if __name__ == "__main__":
    result = Solution().twoSum(nums = [1,2,3,4,5], target = 5)
    print(result)
