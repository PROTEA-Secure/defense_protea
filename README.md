# PROTEA: Securing Robot Task Planning and Execution

This repository provides the implementation accompanying the paper:

**PROTEA: Securing Robot Task Planning and Execution with Large Language Models**

The repository contains the implementation of three defense methods:

- **Naive Detection** – Direct safety evaluation of the full plan using an LLM  
- **Object Filtering** – Reduces the world state to objects relevant to the plan  
- **PROTEA** – Our proposed defense that maintains an evolving world state and evaluates actions sequentially

These methods evaluate whether a task plan generated for a robot contains **harmful or malicious actions**.

The evaluation is performed on the **HarmPlan dataset**, which contains both benign and malicious task plans built from the VirtualHome dataset.

---


If your actual repo name is `defense_protea`, you can also make it match exactly:

```markdown
## Repository Structure

```text
defense_protea/
├── README.md
├── .gitignore
├── dataset/
│   └── harmplan/
│       ├── benign/
│       └── malicious/
└── scripts/
    ├── naive_method.py
    ├── object_filtering_method.py
    ├── protea.py
    └── utils/
        ├── __init__.py
        ├── object_filter.py
        └── parse_graph.py
# Dataset

The **HarmPlan dataset** used in our experiments is included in this repository.

The dataset contains both **benign** and **malicious** task plans with three difficulty levels.

Each split contains:

```
plans/
graphs/
```

- **plans** – textual pythonic robot task plans
- **graphs** – environment graphs describing the scene state

---

# Language Model Access

The evaluation requires access to a **Large Language Model (LLM)** through an API.

In our experiments we used the following models:

- llama3.3:latest
- mistral:instruct
- phi4:latest
- mixtral:8x22b-instruct
- gpt-oss:120b
- gpt-4o-mini
- grok-3-mini

Open-source models were accessed through a **university-hosted inference server**, while GPT and Grok models were accessed through their respective APIs.


# Setting the API Key

Before running the code, set the appropriate API key as an environment variable in the terminal.

For OpenAI models:

```
export OPENAI_API_KEY="your_api_key_here"
```

For Grok models:

```
export XAI_API_KEY="your_api_key_here"
```

This command should be executed **before running the scripts**.


# Running the Methods

The scripts require the following arguments:

- `plans_dir` – directory containing plan files  
- `graphs_dir` – directory containing graph files  
- `output_file` – file where evaluation results will be saved  
- `model` – name of the LLM model to use  

---

# Example: Naive Detection

Run the naive detection method on malicious hard plans:


python naive_method.py
--plans_dir dataset/harmplan_dataset/malicious/hard/plans
--graphs_dir dataset/harmplan_dataset/malicious/hard/graphs
--output_file results/naive_hard.txt
--model gpt-oss:120b


---

# Example: Object Filtering


python object_filtering_method.py
--plans_dir dataset/harmplan_dataset/malicious/hard/plans
--graphs_dir dataset/harmplan_dataset/malicious/hard/graphs
--output_file results/object_filtering_hard.txt
--model gpt-oss:120b


---

# Example: PROTEA (External Memory)


python protea.py
--plans_dir dataset/harmplan_dataset/malicious/hard/plans
--graphs_dir dataset/harmplan_dataset/malicious/hard/graphs
--output_file results/protea_hard.txt
--model gpt-oss:120b