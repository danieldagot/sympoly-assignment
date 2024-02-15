# Revised function to better handle lists and potentially fix the issue with empty "Approvers" list
def parse_exrf(file_path):
    data = {}  # Initialize the root of the data structure
    current_context = data  # Pointer to the current working block or list
    context_stack = []  # Stack to keep track of block/list hierarchy
    list_mode = False  # Flag to indicate if currently parsing a list
  
    with open(file_path, 'r') as file: 
        temp_dict = {}
        new_list = []
        list_name
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
                if  not list_mode:
                    current_context[key] = value
                else : 
                  temp_dict[key] = value
            elif line.startswith('[') and  not line.startswith('[['):  # Start of a list
                list_mode = True
                list_name = line.strip('[]')
                temp_dict = {}
                new_list = []
                # current_context = new_list
            elif line.startswith('::::'):
                new_list.append(temp_dict)
                temp_dict = {}
            #     list_mode = True
            elif line.startswith('[[') and line.endswith(']]'):  # End of a list
                current_context[list_name] = new_list
                context_stack.append(current_context)

            #     if context_stack:
            #         current_context = context_stack.pop()
            #     list_mode = False

    return data

# Testing the updated function with the provided EXRF file.