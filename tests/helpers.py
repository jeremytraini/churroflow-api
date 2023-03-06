

# Used to invalidate invoice
# To be replaced with Denzel's better function
def remove_part_of_string(string, start, end):
    return string[:start] + string[end:]

def check_equal(a, b):
    if len(a) != len(b):
        print ("String lengths not equal")
        return
    else:
        for i in range(len(b)):
            if a[i] != b[i]:
                return False

    print ("Strings are equal and same")     