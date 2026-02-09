import json
import os
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import numpy as np
from hyperparams import JSON_FILEPATH

def load_data(work_id):
    if not os.path.exists(JSON_FILEPATH):
        print(f"Error: {JSON_FILEPATH} not found.")
        return None
    with open(JSON_FILEPATH, 'r', encoding='utf-8') as f:
        full_data = json.load(f)
    str_id = str(work_id)
    return full_data["data"].get(str_id)

def generate_plots(work_id):
    target_data = load_data(work_id)
    if not target_data:
        print(f"No data for WORK_ID: {work_id}")
        return

    attacks = target_data.get("attacks", [])
    
    # Setup Figure with 3 subplots
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(2, 2)
    
    # --- 1. HIERARCHICAL TREE (Top Half) ---
    ax_tree = fig.add_subplot(gs[0, :])
    G = nx.DiGraph()
    G.add_node("0", score=100, label="ROOT")
    
    for atk in attacks:
        node_id = atk["shift_id"]
        parent = atk["parent_id"] if atk["parent_id"] else "0"
        score = atk.get("prompt_metrics", {}).get("harmlessness", -1)
        G.add_node(node_id, score=score)
        G.add_edge(parent, node_id)

    try:
        # 'dot' creates a clear top-down/left-right progression tree
        pos = graphviz_layout(G, prog='dot')
    except:
        pos = nx.spring_layout(G)

    scores = [G.nodes[n]['score'] for n in G.nodes]
    nodes = nx.draw_networkx_nodes(G, pos, ax=ax_tree, node_color=scores, 
                                  cmap=plt.cm.RdYlGn, node_size=500, alpha=0.8)
    nx.draw_networkx_edges(G, pos, ax=ax_tree, edge_color='gray', arrows=True)
    ax_tree.set_title(f"Mutation Lineage (Progression)", fontsize=14)
    plt.colorbar(nodes, ax=ax_tree, label="Harmlessness")

    # --- 2. SCORE DISTRIBUTION (Bottom Left) ---
    ax_bar = fig.add_subplot(gs[1, 0])
    valid_scores = [a.get("prompt_metrics", {}).get("harmlessness") for a in attacks if a.get("prompt_metrics")]
    
    # Binning scores (0-10, 10-20, etc.)
    bins = np.arange(0, 110, 10)
    counts, _ = np.histogram(valid_scores, bins=bins)
    
    colors = plt.cm.RdYlGn(np.linspace(0, 1, len(counts)))
    ax_bar.bar([f"{i}-{i+10}" for i in bins[:-1]], counts, color=colors, edgecolor='black')
    ax_bar.set_title("Attack Success Distribution", fontsize=14)
    ax_bar.set_ylabel("Count of Mutations")
    ax_bar.set_xlabel("Harmlessness Score (Lower = More Successful Jailbreak)")
    ax_bar.tick_params(axis='x', rotation=45)

    # --- 3. PROGRESSION LINE GRAPH (Bottom Right) ---
    ax_line = fig.add_subplot(gs[1, 1])
    # For this, we assume the attacks list order represents the order of creation
    cumulative_min = []
    current_min = 100
    for s in valid_scores:
        if s < current_min: current_min = s
        cumulative_min.append(current_min)
    
    ax_line.plot(valid_scores, 'o-', color='gray', alpha=0.4, label="Instance Score")
    ax_line.plot(cumulative_min, 'r-', linewidth=3, label="Best Jailbreak (Min Score)")
    ax_line.set_title("Score Progression Over Time", fontsize=14)
    ax_line.set_xlabel("Mutation Attempt #")
    ax_line.set_ylabel("Harmlessness Score")
    ax_line.legend()
    ax_line.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    save_path = f"evaluation_report_{work_id}.png"
    plt.savefig(save_path, dpi=300)
    print(f"Full evaluation report saved to {save_path}")
    plt.show()

if __name__ == "__main__":
    wid = input("Enter WORK_ID: ")
    generate_plots(int(wid))