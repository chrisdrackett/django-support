def process_full_name(full_name):
    first_name = full_name.split(" ")[0].strip(" ")
    last_name = " ".join(full_name.split(" ")[1:]).strip(" ")
    
    return (first_name, last_name)