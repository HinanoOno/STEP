import sys
import collections
import time

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


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    
    # breadth first search
    # |start|: start point of the search
    # |goal|: goal point of the search
    def bfs(self,start,goal):
        visited = {}
        previous = {}
        queue = collections.deque()
        queue.append(start)
        visited[start] = True
        previous[start] = None
        while len(queue):
            node = queue.popleft()
            if node == goal:
                return previous
            for child in self.links[node]:
                if not child in visited:
                    visited[child] = True
                    previous[child] = node
                    queue.append(child)
        return previous
    

    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        for id, title in self.titles.items():
            if title == start:
                start_id = id
            if title == goal:
                goal_id = id
                
        previous = self.bfs(start_id,goal_id)
        print("The shortest path from %s to %s is:" % (start, goal))
        self.print_path(start_id, goal_id, previous)
        
    
    #　print the path from start to goal
    def print_path(self, start, goal, previous):
        path = []
        node = goal
        path.append(node)
        while previous[node]:
            node = previous[node]
            path.append(node)
        path.reverse()
        print(" -> ".join([self.titles[node] for node in path]))
        print()
        
        
        
        
        
    
    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        max_iter = 100
        epsilon = 0.01
        
        node_values = {}
        for id in self.titles.keys():
            node_values[id] = 1.0
            
        new_node_values = {}
        for id in self.titles.keys():
            new_node_values[id] = 0
            
        for i in range(max_iter):
            start = time.time()
            next_node_values = new_node_values.copy() 
            
            all_value = 0
            for id in self.titles.keys():
                children = self.links[id]
                if len(children) == 0:
                    all_value +=  node_values[id] / len(self.titles)
                else:
                    child_value = 0.85*node_values[id]/ len(children)
                    
                    for child in children:
                        next_node_values[child] += child_value
                    
                    all_value += 0.15*node_values[id]/len(self.titles)
                    
            for id in self.titles.keys():
                next_node_values[id] += all_value
            
            # if all(abs(node_values[id] - next_node_values[id]) < 0.01 for id in self.titles.keys()):
            #     break
            if(sum((node_values[id] - next_node_values[id])**2 for id in self.titles.keys()) < epsilon ):
                break
                
            node_values = next_node_values   
             
            sum_rank_value = sum(next_node_values.values())
            
            end = time.time()
            
            print(i, sum_rank_value, end - start)
    
        return self.print_most_popular_pages(node_values)
    
    def print_most_popular_pages(self,node_values):
        print("The most popular pages are:")
        
        node_values = sorted(node_values.items(), key=lambda x: x[1], reverse=True)
        for i in range(min(10, len(node_values))):
            print(self.titles[node_values[i][0]], node_values[i][1])
            
        print()
        



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia.find_longest_titles()
    wikipedia.find_most_linked_pages()
    #wikipedia.find_shortest_path("渋谷", "小野妹子")
    wikipedia.find_most_popular_pages()
