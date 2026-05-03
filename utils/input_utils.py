def yes_no_to_boolean(prompt: str, allow_for_None: bool = False):
    prompt_clean = (
        prompt.strip().removesuffix("?").removesuffix(" ") + " (y/n)? "
        if not prompt.endswith("(y/n)? ")
        else prompt 
    )

    while True:
        inp = input(prompt_clean)
        if inp is None and not allow_for_None:
            return None
        if inp in ["yes", "y"]:
            return True
        elif inp in ["no", "n"]:
            return False
        print("Please Enter yes or no.")

def select_from_list(options: list[str], prompt = "Options:", select_multiple: bool = False) -> str | list[str]:
    if options is None or len(options) == 0:
        print("options list is None. Returning.")
        return ""
    options_number_list: list[str] = [f"{i + 1}) " for i in range(len(options))]
    remaining_options: list[str] = options.copy()
    res = []
    len_remaining_options = len(remaining_options)
    while len_remaining_options > 0:
        print(prompt)
        print(*[i + j for i, j in zip(options_number_list[:len_remaining_options], remaining_options)], sep="\n")
        print()
        inp = input("> ")
        if inp == "":
            break
        
        if inp.isnumeric() and 0 < int(inp) <= len_remaining_options:
            res.append(remaining_options[int(inp) - 1])
            remaining_options.remove(remaining_options[int(inp) - 1])
            len_remaining_options = len(remaining_options)
            
        if not select_multiple: 
            break
    
    if res == []: 
        return res
    
    print()
    print(*res, sep="\n")
    return (res
        if yes_no_to_boolean("\nIs this correct?")
        else select_from_list(options, prompt= prompt, select_multiple=select_from_list))
        
if __name__ == "__main__":
    pass