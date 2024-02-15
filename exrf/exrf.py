import json
def parse_exrf(file_path):
    data = {}  # Initialize the root of the data structure
    current_context = data  # Pointer to the current working block or list
    context_stack = []  # Stack to keep track of block/list hierarchy
    list_mode = False  # Flag to indicate if currently parsing a list
  
    with open(file_path, 'r') as file: 
        temp_dict = {}
        new_list = []
        list_name = ""
        for line in file:
            line = line.strip()
            if line.startswith(':') and not line.endswith('::') and not line.endswith('::::'):  # Start of a new block
                list_mode = False 
                block_name = line.strip(':')
                new_block = {}
                if not list_mode:
                    current_context[block_name] = new_block
                    context_stack.append(current_context)                
                current_context = new_block
            elif line.endswith('::') and not line.endswith('::::'):  # End of a block
                current_context = context_stack.pop()
            elif '::' in line and not line.endswith('::::'):  # Field within a block
                key, value = line.split('::', 1)
                if not list_mode:
                    current_context[key] = value

                else: 
                    temp_dict[key] = value
                # if context_stack:
                    # current_context = context_stack  # Return to the previous context without removing it
            elif line.startswith('[') and not line.startswith('[['):  # Start of a list
                list_mode = True
                list_name = line.strip('[]')
                temp_dict = {}
                new_list = []
            elif line.startswith('::::'):
                new_list.append(temp_dict.copy())  # Use .copy() to ensure a fresh dict is appended
                temp_dict = {}
            elif line.startswith('[[') and line.endswith(']]'):  # End of a list
                new_list.append(temp_dict)
                current_context[list_name] = new_list
                list_mode = False
                # if context_stack:
                #     current_context = context_stack[-1]  # Return to the previous context without removing it

    print(data)
    json_object = json.dumps(data, indent=4)
    
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
    return data

# Test the function with the new EXRF file.
