import json

def display_menu():
    print("\nChoose an action:")
    print("1. add    (program will prompt you for a key and value to add)")
    print("2. delete (program deletes key and value if key exists")
    print("3. quit   ('q' or 'quit' exits the program)")

def add_key_value(dictionary):
    key = input("Enter the key: ")
    value = input("Enter the value: ")
    dictionary[key] = value
    print(f"Added ({key}: {value})")
    display_dictionary(dictionary)

def delete_key(dictionary):
    key = input("Enter the key to delete: ")
    if key in dictionary:
        del dictionary[key]
        print(f"Deleted key: {key}")
    else:
        print(f"Key '{key}' not found.")
    display_dictionary(dictionary)

def display_dictionary(dictionary):
    print("\nCurrent dictionary contents:")
    print(json.dumps(dictionary, indent=4))

def main():
    print("Welcome to the Python Dictionary Exercise!\n")
    print("A dictionary in Python is a collection of key-value pairs.")
    print("Keys are unique identifiers that you use to access values.")
    print("Values can be any valid python datatype, and can be looked up using their key.")
    print("A key can only appear in a dictionary once, but two keys can have the same value.")
    print("Entering a key with a new value replaces its old value.")
    print("Deleting a key will also delete its value.")
    print("Deleting a key that does not exist will throw an error.\n")
    input("Hit 'Enter' when you are read to begin...")
        
    dictionary = {}
    
    while True:
        display_menu()
        action = input("\nEnter your action: ").strip().lower()
        
        if action.startswith("add"):
            add_key_value(dictionary)
        elif action.startswith("delete"):
            delete_key(dictionary)
        elif action in ('q', 'quit'):
            print("Thank you for using the Python Dictionary Exercise. Goodbye!")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
