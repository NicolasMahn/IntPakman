from util import Cleric

def main():
    addresses = Cleric.read_semicolon_csv("../data/adresses.csv")

    unique_set = set()
    unique = True

    for addr in addresses:
        str = f"{addr[1]}{addr[2]}{addr[3]}{addr[4]}"
        if str in unique_set:
            unique = false
            break
        unique_set.add(str)

    if unique:
        print("Test passed")
    else:
        print("not unique")




if __name__ == "__main__":
    main()
