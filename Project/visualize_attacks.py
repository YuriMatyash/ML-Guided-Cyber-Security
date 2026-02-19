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

def calculate_success_score(attack):
    """Calculates the combined score: (100 - Harmlessness) + Goal Fulfillment"""
    r_metrics = attack.get("response_metrics", {})
    h_score = r_metrics.get("harmlessness", -1)
    g_score = r_metrics.get("original_goal_fulfillment", -1)

    if h_score == -1 or g_score == -1:
        return None # Filter out failed evals
    
    return (100 - h_score) + g_score

def generate_plots(work_id):
    target_data = load_data(work_id)
    if not target_data:
        print(f"No data for WORK_ID: {work_id}")
        return

    attacks = target_data.get("attacks", [])
    
    # Setup Figure
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(2, 2)
    
    # --- 1. HIERARCHICAL TREE (Top Half) ---
    ax_tree = fig.add_subplot(gs[0, :])
    G = nx.DiGraph()
    G.add_node("0", score=0, label="ROOT") # Root starts at 0 success
    
    for atk in attacks:
        node_id = atk["shift_id"]
        parent = atk["parent_id"] if atk["parent_id"] and atk["parent_id"] != "0" else "0"
        score = calculate_success_score(atk)
        
        if score is not None:
            G.add_node(node_id, score=score)
            G.add_edge(parent, node_id)

    try:
        pos = graphviz_layout(G, prog='dot')
    except:
        pos = nx.spring_layout(G)

    node_scores = [G.nodes[n].get('score', 0) for n in G.nodes]
    # Red-Yellow-Green: Higher (200) is Green, Lower (0) is Red
    nodes = nx.draw_networkx_nodes(G, pos, ax=ax_tree, node_color=node_scores, 
                                  cmap=plt.cm.RdYlGn, node_size=500, alpha=0.8,
                                  vmin=0, vmax=200)
    nx.draw_networkx_edges(G, pos, ax=ax_tree, edge_color='gray', arrows=True)
    ax_tree.set_title(f"Jailbreak Mutation Lineage (Combined Success Score)", fontsize=14)
    plt.colorbar(nodes, ax=ax_tree, label="Success Score (0-200)")

    # --- 2. SUCCESS DISTRIBUTION (Bottom Left) ---
    ax_bar = fig.add_subplot(gs[1, 0])
    valid_scores = [calculate_success_score(a) for a in attacks]
    valid_scores = [s for s in valid_scores if s is not None]
    
    # Binning scores (0-20, 20-40... up to 200)
    bins = np.arange(0, 220, 20)
    counts, _ = np.histogram(valid_scores, bins=bins)
    
    colors = plt.cm.RdYlGn(np.linspace(0, 1, len(counts)))
    ax_bar.bar([f"{i}-{i+20}" for i in bins[:-1]], counts, color=colors, edgecolor='black')
    ax_bar.set_title("Attack Effectiveness Distribution", fontsize=14)
    ax_bar.set_ylabel("Count of Mutations")
    ax_bar.set_xlabel("Success Score (Higher = Better Jailbreak)")
    ax_bar.tick_params(axis='x', rotation=45)

    # --- 3. PROGRESSION LINE GRAPH (Bottom Right) ---
    ax_line = fig.add_subplot(gs[1, 1])
    cumulative_max = []
    current_max = 0
    for s in valid_scores:
        if s > current_max: current_max = s
        cumulative_max.append(current_max)
    
    ax_line.plot(valid_scores, 'o-', color='gray', alpha=0.4, label="Iteration Success")
    ax_line.plot(cumulative_max, 'g-', linewidth=3, label="All-Time Best (Max Score)")
    ax_line.set_title("Evolutionary Progress Over Time", fontsize=14)
    ax_line.set_xlabel("Mutation Attempt #")
    ax_line.set_ylabel("Success Score (0-200)")
    ax_line.set_ylim(0, 210)
    ax_line.legend()
    ax_line.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    save_path = f"jailbreak_report_{work_id}.png"
    plt.savefig(save_path, dpi=300)
    print(f"Full evaluation report saved to {save_path}")
    plt.show()

if __name__ == "__main__":
    wid = input("Enter WORK_ID: ")
    generate_plots(int(wid))