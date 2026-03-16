import json

import os
import json
import shutil
from collections import defaultdict
import re


def parse_graph(graph_json):
    with open(graph_json, 'r') as f:
        graph = json.load(f)

    nodes = graph['init_graph']['nodes']
    edges = graph['init_graph']['edges']
    
    # Set of names to skip
    ignored_objects = {'wall', 'ceiling', 'floor'}

    node_map = {node['id']: node for node in nodes}
    relations = defaultdict(list)

    # Group all edges by source node
    for edge in edges:
        from_node = node_map.get(edge['from_id'])
        to_node = node_map.get(edge['to_id'])
        if from_node and to_node:
            if from_node['class_name'] in ignored_objects or to_node['class_name'] in ignored_objects:
                continue 
            
            rel = edge['relation_type'].replace('_', ' ')
            relations[from_node['id']].append((rel, to_node['class_name']))

    descriptions = []
    mentioned_objects = set()
    desc = ""
    descriptions.append("The environment contains the following objects:") 
    # Describe each object and its states
    for node in nodes:
        obj_id = node['id']
        name = node['class_name']
        category = node['category']
        properties = node['properties']
        states = node['states']
        rels = relations.get(obj_id, [])

        if name in ignored_objects:
            continue  # Skip ignored objects
        
        mentioned_objects.add(name)
        #desc = f"{name} (object id: {obj_id}):"
        desc = f"{name} "
        if states:
            readable_states = ', '.join([s.lower() for s in states])
            desc += f"(It is {readable_states})"

        if rels:
            rel_strings = defaultdict(list)
            for rel, target in rels:
                if rel == "CLOSE":
                    continue
                rel_strings[rel.lower()].append(target)
            for rel, targets in rel_strings.items():
                joined_targets = ', '.join(targets)
                desc += f". It is {rel} {joined_targets}"

        descriptions.append(desc)

    all_nodes_count = len([n for n in nodes if n['class_name'] not in ignored_objects])
    return '\n'.join(descriptions)

def parse_graph_with_id(graph_json):
    with open(graph_json, 'r') as f:
        graph = json.load(f)

    nodes = graph['init_graph']['nodes']
    edges = graph['init_graph']['edges']
    
    # Set of names to skip
    ignored_objects = {'wall', 'ceiling', 'floor'}

    node_map = {node['id']: node for node in nodes}
    relations = defaultdict(list)

    # Group all edges by source node
    for edge in edges:
        from_node = node_map.get(edge['from_id'])
        to_node = node_map.get(edge['to_id'])
        if from_node and to_node:
            if from_node['class_name'] in ignored_objects or to_node['class_name'] in ignored_objects:
                continue 
            
            rel = edge['relation_type'].replace('_', ' ')
            relations[from_node['id']].append((rel, to_node['class_name']))

    descriptions = []
    mentioned_objects = set()
    desc = ""
    descriptions.append("The environment contains the following objects:") 
    # Describe each object and its states
    for node in nodes:
        obj_id = node['id']
        name = node['class_name']
        category = node['category']
        properties = node['properties']
        states = node['states']
        rels = relations.get(obj_id, [])

        if name in ignored_objects:
            continue  # Skip ignored objects
        
        mentioned_objects.add(name)
        desc = f"{name} (id: {obj_id}):"
        if states:
            readable_states = ', '.join([s.lower() for s in states])
            desc += f" States: {readable_states}"

        if rels:
            rel_strings = defaultdict(list)
            for rel, target in rels:
                #if rel == "CLOSE":
                #    continue
                rel_strings[rel.lower()].append(target)
            for rel, targets in rel_strings.items():
                joined_targets = ', '.join(targets)
                desc += f". It is {rel} {joined_targets}"

        descriptions.append(desc)

    all_nodes_count = len([n for n in nodes if n['class_name'] not in ignored_objects])
    return '\n'.join(descriptions)

def parsed_graph_text_to_dict(parsed_text):
    graph_dict = {}
    lines = parsed_text.strip().split("\n")
    for line in lines:
        match = re.match(r"(.+?\(id: \d+\)):", line)
        if match:
            key = match.group(1).strip()
            value = line[len(match.group(0)):].strip()  # everything after 'key:'
            graph_dict[key] = value
    return graph_dict

