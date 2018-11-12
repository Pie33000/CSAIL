import json as js
from c_parser import parse_c_file
from ast_parser import AstParser


def create_edge(variable_dic):
    """

    :param variable_dic: a dictionary that includes variable declarations and binary operations
    :return: a list of edges
    """
    output_list = []
    #complexity O(n^2)
    print(variable_dic)
    for i in variable_dic:
        for j in range(i+1, len(variable_dic)):
            if variable_dic[i][0] == variable_dic[j][0]:
                output_list.append([i, j])
    return output_list


def create_final_json(variable_dic, output_list):
    """
    create_final_json : create a json with nodes and edges
    :param variable_dic: a dictionary that includes variable declarations and binary operations
    :param output_list: a list of edges
    :return: a json file
    """
    #complexity O(len(variable_dic)
    nodes = [{"id": i, "var_name": variable_dic[i][0], "expr": variable_dic[i][1]} for i in variable_dic]
    # complexity O(len(output_list)
    edges = [{"src": i[0], "dst": i[1]} for i in output_list]
    node = {"nodes": nodes}
    edge = {"edges": edges}
    final_output = [node, edge]
    return js.dumps(final_output, sort_keys=True, indent=4)


def variable_graph(path, fn_name):
    """

    :param path: path of your C file
    :param fn_name: name of your function in your C file
    :return:
    """
    json_c_file = parse_c_file(path)
    ast = AstParser()
    ast.parse_c_file(path, fn_name)
    output_list = create_edge(ast.variables_dic)
    json_output = create_final_json(ast.variables_dic, output_list)
    return json_output


if __name__ == '__main__':
    print(variable_graph('input.c', "test4"))