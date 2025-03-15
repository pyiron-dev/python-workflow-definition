import json
from importlib import import_module
from inspect import isfunction


from python_workflow_definition.shared import get_dict, get_list, get_kwargs, get_source_handles
from python_workflow_definition.purepython import resort_total_lst, group_edges, get_value


def load_workflow_json(file_name, exe):
    with open(file_name, "r") as f:
        content = json.load(f)

    edges_new_lst = content["edges"]
    nodes_new_dict = {}
    for k, v in content["nodes"].items():
        if isinstance(v, str) and "." in v:
            p, m = v.rsplit('.', 1)
            mod = import_module(p)
            nodes_new_dict[int(k)] = getattr(mod, m)
        else:
            nodes_new_dict[int(k)] = v

    total_lst = group_edges(edges_new_lst)
    total_new_lst = resort_total_lst(total_lst=total_lst, nodes_dict=nodes_new_dict)

    result_dict = {}
    last_key = None
    for lst in total_new_lst:
        node = nodes_new_dict[lst[0]]
        if isfunction(node):
            kwargs = {
                k: get_value(result_dict=result_dict, nodes_new_dict=nodes_new_dict, link_dict=v)
                for k, v in lst[1].items()
            }
            result_dict[lst[0]] = exe.submit(node, **kwargs)
            last_key = lst[0]

    return result_dict[last_key]
