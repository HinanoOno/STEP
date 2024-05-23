import sys
from hash_table import HashTable
from typing import List

# Implement a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library like collections.OrderedDict). The goal is
#       to implement the data structure yourself!


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.pre = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    # Add a node to the head of the linked list
    def insert(self, node: Node):
        if self.head == None:
            self.head = node
            self.tail = node
            self.length += 1
        else:
            self.head.pre = node
            node.next = self.head
            self.head = node
            self.length += 1

    # Remove the tail of the linked list
    def remove_tail(self):
        if self.tail.pre == None:
            self.tail = None
        else:
            self.remove(self.tail)
        

    # Remove a node from the linked list
    def remove(self, node: Node):
        if self.head == node:
            self.head = node.next
            self.length -= 1
        elif self.tail == node:
            self.tail = node.pre
            node.pre.next = None
            self.length -= 1
        else:
            node.pre.next = node.next
            node.next.pre = node.pre
            self.length -= 1

    # Move a node to the head of the linked list
    def move_to_head(self, node: Node):
        self.remove(node)
        self.insert(node)

class Cache:
    # Initialize the cache.
    # |n|: The size of the cache.
    def __init__(self, n):
        self.hash_table = HashTable()
        self.linked_list = LinkedList()
        self.max_size = n
        self.size = 0

    # Access a page and update the cache so that it stores the most recently
    # accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url: str, contents: str):
        item, isExist = self.hash_table.get(url)
        if isExist:
            self.linked_list.move_to_head(item)
        else:
            if self.size >= self.max_size:
                old_node = self.linked_list.tail
                self.linked_list.remove_tail()
                self.hash_table.delete(old_node.key)
                self.size -= 1
            new_node = Node(url, contents)
            self.hash_table.put(url, new_node)
            self.linked_list.insert(new_node)
            self.size += 1

    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    def get_pages(self) -> List[str]:
        urls = []
        node = self.linked_list.head
        while node:
            urls.append(node.key)
            node = node.next
            
        return urls


def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)

    # Initially, no page is cached.
    assert cache.get_pages() == []

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]

    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["b.com", "a.com"]

    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]

    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]

    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]

    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "f.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "e.com", "f.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Tests passed!")


if __name__ == "__main__":
    cache_test()
    
    