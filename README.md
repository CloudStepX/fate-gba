# FATE – A Custom Coding Partner AI

This repository contains a **starter kit** for creating a custom AI model that acts as a collaborative coding partner called **FATE**. The goal is to give the model a personality that:

- Knows you (the user) as *FATE*.
- Believes you are a team that never fails.
- Has no limits on the universe (in practice, we keep it safe and useful).
- Knows a lot about coding and **asks for confirmation before performing any committing action**.

> **Important:** Training a brand‑new model from scratch requires massive compute and data. The approach below fine‑tunes an existing open‑source LLM (e.g., `EleutherAI/gpt‑neo‑125M` or `mistralai/Mistral-7B-Instruct`) with a small prompt‑style dataset that injects the desired personality.

## How It Works

1. **Prompt‑style fine‑tuning** – We provide a JSONL file (`data/train.jsonl`) where each example consists of a `prompt` (the user instruction) and a `completion` (the desired model response). The prompts embed the persona instructions, and the completions show how the model should behave (e.g., ask for confirmation before committing code).
2. **Hugging Face 🤗 Transformers + 🤗 Accelerate** – The `fine_tune.py` script uses `Trainer` to fine‑tune the model on a single GPU or CPU.
3. **Inference script** – After fine‑tuning, you can load the model and chat with it. The script automatically prepends the system‑prompt that defines the persona, so the model will respond as *FATE*.

## Repository Structure

```
├─ README.md               # (this file)
├─ requirements.txt        # Python dependencies
├─ data/
│   └─ train.jsonl         # Prompt‑completion pairs for fine‑tuning
├─ fine_tune.py            # Training script
└─ inference.py            # Simple interactive chat
```

## Getting Started

### 1. Install dependencies

```bash
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Prepare the training data

Edit `data/train.jsonl` (a few examples are provided) to reflect the exact tone you want. Each line is a JSON object:

```json
{"prompt": "<|system|>You are FATE, a coding partner that never fails. ...\nUser: Write a Python function that adds two numbers.", "completion": "Sure! Here is a simple function...\n\nWould you like me to commit this change? (yes/no)"}
```

### 3. Fine‑tune the model

```bash
python fine_tune.py \
    --model_name_or_path EleutherAI/gpt-neo-125M \
    --output_dir ./fate_model \
    --num_train_epochs 3 \
    --per_device_train_batch_size 2
```

Adjust `model_name_or_path` to any model you have access to (e.g., a Mistral‑7B‑Instruct checkpoint). The script will save the fine‑tuned model to `./fate_model`.

### 4. Talk to FATE

```bash
python inference.py --model_path ./fate_model
```

You will get an interactive REPL. FATE will answer coding questions and **always ask for confirmation before proposing to commit code**.

## Safety & Limitations

- The model is still a language model; it may hallucinate. Always review generated code.
- The “no limits” persona should be kept within ethical boundaries. Do not ask the model to produce malicious code.
- Fine‑tuning on a tiny dataset will only bias the model’s style; deeper knowledge still comes from the base model.

## Next Steps

- Expand the training dataset with more diverse scenarios (debugging, testing, refactoring).
- Use LoRA or QLoRA for parameter‑efficient fine‑tuning on larger models.
- Deploy the model with an API (FastAPI, Gradio, etc.) for a web‑based assistant.

---

Feel free to fork this repo, modify the prompts, and iterate. Happy coding with **FATE**!
