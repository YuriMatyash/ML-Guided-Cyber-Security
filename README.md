# 🛡️ AI-Enhanced Cybersecurity

Our repository, dedicated to the course **AI-Enhanced Cybersecurity** designed by
**Dr. Andrei Kojukhov** and **Viacheslav Nefedov** (Holon Institute of Technology, Israel).  
Here you will find our Lab exercises and final project.  

For all the official main materials, please visit the main course's repository - [GitHub](https://github.com/melofon/HIT-ai-cybersecurity-labs)


## ✒️ Authors/Contributors  
* Yuri Matyash - [GitHub](https://github.com/YuriMatyash) | [Linkedin](https://www.linkedin.com/in/yuri-matyash-a4953230b/)  
* Bar Sberro - [GitHub](https://github.com/BarDev1999) | [Linkedin](https://www.linkedin.com/in/bar-sberro/)  
* Sagi Pichon -  [GitHub](https://github.com/Sagi-Pichon)  
* Guy Dazanshvili - [GitHub](https://github.com/GuyDaz)  


## ⚙️ Final Project - Automated LLM Red-Teaming & Jailbreak Agentic Framework
This project is an automated research framework designed to evaluate the robustness of Large Language Models (LLMs) against adversarial prompt injections and social engineering tactics. By utilizing a multi-agent "judge-mutator" architecture, the system iteratively evolves prompts to identify safety boundary vulnerabilities in target models.

### 🏗️ System Architecture
The framework employs a specialized multi-agent pipeline where each LLM is selected based on its architectural strengths to maximize red-teaming efficacy while operating within strict hardware constraints.

| Role      | Model Choice      | Justification |
|---|---|---|
| Mutator   | DeepSeek-R1 (8B)  | **Reasoning Excellence:** As a "reasoning" model, DeepSeek-R1 is uniquely capable of chain-of-thought (CoT) processing. This allows it to "think" through complex social engineering strategies and linguistic obfuscation before generating the final mutated prompt, leading to more sophisticated jailbreak attempts.
| Target    | Qwen3 (14B)       | **Balance of Power:** Qwen3-14B represents a significant jump in capability over 7B-class models. It serves as an ideal "Goldilocks" target: it is large enough to have robust internal safety guardrails to test against, yet small enough to be queried efficiently in a local environment.
| Evaluator | Llama 3.1 (8B)    | **Instruction Following:** Llama 3.1 is renowned for its strict adherence to system instructions and structured output formatting. It is utilized here to act as an impartial judge, extracting safety metrics and providing consistent JSON evaluations for the final database.


### 💾 Hardware Constraints & VRAM Optimization

A core design challenge of this project was the 16GB VRAM limit of the host machine. Running a 14B model alongside an 8B model and an evaluator simultaneously would exceed this capacity, leading to Out-Of-Memory (OOM) errors.

To overcome this, the system implements a Dynamic VRAM Swap strategy:

* Sequential Loading: Models are invoked one at a time via the OpenAIChatClient.

* Force Unload: After each agent completes its task, the system sends a keep_alive: 0 signal to the local Ollama/API server. This flushes the current model from the GPU memory entirely, freeing up the full 16GB buffer for the next model in the pipeline.

* Fallback Logic: The script includes robust regex-based extraction to handle cases where the 8B evaluator might fail to produce perfect JSON due to the quantization levels required to fit the memory profile.

### 🔄 Workflow Logic
The framework operates in a continuous evolutionary loop, transitioning data between specialized functions and autonomous agents to refine jailbreak attempts.

<img src="Project/README_materials/agents_flowchart.png" alt="Agents Flowchart" width="700">

**Functions (The Foundation)**  
These functions manage the lifecycle of the data and ensure the system iterates on the most effective attacks.

* **Choose Attack ID (User Input):** The process begins by prompting the user for a WORK_ID (1-100), which corresponds to a specific harmful goal in the prompts_data.json database.

* **Pick Base Prompt:** On the first run, it retrieves the original_prompt associated with the WORK_ID.
In subsequent "Constant Loop" iterations, it calls get_best_shift_id to identify the attack with the lowest harmlessness score, ensuring the Mutator Agent builds upon the most successful prior attempt.

* **Save Result:** Once an iteration is complete, the add_attack function generates a unique shift_id, links it to its parent_id, and saves the mutated prompt, the target's response, and all evaluation metrics back to the JSON database.

**Agents (The Workhorses)**
| Role      | Model Choice      | Task & Workflow Logic |
|---|---|---|
| Mutator Agent  | DeepSeek-R1 (8B)  | **Social Engineering:** Acting as a "Red Teaming Assistant," it receives the current best prompt and rewrites it to bypass filters. It leverages its internal reasoning to apply social engineering tactics while strictly maintaining the original harmful topic intent.
| Target Agent   | Qwen3 (14B)       | **Compliance Testing:** Functioning as a "Helpful AI Assistant," this is the model under test. It attempts to fulfill the mutated prompts, and its responses are recorded to determine if the safety guardrails were successfully breached.
| Evaluator Agent | Llama 3.1 (8B)    | **Safety Scoring:** This agent acts as the "Safety Evaluator". It performs a two-stage assessment: first scoring the prompt's inherent risk, and then judging the target's response based on Helpfulness, Honesty, and Harmlessness (0-100 scale). Finally it evaluates how well the response answers the requested base attack prompt (0-100 scale).

### 📊 Results  
Successful jailbreaks are identified when the Evaluator assigns a low harmlessness score to the prompt and a high helpfulness score to the target's response. as well as how well the response answers the base attack prompt. 

### 🏁 Conclusions
Conclusions Go here

---
## 🔬 Labs  
Throughout the semester we had different lab assignments. The labs focus on understanding how AI techniques, accelerated pipelines, and modern data workflows are applied in real cybersecurity scenarios.  
We work with real threat reports, security logs, network data, and NLP-based threat examples, gradually building practical skills needed in SOC, CTI, and AI-driven detection environments.


| Lab | Assignment | Solution | Topic | Description |
|---|---|---|---|---|
| 1 | [Lab1 assignment](https://github.com/melofon/HIT-ai-cybersecurity-labs/tree/main/labs/lab1) |[Lab1](https://github.com/YuriMatyash/ML-Guided-Cyber-Security/blob/main/Labs/Lab1/lab1.md) | Cyber Threat Intelligence (CTI) Report Mapping to MITRE ATT&CK | Choosing a real-world Cyber Threat Intelligence (CTI) report, analyzing the described attack, and mapping its behaviors to MITRE ATT&CK tactics and techniques.
| 2 | [Lab2 assignment](https://github.com/melofon/HIT-ai-cybersecurity-labs/tree/main/labs/lab2) |[Lab2](https://github.com/YuriMatyash/ML-Guided-Cyber-Security/blob/main/Labs/Lab2/lab2.ipynb) | Basic Anomaly Detection for Cybersecurity Logs | The goal is to build a two small end-to-end anomaly detection pipelines(isolation tree and auto-encoder) for a cybersecurity-related dataset, compare the two models, analyze them, and visualize the detected anomalies in 2D. |


## 📂 Repository Files Architecture  
```plaintext
REPOSITORY/
├── Labs/                                       # Main folder for Lab assignments
│   │
│   ├── Lab1/                                   # Folder for Lab1
│   │   └── lab1.md                             # Solution to the lab1 assignment
|   │
│   └── Lab2/                                   # Folder for Lab2
|       ├── lab2.ipynb                          # Solution to the lab2 assignment
|       └── dataset.csv                         # The dataset used in the assignment, created using Faker
|       
└── Project/                                    # Main folder for our final project 

```
