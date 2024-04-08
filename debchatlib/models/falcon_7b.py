
import pandas as pd
import json
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline, AutoModelForCausalLM, AutoTokenizer
import torch
from torch.utils.data import DataLoader, Dataset
from datasets import load_dataset
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model

from debchatlib.data.data_prep import load_csv_prep
from debchatlib.data.data_training import train_model


def print_trainable_parameters(model):
    """
    Prints the number of trainable parameters in the model.
    """
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    print(
        f"trainable params: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param}"
    )


# sharded model by vilsonrodrigues
model_id = "vilsonrodrigues/falcon-7b-instruct-sharded"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map={"":0}, trust_remote_code=True)

model.gradient_checkpointing_enable()
model = prepare_model_for_kbit_training(model)

config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["query_key_value"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, config)
print_trainable_parameters(model)

# Execute model
train_encodings, train_dataset = load_csv_prep()

dataset = TextDataset(train_encodings)

trainer = transformers.Trainer(
    model=model,
    train_dataset=dataset,  # Use the dataset prepared in step 3
    args=transformers.TrainingArguments(
        num_train_epochs=2,  # You can adjust the number of epochs based on your dataset size and desired performance
        per_device_train_batch_size=2,  # Adjust based on your GPU memory
        gradient_accumulation_steps=4,
        warmup_ratio=0.05,
        learning_rate=2e-4,
        fp16=True,  # Make sure your hardware supports FP16 training
        logging_steps=10,
        output_dir="outputs",
        optim="adamw_torch",  # Consider using "adamw_torch" for stability
    ),
    data_collator=transformers.DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

model.config.use_cache = False  # Recommended for training to save memory
trainer.train()

model.config.use_cache = True
model.eval()

# Save the model
model_path = "SaveModel"
model.save_pretrained(model_path)
tokenizer.save_pretrained(model_path)
# model should be saved on:
# ('SaveModel/tokenizer_config.json',
# 'SaveModel/special_tokens_map.json',
# 'SaveModel/tokenizer.json')

# Start the model
model_path = "SaveModel"  # Path where you've saved your model
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

# Format the input question
question = "The United States has traditionally regarded three regions as vital geopolitical centers, given their concentration of power and resources. Which ones?"

# Tokenize the input text
inputs = tokenizer(question, return_tensors="pt")

# Generate a response from the model
output = model.generate(
    inputs['input_ids'],
    max_length=200,
    num_return_sequences=1,
    pad_token_id=tokenizer.eos_token_id,
    temperature=0.7,
)

# Decode the output to text
response = tokenizer.decode(output[0], skip_special_tokens=True)

# Print out the response
print(response)