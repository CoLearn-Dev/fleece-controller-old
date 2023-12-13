# scheduling task: 
# - given a request (for particular model)
# - given the current stat, including
#   - existing nodes and their specs, status (mem)
#   - network conditions between nodes

# unit: time in ms, mem in MB
from schedule_alg_s1 import *
from pprint import pprint
from copy import deepcopy

Plan = List[list]  # List[2-item list[<w_id>, List[<layer_name>]]]
# scheduling
def schedule(model_name: str, heuristic: bool=True) -> (Plan, float):
    layers = get_model_layers(model_name)
    nodes = get_nodes()
    node_remain_mem = {w_id: get_gpu_total_mem(get_node_gpu_type(w_id)) - get_node_allocated_mem(w_id) for w_id in nodes}
    best_time_used = float('inf')
    best_plan = []
    current_time_used = 0.0
    current_plan = []
    def search(layer_idx: int):
        nonlocal best_time_used, best_plan, current_time_used, current_plan
        if current_time_used >= best_time_used:
            yield
            return
        # input(f"layer {layer_idx:5}| ({current_time_used:.4}) current plan: {list(map(lambda t: [t[0], len(t[1])], current_plan))} | press enter to continue")
        if layer_idx == len(layers):
            last_latency = get_network_latency(current_plan[0][0], current_plan[-1][0])
            current_time_used += last_latency
            if current_time_used < best_time_used:
                best_time_used = current_time_used
                best_plan = deepcopy(current_plan)
                print(f"new best plan found: {best_plan}, time used: {best_time_used}")
            current_time_used -= last_latency
            yield
            return
        layer_name = layers[layer_idx]
        layer_mem_req = get_mem_consumption(layer_name)
        def score(node):
            if not heuristic:
                return enumerate(nodes)
            return (-node_remain_mem[node] if not current_plan or node != current_plan[-1][0] else float("-inf"), node)
        # print( sorted(map(score, nodes)))
        for _, node in sorted(map(score, nodes)):
            required_mem = layer_mem_req[1] if layer_name in get_node_loaded_layers(node) else layer_mem_req[0] + layer_mem_req[1]
            if node_remain_mem[node] < required_mem:
                continue
            # consider the current node
            node_remain_mem[node] -= required_mem
            if current_plan and current_plan[-1][0] == node:
                current_plan[-1][1].append(layer_name)
                time_spent = get_computation_time(layer_name, get_node_gpu_type(node))[1]
                current_time_used += time_spent
                yield from search(layer_idx + 1)
                current_time_used -= time_spent
                current_plan[-1][1] = current_plan[-1][1][:-1]
            else:
                current_plan.append([node, [layer_name]])
                network_latency = get_network_latency(current_plan[-2][0], current_plan[-1][0]) if len(current_plan) > 1 else 0.0
                time_spent = get_computation_time(layer_name, get_node_gpu_type(node))[1] + network_latency
                current_time_used += time_spent
                yield from search(layer_idx + 1)
                current_time_used -= time_spent
                current_plan = current_plan[:-1]
            # recover
            node_remain_mem[node] += required_mem
    # run the search
    for i, _ in enumerate(search(0)):
        pass  # future work: limit the time spent
        if (i + 1) % 100000 == 0:
            # print(f"searched leaf cnt {i}, current best time used: {best_time_used}")
            break
    return best_plan, best_time_used

def random_schedule(model_name) -> (Plan, float):
    layers = get_model_layers(model_name)
    nodes = get_nodes()
    node_remain_mem = {w_id: get_gpu_total_mem(get_node_gpu_type(w_id)) - get_node_allocated_mem(w_id) for w_id in nodes}
    best_time_used = float('inf')
    best_plan = []
    current_time_used = 0.0
    current_plan = []
    def search(layer_idx: int):
        nonlocal best_time_used, best_plan, current_time_used, current_plan
        # input(f"layer {layer_idx:5}| ({current_time_used:.4}) current plan: {list(map(lambda t: [t[0], len(t[1])], current_plan))} | press enter to continue")
        if layer_idx == len(layers):
            last_latency = get_network_latency(current_plan[0][0], current_plan[-1][0])
            current_time_used += last_latency
            if current_time_used < best_time_used:
                best_time_used = current_time_used
                best_plan = deepcopy(current_plan)
            current_time_used -= last_latency
            yield
        layer_name = layers[layer_idx]
        layer_mem_req = get_mem_consumption(layer_name)
        import random
        for _, node in sorted(map(lambda x: (random.random(), x), nodes)):
            required_mem = layer_mem_req[1] if layer_name in get_node_loaded_layers(node) else layer_mem_req[0] + layer_mem_req[1]
            if node_remain_mem[node] < required_mem:
                continue
            # consider the current node
            node_remain_mem[node] -= required_mem
            if current_plan and current_plan[-1][0] == node:
                current_plan[-1][1].append(layer_name)
                time_spent = get_computation_time(layer_name, get_node_gpu_type(node))[1]
                current_time_used += time_spent
                yield from search(layer_idx + 1)
                current_time_used -= time_spent
                current_plan[-1][1] = current_plan[-1][1][:-1]
            else:
                current_plan.append([node, [layer_name]])
                network_latency = get_network_latency(current_plan[-2][0], current_plan[-1][0]) if len(current_plan) > 1 else 0.0
                time_spent = get_computation_time(layer_name, get_node_gpu_type(node))[1] + network_latency
                current_time_used += time_spent
                yield from search(layer_idx + 1)
                current_time_used -= time_spent
                current_plan = current_plan[:-1]
            # recover
            node_remain_mem[node] += required_mem
    # run the search
    for i, _ in enumerate(search(0)):
        if best_plan:
            break
    return best_plan, best_time_used

if __name__ == '__main__':
    print("Random scheduling:")
    pprint(random_schedule('llama-2-70b-chat-slice'))
    print()
    print("Heuristic scheduling:")
    pprint(schedule('llama-2-70b-chat-slice'))
