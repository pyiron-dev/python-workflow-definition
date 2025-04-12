def get_dict(**kwargs):
    # NOTE: In WG, this will automatically be wrapped in a dict with the `result` key
    return {k: v for k, v in kwargs.items()}
    # return {'dict': {k: v for k, v in kwargs.items()}}


def get_list(**kwargs):
    return list(kwargs.values())


def get_kwargs(lst):
    return {t["targetPort"]: {"source": t["source"], "sourcePort": t["sourcePort"]} for t in lst}


def get_source_handles(edges_lst):
    source_handle_dict = {}
    for ed in edges_lst:
        if ed["source"] not in source_handle_dict.keys():
            source_handle_dict[ed["source"]] = [ed["sourcePort"]]
        else:
            source_handle_dict[ed["source"]].append(ed["sourcePort"])
    return {
        k: list(range(len(v))) if len(v) > 1 and all([el is None for el in v]) else v
        for k, v in source_handle_dict.items()
    }


def convert_nodes_list_to_dict(nodes_list):
    return {
        str(el["id"]): el["value"] if "value" in el else el["function"]
        for el in sorted(nodes_list, key=lambda d: d["id"])
    }
