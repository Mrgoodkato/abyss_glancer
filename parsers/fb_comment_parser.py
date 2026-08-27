FB_COMMENT_SHAPE = {
    "layer1": "data",
    "layer2": "node_v2",
    "layer3": "comet_sections",
    "layer4": "feedback",
    "layer5": "story",
    "layer6": "story_ufi_container",
    "layer7": "story",
    "layer8": "feedback_context",
    "layer8_1": "feedback_target_with_context", # Too lazy to number these again
    "layer9": "comment_list_renderer",
    "layer10": "feedback",
    "layer11": "comment_rendering_instance_for_feed_location",
    "layer12": "comments",
    "layer13": "edges"
}

def get_nodes_from_response(response_payload: list[dict])-> dict:
    nodes = []
    probe = {}
    for element in response_payload:
        if probe:
            break
        for layer_key, layer_val in FB_COMMENT_SHAPE.items():
            if layer_key == 'layer1':
                probe = element.get(layer_val)
                continue
            if not probe:
                print(f'FB probe failed getting node info on layer {layer_key} on key {layer_val}')
                break

            probe = probe.get(layer_val)

            if isinstance(probe, list):
                for node in probe:
                    nodes.append(node)
    
    return nodes


def parse_nodes_from_response(nodes: list[dict]):

    parsed_nodes = []

    idx = 0
    for node in nodes:
        if 'node' not in node.keys():
            continue
        node_payload = {}

        for n in node.get('node').keys():
            
            current_node = node.get('node')

            if n == "body":
                if current_node.get(n):
                    node_payload['comment_text'] = current_node.get(n).get('text')

            if n == "author":
                node_payload['author'] = current_node.get(n).get('name')
                node_payload['author_id_fb'] = current_node.get(n).get('id')
                node_payload['author_type_fb'] = current_node.get(n).get('__typename')

            if n == "created_time":
                node_payload['time'] = current_node.get('created_time')
        
        if node_payload:
            print(f'Parsed payload for node {idx}')
            parsed_nodes.insert(idx, node_payload)
            idx += 1
            continue

        print('No node payload parsed, continuing...')

    return parsed_nodes
