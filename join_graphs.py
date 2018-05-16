import json
import subprocess
import os
import shutil


def domain_names():
    f = open("../domain_names.txt")
    names = [name.strip() for name in f.readlines()]
    f.close()
    return names

def call_vg(command):
    print("Command: " + command)
    res = subprocess.check_output(command.split())
    return res.decode("utf-8")    

class GraphJoiner:
    def __init__(self, graph_file_names):
        self.graph_file_names = graph_file_names

        self.id_counter = 300000
        self.heads = {}
        self.tails = {}
        self.common_heads = {}
        self.common_tails = {}
        self.graphs = {}
        self.read_graphs()

        self.get_starts_ends()
        self.join_tails()
        self.join_heads() 
        self.connect_graphs()
        self.write_modified_files()

    def read_graphs(self):
        for name in self.graph_file_names:
            with open(name) as f:
                data = json.load(f)
            self.graphs[name] = data
            if name == "CIDRpam.incremented.json":
                print(data["node"][0])

            
    def get_starts_ends(self):
        for name in self.graph_file_names:
            heads = call_vg("vg stats --heads %s" % name.replace(".json", ".vg")) 
            heads = heads.split()[1:]
            self.heads[name] = heads
            
            tails = call_vg("vg stats --tails %s" % name.replace(".json", ".vg")) 
            tails = tails.split()[1:]
            self.tails[name] = tails

    def join_tails(self):
        for name in self.graph_file_names:
            new_node_id = self.id_counter
            self.id_counter += 1
            self.add_node_to_json(name, new_node_id)
            self.common_tails[name] = new_node_id
            
            for tail in self.tails[name]:
                self.add_edge_to_json(name, tail, new_node_id)
    
    def join_heads(self):
        for name in self.graph_file_names: 
            new_node_id = self.id_counter
            self.id_counter += 1
            self.add_node_to_json(name, new_node_id)
            self.common_heads[name] = new_node_id
            
            for head in self.tails[name]:
                print("Joining heads on %s (from %s to head %s)" % (name, new_node_id, head))
                self.add_edge_to_json(name, new_node_id, head) 
    
    def connect_graphs(self):
        for tail_name, tail in self.common_tails.items():
            for head_name, head in self.common_heads.items():
                if tail_name != head_name:
                    print("Connecting tail %s:%s to head %s:%s" % (tail_name, tail, head_name, head))
                    # Add to first graph, will be concatenated after
                    self.add_edge_to_json(self.graph_file_names[0], tail, head)
       
    def write_modified_files(self):
        for name in self.graph_file_names:
            print("Writing %s to json" % name)
            new_name = name + ".processed"
            with open(new_name, 'w') as outfile:
                json.dump(self.graphs[name], outfile)

    def add_edge_to_json(self, file_name, from_node, to_node):
        self.graphs[file_name]["edge"].append({"from":from_node, "to": to_node})

    def add_node_to_json(self, file_name, node_id):
        self.graphs[file_name]["node"].append({"id": node_id, "sequence": ""})


if __name__ == "__main__":
    joiner = GraphJoiner([name + ".incremented.json" for name in domain_names()]) 
    print(joiner.common_heads)
    print(joiner.common_tails)

    
