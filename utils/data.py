from config import *

def load_csv_file(path):
    res_states, res_commands = [], []
    with open(path, 'r') as fop:
        for line in fop:
            line_parts = [float(part.replace('"', '')) for part in line.strip().split(',')]
            res_states.append(line_parts[:-5]) # append state information up to command
            res_commands.append(line_parts[-5:]) # append command information of length 5
    return res_states, res_commands

def state_to_dict(state):
    '''
    Returns dict with masked state properties
    '''
    res = {}
    for prop in STATE_PROPERTIES:
        if prop in STATE_MASK:
            res[prop] = eval('state.' + prop)
    return res

def dict_to_vector(dict_in, properties):
    res = []
    for prop in properties:
        if type(dict_in[prop]) is tuple:
            for val in dict_in[prop]:
                res.append(val)
        else:
            res.append(dict_in[prop])
    return res

def state_to_vector(state):
    return dict_to_vector(state_to_dict(state), STATE_MASK)

def vector_to_command(vector):
    res = Command()
    res.accelerator = vector[0] 
    res.brake = vector[1] 
    res.steering = vector[2] 
    return res

def apply_mask_to_vectors(data, properties, mask):
    res = []
    for data_point in data:
        cur_res = []
        i = 0
        for prop in properties:
            if prop in mask:
                cur_res += data_point[i:i+properties[prop]]
            i += properties[prop]
        res.append(cur_res)
    return res