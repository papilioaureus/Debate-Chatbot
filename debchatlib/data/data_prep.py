
import pandas as pd
import json
from datasets import load_dataset


class TextDataset(Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = item["input_ids"].clone()
        return item

    def __len__(self):
        return len(self.encodings["input_ids"])


def split_into_sentence_pairs_alternative_fixed(text):
    sentences = text.split(". ")
    sentence_pairs = []
    for i in range(len(sentences) - 1):
        input_text = sentences[i].strip() + '.'  # Add the period back to the end of the sentence
        target_text = sentences[i + 1].strip()
        if target_text and target_text[-1] not in '.?!':  # Check if target text is not empty and ends with a punctuation mark
            target_text += '.'
        sentence_pairs.append({"input_text": input_text, "target_text": target_text})
    return sentence_pairs


def convert_to_chat_template_from_memory(json_data):
    chat_data = []
    for entry in json_data:
        chat_data.append({
            "input_text": entry["input_text"],
            "target_text": entry["target_text"]
        })
    return chat_data


def load_csv_prep():
    # Returns train encodings and datasets
    
    # Load the CSV file
    csv_file_path = 'debate2019_948.csv'
    df = pd.read_csv(csv_file_path)

    # Apply the fixed function to each document to get sentence pairs
    chat_data_alternative_fixed = []
    for _, row in df.iterrows():
        chat_data_alternative_fixed.extend(split_into_sentence_pairs_alternative_fixed(row['Full-Document']))

    # Convert chat data to JSON
    json_chat_data_alternative_fixed = pd.DataFrame(chat_data_alternative_fixed).to_json(orient='records')

    # Preview the first few entries of the chat data in JSON format
    json_chat_data_alternative_fixed[:500]  # Displaying a substring to keep the output concise

    # Since json_chat_data_alternative_fixed is a string representation of your JSON, you need to load it into a Python object
    json_data = json.loads(json_chat_data_alternative_fixed)

    # Convert the in-memory JSON data to the chat template format
    chat_data = convert_to_chat_template_from_memory(json_data)

    # Print the first few elements of the chat data
    print(chat_data[:5])

    data = load_dataset("truthful_qa", "generation")
    tokenizer.pad_token = tokenizer.eos_token

    # prompt_template = "### Instruction: {prompt}\n### Response:"

    train_dataset = data['validation'].select(range(100)).map(lambda x: {"input_text": x['question']  + "\n" + x['best_answer']})

    # Tokenize the datasets
    train_encodings = tokenizer(train_dataset['input_text'], truncation=True, padding=True, max_length=256, return_tensors='pt')

    print(train_encodings)

    dataset = TextDataset(train_encodings)

    # Convert the encodings to PyTorch datasets
    train_dataset = TextDataset(dataset)

    return train_encodings, train_dataset