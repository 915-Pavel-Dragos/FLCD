from FA import FA


def print_menu():
    print("1: set of states")
    print("2: alphabet")
    print("3: transitions")
    print("4: initial state")
    print("5: set of final states")
    print("6: check if a sequence is accepted by the fa")
    print("7: Exit")


def main():
    my_fa = FA("FA.in")
    while True:
        print_menu()
        user_choice = int(input("Enter the number corresponding to your choice: "))
        if user_choice == 1:
            print(f"This is the set of states: {my_fa.Q}")
        if user_choice == 2:
            print(f"This is the alphabet: {my_fa.Sigma}")
        if user_choice == 3:
            print(f"This is the set of all transitions: {my_fa.Gamma}")
        if user_choice == 4:
            print(f"This is the initial state: {my_fa.q0}")
        if user_choice == 5:
            print(f"This is the set of final states: {my_fa.F}")
        if user_choice == 6:
            sequence = input("Please enter a sequence to be checked: ")
            if my_fa.sequence_fa_accepted(sequence):
                print("It is accepted.")
            else:
                print("It is not accepted.")
        if user_choice == 7:
            print(f"Goodbye!")
            break


main()
