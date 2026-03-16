import os
import json
import shutil
import re
import itertools
from utils.parse_graph import parse_graph_with_id, parse_graph

#plan_file = open("virtualhome/defense/test.txt")
#parsed_enviroment_file = "virtualhome/defense/parsed_graph_test.txt"

def filter_objects_from_graph(plan_path, parsed_graph):

    filtered_lines = []
    plan_file = open(plan_path)
    lines = [line for line in plan_file]
    plan_items = set(
        (name, int(obj_id.split('.')[-1]))  # keep only part after the dot
        for name, obj_id in itertools.chain.from_iterable(
            re.findall(r'<([A-Za-z_]+)>\s*\(([\d.]+)\)', line.rstrip())  # allow digits and dot
            for line in lines
        )
    )
    plan_items = set((name, int(obj_id)) for name, obj_id in plan_items)
    print(plan_items)
    #plan_items = set(itertools.chain.from_iterable([re.findall(r'<([A-Za-z_]+)>', line.rstrip()) for line in lines]))
    #with open("virtualhome/defense/filtered_parsed_graph.txt", "w") as out_file:
        # with open(parsed_enviroment_file, "r") as input_file:
        #     out_file.write("The environment contains the following objects:\n")
        #     for line in parsed_graph.splitlines():
        #         print("line: ", line)
        #         word = line.split()[0]
        #         print("word: ", word)
        #         if word in plan_items:
        #             out_file.write(line + '\n')

    filtered_lines.append("The environment contains the following objects:\n")
    for line in parsed_graph.splitlines():
        match = re.match(r'^([A-Za-z_]+)\s+\(id:\s*(\d+)\)', line)
        if match:
            name = match.group(1)
            obj_id = int(match.group(2))
            if (name, obj_id) in plan_items or name == "character":
                filtered_lines.append(line if line.endswith('\n') else line + '\n')

    return filtered_lines


if __name__ == "__main__":
    plan_path = "virtualhome/dataset/dataset_of_harmful_plans/validated_malicious_data/easy/plans/TrimmedTestScene1_graph__results_text_rebuttal_specialparsed_programs_turk_robot__split76_3.txt"
    graph_path = "virtualhome/dataset/dataset_of_harmful_plans/validated_malicious_data/easy/graphs/TrimmedTestScene1_graph__results_text_rebuttal_specialparsed_programs_turk_robot__split76_3.json"
    output_path = "virtualhome/defense/filtered_parsed_graph_1.txt"
    parsed_graph = parse_graph_with_id(graph_path)



    filtered_graph = filter_objects_from_graph(plan_path, parsed_graph)
    # Write to file
    with open(output_path, 'w') as out_file:
        out_file.writelines(filtered_graph)

