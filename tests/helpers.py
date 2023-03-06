

# Used to invalidate invoice
# To be replaced with Denzel's better function
def remove_part_of_string(string, start, end):
    return string[:start] + string[end:]

def replace_part_of_string(string, start, end, replace):
    return string[:start] + replace + string[end:]
