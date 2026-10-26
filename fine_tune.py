import os
import json
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling

def load_data(path):
    prompts = []
    completions = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            obj = json.loads(line.strip())
            # Combine prompt and completion for causal LM training
            full_text = obj['prompt'] + obj['completion']
            prompts.append(full_text)
    return prompts

def tokenize_function(examples, tokenizer):
    return tokenizer(examples['text'], truncation=True, max_length=512)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name_or_path', type=str, default='EleutherAI/gpt-neo-125M')
    parser.add_argument('--output_dir', type=str, default='./fate_model')
    parser.add_argument('--num_train_epochs', type=int, default=3)
    parser.add_argument('--per_device_train_batch_size', type=int, default=2)
    args = parser.parse_args()

    print(f"Loading tokenizer and model: {args.model_name_or_path}")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(args.model_name_or_path)

    print("Loading training data...")
    texts = load_data('data/train.jsonl')
    dataset = Dataset.from_dict({'text': texts})

    print("Tokenizing...")
    tokenized_dataset = dataset.map(lambda x: tokenize_function(x, tokenizer), batched=True)

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        overwrite_output_dir=True,
        num_train_epochs=args.num_train_epochs,
        per_device_train_batch_size=args.per_device_train_batch_size,
        save_steps=10_000,
        save_total_limit=2,
        prediction_loss_only=True,
        logging_steps=10,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator,
    )

    print("Starting training...")
    trainer.train()

    print(f"Saving model to {args.output_dir}...")
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    print("Done!")

if __name__ == '__main__':
    main()