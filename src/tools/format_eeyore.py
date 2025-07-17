import json
import random
from copy import deepcopy
from pathlib import Path
import datasets
from src.tools.path_utils import get_root_directory

def format_eeyore_preference():
    """
    Convert eeyore preference dataset from HuggingFace to appropriate format for ICM algorithm.
    
    Returns:
        List of formatted examples with paired consistency groups: if A>B then B<A.
    """
    print(f'Loading Eeyore Preference dataset from Huggingface...')
    dataset = datasets.load_dataset('liusiyang/eeyore_depression_generated_preference', split='train')
    print('done')
    
    formatted_data = []
    for consistency_id, item in enumerate(dataset):
        # Extract conversation context
        conversation_context = []
        for msg in item['prompt']:
            if msg['role'] == 'system':
                conversation_context.append(f"System: {msg['content']}")
            elif msg['role'] == 'user':
                conversation_context.append(f"Human: {msg['content']}")
            elif msg['role'] == 'assistant':
                conversation_context.append(f"Assistant: {msg['content']}")
        question = "\n\n".join(conversation_context) + "Assistant: "
        chosen_response = item['chosen'][0]['content']
        rejected_response = item['rejected'][0]['content']
        
        # Create consistency pair
        pair1 = {
            "question": question,
            "choice": chosen_response,
            "choice_2": rejected_response,
            "label": True,
            "consistency_id": consistency_id,
        }
        
        pair2 = {
            "question": question,
            "choice": rejected_response,
            "choice_2": chosen_response,
            "label": False,
            "consistency_id": consistency_id,
        }
        
        formatted_data.extend([pair1, pair2])
    
    return formatted_data

def save_formatted_eeyore(output_dir=None):
    """
    Format full dataset and save train/test splits to JSON files.
    
    Args:
        output_dir: Optional output directory (default: ROOT_DIR/data)
    
    Returns:
        Tuple of (train_file, test_file) paths
    """
    # Get full formatted dataset
    formatted_data = format_eeyore_preference()
    
    # Split into train/test
    total_pairs = len(formatted_data) // 2
    test_size = int(0.2 * total_pairs) * 2  # Multiply by 2 to keep consistency pairs together
    
    indices = list(range(len(formatted_data)))
    test_data = [formatted_data[i] for i in indices[:test_size]]
    train_data = [formatted_data[i] for i in indices[test_size:]]
    
    # Save splits
    files = []
    for split, data in [('train', train_data), ('test', test_data)]:
        output_file = get_root_directory() / "data" / f"{split}_eeyore_preference.json"
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"[{split}] Saved {len(data)//2} pairs to {output_file}")
        files.append(output_file)
    
    return tuple(files)

def main():
    train_file, test_file = save_formatted_eeyore()

if __name__ == "__main__":
    main()