# 7b each layer runtime mem (512) 9043968 Bytes
# 7b each layer mem 404750336, tok_embeddings output 262144000
# 7b time A10 each layer 1s
# emb 0.095ms
# layers 1.02ms
# norm 0.124ms
# output 0.648ms
# 1 1.288ms
# 2 2.267ms
# 4 4.274ms
# 8 8.281ms
# 16 16.244ms
# 32 32.233ms
from typing import List, Tuple, Dict, Any, Set

# spec


def get_model_layers(model_name: str) -> List[str]:
    # return layer_name
    if model_name == "llama-2-7b-chat-slice":
        return ["llama-2-7b-chat-slice/tok_embeddings",
                *[f"llama-2-7b-chat-slice/layers.{i}" for i in range(32)],
                "llama-2-7b-chat-slice/norm", "llama-2-7b-chat-slice/output"]
    if model_name == "llama-2-70b-chat-slice":
        return ["llama-2-70b-chat-slice/tok_embeddings",
                *[f"llama-2-70b-chat-slice/layers.{i}" for i in range(80)],
                "llama-2-70b-chat-slice/norm", "llama-2-70b-chat-slice/output"]
    raise NotImplementedError

# print(get_model_layers("llama-2-70b-chat-slice"))


def parse_layer_name(layer_name: str):
    s = layer_name.split('/')
    return s[0], s[1]


def get_mem_consumption(full_layer_name: str) -> (float, float):  # return (model_mem, inference_mem)  Bytes
    model_name, layer_name = parse_layer_name(full_layer_name)
    if model_name.startswith("llama-2-7b"):
        if layer_name == "tok_embeddings":
            return (262144000, 0)
        elif layer_name.startswith("layer"):
            return (404750336, 8388608)
        elif layer_name == "norm":
            return (8866, 0)
        elif layer_name == "output":
            return (262144000, 0)
        else:
            raise NotImplementedError("Unknown layers")
    elif model_name.startswith("llama-2-70b"):
        if layer_name == "tok_embeddings":
            return (524288000, 0)
        elif layer_name.startswith("layer"):
            return (1711276032, 2097152)
        elif layer_name == "norm":
            return (17058, 0)
        elif layer_name == "output":
            return (524288000, 0)
        else:
            raise NotImplementedError("Unknown layers")

    raise NotImplementedError


def get_gpu_total_mem(gpu_type: str) -> float:
    # return mem
    if gpu_type == "A10G":
        return 23827316736
    if gpu_type == "A100":
        return 84986691584
    raise NotImplementedError


def get_computation_time(full_layer_name: str, gpu_type: str) -> (float, float):  # return (loading_time, inference_time) ms # Note: loading_time is related to the disk speed
    model_name, layer_name = parse_layer_name(full_layer_name)
    if gpu_type == "A10G":
        if model_name.startswith("llama-2-7b"):
            if layer_name == "tok_embeddings":
                return (144.695, 0.095)
            elif layer_name.startswith("layer"):
                return (220.949, 1.02)
            elif layer_name == "norm":
                return (0.543, 0.124)
            elif layer_name == "output":
                return (152.412, 0.648)
            else:
                raise NotImplementedError("Unknown layers")
        elif model_name.startswith("llama-2-70b"):
            if layer_name == "tok_embeddings":
                return (279.545, 0.098)
            elif layer_name.startswith("layer"):
                return (864.465, 3.748)
            elif layer_name == "norm":
                return (0.534941, 0.134)
            elif layer_name == "output":
                return (277.843, 1.159)
            else:
                raise NotImplementedError("Unknown layers")

    if gpu_type == "A100":
        if model_name.startswith("llama-2-7b"):
            if layer_name == "tok_embeddings":
                return (164.065, 0.074)
            elif layer_name.startswith("layer"):
                return (265.658, 0.675)
            elif layer_name == "norm":
                return (0.936, 0.113)
            elif layer_name == "output":
                return (166.615, 0.203)
            else:
                raise NotImplementedError("Unknown layers")
        elif model_name.startswith("llama-2-70b"):
            if layer_name == "tok_embeddings":
                return (330.723, 0.074)
            elif layer_name.startswith("layer"):
                return (749.449, 1.211)
            elif layer_name == "norm":
                return (0.942, 0.124)
            elif layer_name == "output":
                return (188.085, 0.347)
            else:
                raise NotImplementedError("Unknown layers")

    raise NotImplementedError

# status


nodes_list = ["A10_0", "A10_1", "A10_2", "A10_3", "A100_0", "A100_1"]


def get_nodes() -> List[str]:
    # return node_num
    return nodes_list
    raise NotImplementedError


def get_node_allocated_mem(w_id: str) -> float:
    # return mem
    return 0
    raise NotImplementedError


def get_node_gpu_type(w_id: str) -> str:
    # return gpu_type
    if w_id.startswith("A10_"):
        return "A10G"
    if w_id.startswith("A100_"):
        return "A100"
    raise NotImplementedError


def get_node_loaded_layers(w_id: str) -> List[str]:
    # return layer_name
    return []
    raise NotImplementedError


def get_network_latency(from_w_id: str, to_w_id: str) -> float:
    # return latency
    if from_w_id.startswith("A10_") and to_w_id.startswith("A100_"):
        return 2.0
    if from_w_id.startswith("A100_") and to_w_id.startswith("A10_"):
        return 2.0
    if from_w_id.startswith("A10_") and to_w_id.startswith("A10_"):
        return 1.0
    if from_w_id.startswith("A100_") and to_w_id.startswith("A100_"):
        return 1.0
    raise NotImplementedError(f"Unknown network latency between {from_w_id} and {to_w_id}.")
