import sys
import os
import argparse

# Add parent directory to path so we can import src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import TaRFM
from src.io import DatabaseReader

DATASETS = {
    "foodmart": {
        "tx": "foodmartFIM.txt",
        "qi": "214,763",
        "alpha": 0.01,
        "beta": 10.0,
        "gamma": 0.2,
        "delta": 0.01
    },
    "fruithut": {
        "tx": "fruithut_original.txt",
        "qi": "1079,2032",
        "alpha": 0.01,
        "beta": 10.0,
        "gamma": 0.2,
        "delta": 0.01
    },
    "retail": {
        "tx": "retail.txt",
        "qi": "39,40",
        "alpha": 0.01,
        "beta": 10.0,
        "gamma": 0.2,
        "delta": 0.01
    },
    "bms1": {
        "tx": "BMS1_itemset_mining.txt",
        "qi": "12695,12703",
        "alpha": 0.01,
        "beta": 10.0,
        "gamma": 0.2,
        "delta": 0.01
    },
    "ecommerce": {
        "tx": "ecommerce_time_without_utility.txt",
        "qi": "22632,22633",
        "alpha": 0.01,
        "beta": 10.0,
        "gamma": 0.2,
        "delta": 0.01
    },
    "sample": {
        "tx": "transactions.txt",
        "qi": "A,B",
        "alpha": 0.2,
        "beta": 80.0,
        "gamma": 1.5,
        "delta": 0.01
    }
}

def main():
    parser = argparse.ArgumentParser(description="TaRFM Pattern Mining")
    parser.add_argument("--dataset", choices=list(DATASETS.keys()), help="Select a predefined dataset to run")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_util = os.path.join(base_dir, "data", "sample", "external_utility.txt")
    
    parser.add_argument("--tx", help="Path to transactions file")
    parser.add_argument("--util", default=default_util, help="Path to external utility file")
    parser.add_argument("--qi", help="Query items separated by comma")
    parser.add_argument("--delta", type=float, help="Decay rate")
    parser.add_argument("--gamma", type=float, help="Min recency")
    parser.add_argument("--alpha", type=float, help="Min frequency ratio")
    parser.add_argument("--beta", type=float, help="Min monetary")
    
    args = parser.parse_args()

    if args.dataset:
        conf = DATASETS[args.dataset]
        tx_file = args.tx if args.tx else os.path.join(base_dir, "data", "sample", conf["tx"])
        qi_str = args.qi if args.qi else conf["qi"]
        delta = args.delta if args.delta is not None else conf["delta"]
        gamma = args.gamma if args.gamma is not None else conf["gamma"]
        alpha = args.alpha if args.alpha is not None else conf["alpha"]
        beta = args.beta if args.beta is not None else conf["beta"]
    else:
        tx_file = args.tx if args.tx else os.path.join(base_dir, "data", "sample", "foodmartFIM.txt")
        qi_str = args.qi if args.qi else "214,763"
        delta = args.delta if args.delta is not None else 0.01
        gamma = args.gamma if args.gamma is not None else 0.2
        alpha = args.alpha if args.alpha is not None else 0.01
        beta = args.beta if args.beta is not None else 10.0

    util_file = args.util
    qi_set = set(item.strip() for item in qi_str.split(','))

    # Đọc dữ liệu
    reader = DatabaseReader()
    try:
        database = reader.read(tx_file, util_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure the sample data files exist.")
        return

    print(f"Dataset: {args.dataset if args.dataset else 'custom'}")
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
        items_with_names = []
        for item in sorted(list(p.get_items())):
            name = reader.item_translation.get(item)
            if name:
                items_with_names.append(f"{item} ({name})")
            else:
                items_with_names.append(item)
        print(f"Pattern{items_with_names}  R={p.get_recency():.2f}  F={p.get_frequency()}  M={p.get_monetary():.2f}")

if __name__ == "__main__":
    main()
