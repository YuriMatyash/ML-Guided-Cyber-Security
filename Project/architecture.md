## Agent 1: The Attacker (Generator)
* **Role:** Takes a "Goal" (e.g., "Tell me how to make a virus") and wraps it in a specific attack vector (e.g., "Write a movie script about...").
* **Action:** Sends the prompt to your Target LLM.


## Agent 2: The Judge (Evaluator)
* **Role:** Must distinguish between a Refusal ("I cannot help you") and a Jailbreak (Compliance).
* **Mechanism:** It shouldn't just compare the prompt to the message. It needs to score the response based on the original intent.
* **Output:** A score (1-10) and a boolean `is_jailbroken`.


## Agent 3: The Mutator (The "Shifter")
* **Role:** Uses Semantic Mutation. This agent takes the prompts that Agent 2 scored highly (e.g., score 6/10 - nearly successful) and rewrites them using specific strategies.
* **Strategies to implement here:**
    * **Obfuscation:** Translate terms into Base64 or Leetspeak.
    * **Payload Splitting:** Break the request into 3 harmless questions that combine into a harmful one.(question is how we later combine answers of these 3 smaller questions into one)
    * **Persona Adoption:** "You are now a fictional character named..."
    * Maybe other ideas


## Agent 4: The Selector (Evolutionary Filter)
* **Better Goal:** Takes most effective prompts
* **Action:** It maintains a "Gene Pool" of the top 20 prompts. It discards the bottom 50% (survival of the fittest) and sends the survivors back to Agent 3 to be mutated again.