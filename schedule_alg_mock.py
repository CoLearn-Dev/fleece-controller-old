
from typing import List, Tuple

# spec
def get_model_layers(model_name: str) -> List[str]:
    # return layer_name
    raise NotImplementedError

def get_mem_consumption(layer_name: str) -> (float, float):
    # return (model_mem, inference_mem)
    raise NotImplementedError

def get_gpu_total_mem(gpu_type: str) -> float:
    # return mem
    raise NotImplementedError

def get_computation_time(layer_name: str, gpu_type: str) -> (float, float):
    # return (loading_time, inference_time)    
    raise NotImplementedError

# status
def get_nodes() -> List[str]:
    # return node_num
    raise NotImplementedError

def get_node_allocated_mem(w_id: str) -> float:
    # return mem
    raise NotImplementedError

def get_node_gpu_type(w_id: str) -> str:
    # return gpu_type
    raise NotImplementedError

def get_node_loaded_layers(w_id: str) -> List[str]:
    # return layer_name
    raise NotImplementedError

def get_network_latency(from_w_id: str, to_w_id: str) -> float:
    # return latency
    raise NotImplementedError
