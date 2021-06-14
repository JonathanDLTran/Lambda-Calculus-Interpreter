from ast import (
    Expr,
    IntValue,
    BoolValue,
    StrValue,
    Assign,
    Bop,
    For,
    IfThenElse,
    While,
    Return,
    Ignore,
    Function,
    Program,)

from graph_classes import (
    Node, Edge
)

from dot_generator import (
    gen_dot
)


# --------- CONSTANTS ---------


# Testing mode when invoked from command line
TESTING = True
# Global variable for unique node numbering
NODE_NUMBER = 0
# Special Node for Exiting Early with Reeturn
EARLY_RETURN_NODE_NUMBER = -1
# Special number for indicating a function
FUNCTION_INDICATOR = -2


# --------- UTILITY FUNCTIONS ---------


def gen_node_number():
    """
    Generates unique node number each time it is called.
    Utilizes global state.
    """
    global NODE_NUMBER
    NODE_NUMBER += 1
    return NODE_NUMBER


def is_basic(ast_node):
    """
    True iff AST node can be combined in a basic block.
    """
    assert isinstance(ast_node, Expr)
    if type(ast_node) == Assign:
        return True
    elif type(ast_node) == Ignore:
        return True
    return False


# --------- GENERATION FUNCTIONS ---------


def gen_return(ast_return):
    """
    Generates CFG for an returns Statement AST node
    """
    assert type(ast_return) == Return

    return_node_num = gen_node_number()
    return_node = Node(return_node_num, [str(ast_return)], final=True)
    # make exit node special number -1 as it should not connect to anything
    early_return_node = Node(EARLY_RETURN_NODE_NUMBER, [])
    return return_node, early_return_node, [return_node], []


def gen_if(ast_if):
    """
    Generates CFG for an If Statement AST node
    """
    assert type(ast_if) == IfThenElse

    if_guard, if_body = ast_if.get_if_pair()
    elif_guards, elif_bodies = ast_if.get_elif_pair_list()
    else_body = ast_if.get_else()

    init = None
    _exit = None
    nodes = []
    edges = []

    dummy_node_num = gen_node_number()
    dummy_node = Node(dummy_node_num, [])

    start_body, end_body, body_nodes, body_edges = gen_bodies(if_body)
    assert type(body_nodes) == list
    assert type(body_edges) == list

    exit_node_num = gen_node_number()
    exit_node = Node(exit_node_num, [])

    init = dummy_node
    _exit = exit_node
    nodes += [dummy_node] + body_nodes
    edges += [Edge(dummy_node, start_body, [str(if_guard)])] + \
        body_edges + [Edge(end_body, exit_node, [])]

    if elif_guards != []:
        for guard, body in zip(elif_guards, elif_bodies):
            start_body, end_body, body_nodes, body_edges = gen_bodies(
                body)
            assert type(body_nodes) == list
            assert type(body_edges) == list

            nodes += body_nodes
            edges += [Edge(dummy_node, start_body,
                           [f"Else: {str(guard)}"]), Edge(end_body, exit_node, [])]

    if else_body != None:
        start_body, end_body, body_nodes, body_edges = gen_bodies(else_body)
        assert type(body_nodes) == list
        assert type(body_edges) == list

        nodes += body_nodes
        edges += [Edge(dummy_node, start_body,
                       [f"Else: !{str(if_guard)}"]), Edge(end_body, exit_node, [])]

    if elif_guards == [] and else_body == None:
        edges += [Edge(dummy_node, exit_node, [f"Else: !{str(if_guard)}"])]

    return init, _exit, nodes, edges


def gen_while(ast_while):
    """
    Generates CFG for a While Loop AST node
    """
    assert type(ast_while) == While

    guard = ast_while.get_guard()
    body = ast_while.get_body()

    dummy_node_num = gen_node_number()
    dummy_node = Node(dummy_node_num, [str(guard)])

    start_body, end_body, body_nodes, body_edges = gen_bodies(body)
    assert type(body_nodes) == list
    assert type(body_edges) == list

    exit_node_num = gen_node_number()
    exit_node = Node(exit_node_num, [])

    nodes = [dummy_node] + body_nodes + [exit_node]
    edges = [Edge(dummy_node, start_body, ["True"])] + \
        body_edges + \
        [Edge(end_body, dummy_node, []),
         Edge(dummy_node, exit_node, ["False"])]

    return dummy_node, exit_node, nodes, edges


def gen_for(ast_for):
    """
    Generates Control Flow Graph for a For Loop AST node
    """
    assert type(ast_for) == For

    index_var = ast_for.get_index()
    from_int = ast_for.get_from()
    end_int = ast_for.get_end()
    by_int = ast_for.get_by()
    body = ast_for.get_body()

    set_idx = f"{index_var} = {from_int}"
    init_node_num = gen_node_number()
    init_node = Node(init_node_num, [set_idx])

    guard_node_num = gen_node_number()
    guard_node = Node(guard_node_num, [])

    start_body, end_body, body_nodes, body_edges = gen_bodies(body)
    assert type(body_nodes) == list
    assert type(body_edges) == list

    incr_node_num = gen_node_number()
    incr_idx = f"{index_var} += {by_int}"
    incr_node = Node(incr_node_num, [incr_idx])

    exit_node_num = gen_node_number()
    exit_node = Node(exit_node_num, [])

    nodes = [init_node, guard_node] + body_nodes + [incr_node, exit_node]
    edges = [Edge(init_node, guard_node, []),
             Edge(guard_node, start_body, [f"{index_var} <= {end_int}"])] + \
        body_edges + \
        [Edge(end_body, incr_node, []),
         Edge(incr_node, guard_node, []),
         Edge(guard_node, exit_node, [f"{index_var} > {end_int}"])]

    return init_node, exit_node, nodes, edges


def gen_function(ast_function):
    """
    Generates a CFG from List of AST nodes corresponding to a function definition
    """
    assert type(ast_function) == Function
    bodies_list = ast_function.get_body()
    start, end, nodes, edges = gen_bodies(bodies_list)
    # set extra nodes for function
    extra_top = Node(FUNCTION_INDICATOR, [])
    extra_bottom = Node(FUNCTION_INDICATOR, [])
    # set last node to be a return out of function
    end.set_final(True)
    return extra_top, extra_bottom, nodes, edges


def gen_program(ast_program):
    """
    Generates a CFG from List of AST nodes corresponding to a program
    """
    assert type(ast_program) == Program
    bodies_list = ast_program.get_phrases()
    return gen_bodies(bodies_list)


def gen_basic(ast_node_list):
    """
    Generates a Basic Block CFG from List of AST nodes corresponding to basic block expressions
    """
    assert type(ast_node_list) == list

    single_node_num = gen_node_number()
    stmt = "\n".join(list(map(lambda n: str(n), ast_node_list)))
    single_node = Node(single_node_num, [stmt])
    return single_node, single_node, [single_node], []


def gen_bodies(ast_node_list):
    """
    Generates a Body CFG from List of AST nodes corresponding to body expressions
    """
    assert type(ast_node_list) == list

    # pass in empty list of ast nodes
    if ast_node_list == []:
        empty_node_num = gen_node_number()
        empty_node = Node(empty_node_num, [])
        return empty_node, empty_node, [empty_node], []

    # formal base case: only 1 node
    if len(ast_node_list) == 1:
        node = ast_node_list[0]
        if is_basic(node):
            return gen_basic([node])
        return gen_cfg(node)

    # recursive case: multiple ast nodes
    # grab basic block(s) at front
    idx = 0
    while idx < len(ast_node_list) and is_basic(ast_node_list[idx]):
        idx += 1

    # handle basic block or first part
    first_init, first_exit, first_nodes, first_edges = None, None, None, None
    if idx == 0:
        first_init, first_exit, first_nodes, first_edges = gen_cfg(
            ast_node_list[idx])
    else:
        first_init, first_exit, first_nodes, first_edges = gen_basic(
            ast_node_list[:idx])

    # recurse on end
    final_init, final_exit, final_nodes, final_edges = gen_bodies(
        ast_node_list[idx + 1:])

    # combine parts
    init = first_init
    _exit = final_exit
    nodes = first_nodes + final_nodes
    edges = first_edges + [Edge(first_exit, final_init, [])] + final_edges

    return init, _exit, nodes, edges


def gen_cfg(ast_node):
    assert isinstance(ast_node, Expr)
    if type(ast_node) == Program:
        return gen_program(ast_node)
    elif type(ast_node) == Function:
        return gen_function(ast_node)
    elif type(ast_node) == For:
        return gen_for(ast_node)
    elif type(ast_node) == While:
        return gen_while(ast_node)
    elif type(ast_node) == IfThenElse:
        return gen_if(ast_node)
    elif type(ast_node) == Return:
        return gen_return(ast_node)
    else:
        raise RuntimeError(f"Unrecognized Ast Node {ast_node}.")


def gen_cfg_main(ast_node):
    """
    Entry Function to Generate Control Flow Graph
    """
    first, last, nodes, edges = gen_cfg(ast_node)
    final_edges = []
    for e in edges:
        assert type(e) == Edge
        start = e.get_start()
        end = e.get_end()
        # filter out early returns
        if start.get_num() == EARLY_RETURN_NODE_NUMBER:
            continue
        # remove function nodes
        elif start.get_num() == FUNCTION_INDICATOR:
            continue
        elif end.get_num() == FUNCTION_INDICATOR:
            continue
        else:
            final_edges.append(e)
    return nodes, final_edges


def main():
    pass


def test():
    """
    Test Function 
    """
    stmt = Program(
        [Function("f", [],
                  [For("i", 1, 10, 1,
                       [Assign("x", IntValue(3)),
                        Assign("x", IntValue(4)),
                           IfThenElse(BoolValue(True), []),
                           While(BoolValue(True),
                                 [Return(IntValue(3))]),
                           Assign("x", IntValue(5))])]),
         Function("g", [],
                  [Assign("x", IntValue(3))]),
         Assign("x", IntValue(1))])
    nodes, edges = gen_cfg_main(stmt)
    gen_dot(nodes, edges)


if __name__ == "__main__":
    if TESTING:
        test()
    else:
        main()
