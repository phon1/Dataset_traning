from datasets import load_dataset
import json

# Tải dataset từ Hugging Face
dataset = load_dataset('jondurbin/airoboros-2.2', split='train')

# Lọc và loại bỏ các dòng trùng lặp dựa trên category
list_category = set()
filtered_data = []

# Định nghĩa một hàm để đếm số lần xuất hiện của một category trong filtered_data
def count_category(category):
    count = sum(1 for data in filtered_data if data['category'] == category)
    return count

for example in dataset:
    category = example['category']
    if category not in list_category:
        list_category.add(category)

for data in dataset:
    if list_category:
        category = data['category']
        if category in list_category:
            if count_category(category) < 50:
                filtered_data.append({
                    'instruction': data['instruction'],
                    'response': data['response'],
                    'category': category,
                    'skip_prompt_formatting': data['skip_prompt_formatting'],
                    'system': data['system']
                })
            else:
                list_category.discard(category)
    else:
        break


# Ghi danh sách filtered_data vào tệp JSON
with open('airoboros.json', 'w', encoding='utf-8') as json_file:
    json.dump(filtered_data, json_file, ensure_ascii=False, indent=4)
