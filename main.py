import json as js
from CParser import parse_c_file


def create_node(json_c_file, fn_name):
    json_c_file = js.loads(json_c_file)

    variable_dic = {}

    id_node = 0
    for i in json_c_file["ext"]:
        # complexity depends on the number of function and variable/operation
        #this code is not generic, it's a test
        if i["decl"]["name"] == fn_name:
            for j in i["body"]["block_items"]:
                if j["_nodetype"] == "Decl":
                    variable_dic[id_node] = [j["name"], j["name"] + "=" + j["init"]["value"]]
                    id_node += 1
                elif j["_nodetype"] == "Assignment":
                    expr = ''
                    variable_name = j["lvalue"]["name"]
                    expr += variable_name
                    expr += j["op"]
                    if j["rvalue"]["left"]["_nodetype"] == "ID":
                        expr += j["rvalue"]["left"]["name"]
                    else:
                        expr += j["rvalue"]["left"]["value"]
                    expr += j["rvalue"]["op"]
                    if j["rvalue"]["right"]["_nodetype"] == "ID":
                        expr += j["rvalue"]["right"]["name"]
                    else:
                        expr += j["rvalue"]["right"]["value"]
                    variable_dic[id_node] = [variable_name, expr]
                    id_node += 1
                else:
                    pass

    return variable_dic


def create_edge(variable_dic):
    output_list = []
    #complexity O(n^2)
    for i in variable_dic:
        for j in range(i+1, len(variable_dic)):
            if variable_dic[i][0] == variable_dic[j][0]:
                output_list.append([i, j])
    return output_list


def create_final_json(variable_dic, output_list):
    #complexity O(len(variable_dic)
    nodes = [{"id": i, "var_name": variable_dic[i][0], "expr": variable_dic[i][1]} for i in variable_dic]
    # complexity O(len(output_list)
    edges = [{"src": i[0], "dst": i[1]} for i in output_list]
    node = {"nodes": nodes}
    edge = {"edges": edges}
    final_output = [node, edge]
    return js.dumps(final_output, sort_keys=True, indent=4)


def variable_graph(path, fn_name):
    json_c_file = parse_c_file(path)
    variable_dic = create_node(json_c_file, fn_name)
    output_list = create_edge(variable_dic)
    json_output = create_final_json(variable_dic, output_list)
    return json_output


if __name__ == '__main__':
    variable_graph('input.c', "foo")
