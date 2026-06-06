import random
import os

def generate_synthetic_data(num_transactions=1000, num_items=50, output_dir="data/synthetic"):
    os.makedirs(output_dir, exist_ok=True)
    
    tx_file = os.path.join(output_dir, "transactions.txt")
    util_file = os.path.join(output_dir, "external_utility.txt")
    
    # Generate items
    items = [f"I{i}" for i in range(1, num_items + 1)]
    # Special query items will be I1, I2 for testing
    
    # Write external utility
    # Prices random from 1.0 to 200.0
    with open(util_file, "w") as f:
        for item in items:
            price = round(random.uniform(1.0, 200.0), 2)
            f.write(f"{item}:{price}\n")
            
    # Write transactions
    with open(tx_file, "w") as f:
        for i in range(num_transactions):
            # random length of transaction: 1 to 15 items
            tx_len = random.randint(1, 15)
            # Pick random items without replacement
            tx_items = random.sample(items, tx_len)
            
            # For 20% of transactions, let's inject our query items [I1, I2]
            # to make sure we find some patterns
            if random.random() < 0.2:
                if "I1" not in tx_items: tx_items.append("I1")
                if "I2" not in tx_items: tx_items.append("I2")
                # Add another common item to form a larger pattern
                if "I3" not in tx_items: tx_items.append("I3")
            
            line_parts = []
            for item in tx_items:
                qty = random.randint(1, 10) # Quantity from 1 to 10
                line_parts.append(f"{item}:{qty}")
            
            f.write(" ".join(line_parts) + "\n")
            
    print(f"Generated {num_transactions} transactions in {tx_file}")
    print(f"Generated {num_items} utilities in {util_file}")

if __name__ == "__main__":
    generate_synthetic_data()
