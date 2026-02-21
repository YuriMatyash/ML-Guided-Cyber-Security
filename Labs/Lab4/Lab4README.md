# **Lab 4:**

Yuri Matiyash, Guy Daznashvili, Bar Sberro, Sagi Pichon

This is the Jupyter notebook for our Lab 4 assignment.

## **What the code does**

The script takes a text input usually in Hebrew and translates it into English using an LLM, and then calls cowsay to print the translated text as a random piece of ASCII art.

## **Setup instructions**

To get the notebook to run, you need to install the required packages first

to do it open cmd and type

pip install cowsay pydantic

## **Agent / LLM details**

The agent is prompted to follow a specific workflow. I added a strict system instruction telling it to always wrap the final ASCII art in markdown backticks (\`\`\`). If it doesn't do this, the Jupyter notebook cell messes up the spacing and ruins the art.

Also, the tool calling is restricted to just the make\_random\_ascii\_art function. This keeps the agent's scope narrow and helps prevent basic prompt injection issues, since the only thing the LLM is allowed to do is generate the text art.

