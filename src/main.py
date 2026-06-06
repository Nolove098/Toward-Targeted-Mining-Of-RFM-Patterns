import sys
import os
import argparse

# Add parent directory to path so we can import src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import TaRFM
from src.io import DatabaseReader

def main():
    parser = argparse.ArgumentParser(description="TaRFM Pattern Mining")
    parser.add_argument("--tx", default="data/sample/transactions.txt", help="Path to transactions file")
    parser.add_argument("--util", default="data/sample/external_utility.txt", help="Path to external utility file")
    parser.add_argument("--qi", default="A,B", help="Query items separated by comma")
    parser.add_argument("--delta", type=float, default=0.01, help="Decay rate")
    parser.add_argument("--gamma", type=float, default=1.5, help="Min recency")
    parser.add_argument("--alpha", type=float, default=0.2, help="Min frequency ratio")
    parser.add_argument("--beta", type=float, default=80.0, help="Min monetary")
    
    args = parser.parse_args()

    tx_file = args.tx
    util_file = args.util
    
    qi_set = set(item.strip() for item in args.qi.split(','))
    delta = args.delta
    gamma = args.gamma
    alpha = args.alpha
    beta = args.beta

    # Đọc dữ liệu
    reader = DatabaseReader()
    try:
        database = reader.read(tx_file, util_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure the sample data files exist.")
        return

    print(f"Database loaded: {len(database)} transactions")
    print(f"Query itemset Qi = {qi_set}")
    print(f"Parameters: delta={delta} gamma={gamma} alpha={alpha} beta=${beta}")
    print("-" * 60)

    # Chạy TaRFM
    tarfm = TaRFM()
    patterns = tarfm.run(database, qi_set, delta, gamma, alpha, beta)

    # In kết quả
    print(f"\nTaRFM Patterns found: {len(patterns)}")
    print("-" * 60)
    for p in patterns:
        print(p)

if __name__ == "__main__":
    main()
