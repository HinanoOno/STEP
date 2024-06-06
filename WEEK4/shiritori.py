import sys
from collections import deque
import time
import random
import sys
sys.setrecursionlimit(3000)


class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()

    # check if the previous word and the next word are shiritori
    # ex) check_shiritori("apple", "elephant") -> True
    def check_shiritori(self, title1, title2):
        return title1[-1] == title2[0]
    
    
    def dfs_shiritori(self, node, visited,parents):
        path = [node]
        
        if(self.links[node]==[]):
            return path
        
        visited.add(node)
        
        max_path = []
        for child in self.links[node]:
            if(child in visited) or (not self.check_shiritori(self.titles[node],self.titles[child])):
                continue
            parents[child]=node
            visited.add(child)
            child_path=self.dfs_shiritori(child,visited, parents)
            if len(child_path)>len(max_path):
                max_path=child_path
        path+=max_path

        return path
    
    #　find longer shiritori paths
    def find_longer_shiritori_paths(self, max_iters=10000):
        max_path = []
        
        for i in range(max_iters):
            start = time.time()
            node = random.choice(list(self.titles.keys()))
            
            path = self.dfs_shiritori(node, set(), {})
            
            if len(path) > len(max_path):
                max_path = path
            end = time.time()
            
            print(max_path, end - start)
        return max_path
    
    

    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    
    path = wikipedia.find_longer_shiritori_paths()
    print(path)
    print([wikipedia.titles[node] for node in path])
    print(len(path))
   