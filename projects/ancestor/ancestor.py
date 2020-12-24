from graph import Graph
from util import Stack


def earliest_ancestor(ancestors, starting_node):
    g = Graph()
    for parent, child in ancestors:
        g.add_vertex(parent)
        g.add_vertex(child)
        g.add_edge(child, parent)
    routes = Stack()
    routes.push([starting_node])
    distance = 1
    ancestor = -1
    while routes.size() > 0:
        path = routes.pop()
        visiting = path[-1]
        parents = g.get_neighbors(visiting)
        if len(parents) == 0:
            if distance < len(path):
                distance = len(path)  # how far we've traveled.
                ancestor = visiting  # who we are visiting.
            elif distance == len(path):
                # (equal distance)
                #    choose lowest vertex_id
                ancestor = min(visiting, ancestor)
        else:
            for c in parents:
                # add each parent as new route
                clone = list(path)
                clone.append(c)
                routes.push(clone)
    return ancestor
