import sys
import json
from ai_model import AI

# Load a pre‑populated knowledge base if desired (for demo we just use the simple AI class)

def load_kb(ai, path='knowledge.json'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for entry in data:
            ai.add_node(entry['path'], entry['value'])
        print(f"Loaded {len(data)} knowledge entries.")
    except FileNotFoundError:
        print('No knowledge file found, starting empty.')

def save_kb(ai, path='knowledge.json'):
    # Serialize the tree recursively
    def recurse(node):
        result = []
        for key, child in node.children.items():
            if child.value is not None:
                result.append({'path': [key], 'value': child.value})
            # prepend current key to children's paths
            for sub in recurse(child):
                sub['path'] = [key] + sub['path']
                result.append(sub)
        return result
    data = recurse(ai.root)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data)} knowledge entries.")


def main():
    ai = AI()
    load_kb(ai)
    print("FATE – your coding partner. Type 'exit' to quit.")
    while True:
        try:
            user = input('You: ').strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user.lower() in ('exit', 'quit'):
            break
        # Simple parsing: treat space‑separated words as a path
        path = user.split()
        answer = ai.query(path)
        if answer:
            print(f'FATE: {answer}')
        else:
            print('FATE: I do not have knowledge on that. Would you like to add it? (yes/no)')
            resp = input('You: ').strip().lower()
            if resp.startswith('y'):
                value = input('Enter the information to store: ')
                ai.add_node(path, value)
                print('Knowledge added.')
    save_kb(ai)
    print('Goodbye!')

if __name__ == '__main__':
    main()
