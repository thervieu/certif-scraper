import numpy as np
import json

# Load JSON from a file (replace 'data.json' with your actual file)
with open('SAA_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(f'{len(data)}')
    print(f'{len(data)}')
    # for obj in data:
    #     print(f'{obj}') 
    count = sum(1 for obj in data if ("question_text" in obj and "Secrets Manager" in obj["question_text"]) or "Secrets Manager" in obj["site_answers"][0])
    print(f"Number of objects containing 'Secrets Manager' in 'question': {count}")
    
    count = 0
    for obj in data:
        for answer in obj["site_answers"]:
            if "Secrets Manager" in answer:
               continue
        for choice in obj["choices"]:
            if "Secrets Manager" in choice:
                count += 1
    print(f"Number of objects containing 'Secrets Manager' in 'answer': {count}")

    
    # Extract lengths of 'question_text'
    lengths = [len(item["question_text"]) for item in data if "question_text" in item]

    # Compute quartiles
    quartiles = np.percentile(lengths, [25, 50, 75, 90, 95, 100])

    # Print results
    print(f"Q1 (25th percentile): {quartiles[0]}")
    print(f"Median (50th percentile): {quartiles[1]}")
    print(f"Q3 (75th percentile): {quartiles[2]}")
    print(f"(90th percentile): {quartiles[3]}")
    print(f"(95th percentile): {quartiles[4]}")
    print(f"(100th percentile): {quartiles[5]}")
