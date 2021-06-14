from graphviz import Digraph

from graph_classes import (
    Node, Edge
)


def gen_dot(nodes, edges):
    """
    Generates Dot Graph from Control Flow Graph Data Structure representation
    """
    assert type(nodes) == list
    assert len(nodes) > 0
    assert type(edges) == list
    assert len(edges) > 0

    dot = Digraph(comment='Control Flow Graph')
    for n in nodes:
        assert type(n) == Node
        is_final = n.get_final()
        if is_final:
            # turn on double circle for final nodes
            dot.attr('node', shape='doublecircle')
        dot.node(str(n.get_num()), str(n))
        if is_final:
            # turn off double circle again to standard mode
            dot.attr('node', shape='circle')

    for e in edges:
        assert type(e) == Edge
        dot.edge(
            f"{e.get_start().get_num()}", f"{e.get_end().get_num()}", label=str(e))

    print(dot.source)
    dot.render('cfg.gv', view=True)


def main(node):
    """
    Main Method for Using DOT Generation
    """
    return gen_dot(node)


def test():
    """
    Test class taken from graphviz documentation
    """
    dot = Digraph(comment='Test Control Flow Graph')
    dot.node('A', 'King Arthur')
    dot.node('B', 'Sir Bedevere the Wise')
    dot.node('L', 'Sir Lancelot the Brave')

    dot.edges(['AB', 'AL'])
    dot.edge('B', 'L', constraint='false')
    print(dot.source)
    dot.render('round-table.gv', view=True)


if __name__ == "__main__":
    test()
