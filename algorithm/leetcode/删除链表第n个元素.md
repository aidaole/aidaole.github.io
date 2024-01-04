# 19. 删除链表的倒数第 N 个结点

给你一个链表，删除链表的倒数第 n 个结点，并且返回链表的头结点。

```
class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        // 前面插入一个代理头节点，防止越界
        ListNode newHead = new ListNode(1, head);
        ListNode p = newHead;
        ListNode q = newHead;
        // 先将p前移n位
        while(n>0){
            p = p.next;
            n--;
        }
        // 双指针一起向前
        while(p.next != null){
            q = q.next;
            p = p.next;
        }
        q.next = q.next.next;
        return newHead.next;
    }
}
```