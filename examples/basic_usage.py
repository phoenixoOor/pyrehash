from src.attacks.dictionary_attack import DictionaryAttack
from src.core.hash_utils import detect_algorithm

def main():
    target_hash = "5f4dcc3b5aa765d61d8327deb882cf99" # 'password'
    
    # Auto-detect algorithm
    algo = detect_algorithm(target_hash)
    print(f"Detected algorithm: {algo}")
    
    # Initialize engine
    engine = DictionaryAttack(target_hash, algo)
    
    # Create a dummy dictionary file
    with open("mini_dict.txt", "w") as f:
        f.write("admin\n123456\npassword\nroot")
    
    print("Starting attack...")
    result = engine.run("mini_dict.txt")
    
    if result:
        print(f"Success! Password is: {result}")
    else:
        print("Failed to find password.")

if __name__ == "__main__":
    main()
