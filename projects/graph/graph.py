"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy
from collections import OrderedDict


class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()  # set of edges from this vert

    def add_vertices(self, vertices):
        for vertex_id in vertices:
            self.add_vertex(vertex_id)

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        have_1 = v1 in self.vertices
        have_2 = v2 in self.vertices
        if (have_1 and have_2):
            self.vertices[v1].add(v2)
            return
        no_2 = f"No '{str(v2)}' vertex in graph" if (
            have_1 and not have_2) else False
        no_1 = f"No '{str(v1)}' vertex in graph" if (
            have_2 and not have_1) else False
        no = f"No '{str(v1)}' or '{str(v2)}' vertex in graph" if (
            not have_1 and not have_2) else False
        err = no or no_1 or no_2
        raise KeyError(err)

    def add_edges(self, v1, edges):
        for v2 in edges:
            self.add_edge(v1, v2)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        q = Queue()
        q.enqueue(starting_vertex)
        visited = OrderedDict()  # boolean matrix
        # loop...
        while q.size() > 0:  # for every vert,
            vertex_id = q.dequeue()  # obtained from g,
            if not visited.get(vertex_id, False):  # if not already visited,
                visited[vertex_id] = True  # mark as visited
                adjacent = self.get_neighbors(
                    vertex_id)  # find adjacent vertices
                for neighbor in adjacent:  # for every adjacent vertice
                    q.enqueue(neighbor)  # push onto stack
        # finally,
        #   cast the vistied vertices into
        #    the format expected by tests.
        print("\n".join(list(map(str, visited))))

    def dft(self, starting_vertex, rType=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # stack = [starting_vertex]  # create new stack containing the head of g
        stack = Stack()
        stack.push(starting_vertex)
        visited = OrderedDict()  # boolean matrix
        # loop...
        while stack.size() > 0:  # for every vert,
            vertex_id = stack.pop()  # obtained from g,
            if not visited.get(vertex_id, False):  # if not already visited,
                visited[vertex_id] = True  # mark as visited
                adjacent = self.get_neighbors(
                    vertex_id)  # find adjacent vertices
                for neighbor in adjacent:  # for every adjacent vertice
                    stack.push(neighbor)  # push onto stack
        # finally,
        #   cast the vistied vertices into
        #    the format expected by tests.
        if not rType:
            print("\n".join(list(map(str, visited))))
            return
        return rType(map(str, visited))

    def dft_recursive(self, starting_vertex, visited=None, rList=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        if visited is None:
            visited = OrderedDict()
        nbrs = self.get_neighbors(starting_vertex)
        if len(visited) == 0:
            visited[starting_vertex] = True
            if rList is None:
                print(starting_vertex)
            else:
                rList.append(starting_vertex)
        for nbr in nbrs:
            if not visited.get(nbr, False):
                visited[nbr] = True
                if rList is None:
                    print(nbr)
                else:
                    rList.append(nbr)
                self.dft_recursive(nbr, visited, rList)
        return rList

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        q = Queue()
        q.enqueue([starting_vertex])
        # loop...
        while q.size() > 0:
            cur = q.dequeue()  # the current path
            tail = cur[-1]  # visiting
            if tail == destination_vertex:
                return cur  # found destination, return path
            nbrs = self.get_neighbors(tail)  # get adjacent vertices
            for vertex_id in nbrs:
                clone = list(cur)
                clone.append(vertex_id)
                q.enqueue(clone)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        travels = self.dft(starting_vertex, rType=list)
        endpoint = travels.index(str(destination_vertex))
        route = travels[:endpoint]
        route.append(destination_vertex)
        return list(map(int, route))

    def dfs_recursive(self, starting_vertex, destination_vertex, travels=None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if travels is None:
            travels = self.dft(starting_vertex, rType=list)
            self.dfs_recursive(starting_vertex, destination_vertex, travels)
        endpoint = travels.index(str(destination_vertex))
        route = travels[:endpoint]
        route.append(destination_vertex)
        return list(map(int, route))


if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
