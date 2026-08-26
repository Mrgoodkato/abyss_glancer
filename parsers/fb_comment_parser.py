def get_nodes_from_response(response_payload: list[dict])-> dict:

    nodes = []

    for element in response_payload:
        if not isinstance(element, dict): continue
        node = _recursive_catcher(element)
        if not isinstance(node, dict): continue
        if "body" in node.keys():
            nodes.append(node)

    return nodes

def parse_nodes_from_response(nodes: list[dict]):

    parsed_nodes = []

    idx = 0
    for node in nodes:
        for n in node.keys():
            node_payload = {}
            current_node = node.get(n)

            if n == "body":
                node_payload['comment_text'] = current_node.get('text')

            if n == "author":
                node_payload['author'] = current_node.get('name')
                node_payload['author_id_fb'] = current_node.get('id')
                node_payload['author_type_fb'] = current_node.get('_typename')

            if n == "created_time":
                node_payload['time'] = current_node.get('created_time')
        parsed_nodes.insert(idx, node_payload)
        idx += 1

    return parsed_nodes

def _recursive_catcher(payload_element)-> dict:
    if not isinstance(payload_element, dict):
        return
    for level_key in payload_element.keys():
        if level_key == "node":
            print('Found node!')
            return payload_element.get(level_key)
        print(level_key)
        _recursive_catcher(payload_element.get(level_key))