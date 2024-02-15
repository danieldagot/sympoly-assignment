def print_pattern(num):
    # Upper part of the pattern
    for i in range(1, num + 1):
        # Printing spaces
        print(' ' * (num - i), end='')
        # Printing stars
        print('*' * i, end=' ')
        print('*' * i)
    
    # Lower part of the pattern
    for i in range(num - 1, 0, -1):
        # Printing spaces
        print(' ' * (num - i), end='')
        # Printing stars
        print('*' * i, end=' ')
        print('*' * i)

# Example usage
num = 10
print_pattern(num)
