import json
import time
import sys
from typing import List, Dict, Optional, Any


class TransactionSearcher:
    """
    Class to implement and compare different search algorithms for transaction data
    Used in our MoMo API project for the DSA assignment
    """
    
    def __init__(self, transactions: List[Dict[str, Any]]):
        """
        Initialize with MoMo transaction data from our XML parsing
        Using the actual transaction structure Ulrich parsed from modified_sms_v2.xml
        """
        self.transactions = transactions
        self.transaction_dict = self._build_dictionary()
        print(f"Loaded {len(transactions)} MoMo transactions for search testing")
        
    def _build_dictionary(self) -> Dict[str, Dict[str, Any]]:
        """
        Build a dictionary for O(1) lookup - this is our performance optimization
        """
        transaction_dict = {}
        for transaction in self.transactions:
            # Handle both string and integer IDs from the dataset
            transaction_dict[str(transaction.get('id', ''))] = transaction
        return transaction_dict
    
    def linear_search(self, transaction_id: str, verbose: bool = False) -> Optional[Dict[str, Any]]:
        """
        Perform linear search to find transaction by ID
        Time Complexity: O(n) - worst case scans entire list
        """
        if verbose:
            print(f"Linear search for ID: {transaction_id}")
        
        search_count = 0
        for transaction in self.transactions:
            search_count += 1
            # Compare string representations to handle different ID formats
            if str(transaction.get('id', '')) == str(transaction_id):
                if verbose:
                    print(f"Found after {search_count} checks")
                return transaction
        
        if verbose:
            print(f"Not found after {search_count} checks")
        return None
    
    def dictionary_lookup(self, transaction_id: str, verbose: bool = False) -> Optional[Dict[str, Any]]:
        """
        Perform dictionary lookup to find transaction by ID
        Time Complexity: O(1) - direct hash table access
        """
        result = self.transaction_dict.get(str(transaction_id))
        if verbose:
            if result:
                print(f"Dictionary lookup found ID: {transaction_id}")
            else:
                print(f"Dictionary lookup - ID not found: {transaction_id}")
        return result
    
    def benchmark_search(self, transaction_id: str, iterations: int = 1000) -> Dict[str, float]:
        """
        Compare our two search approaches with accurate timing
        """
        print(f"Benchmarking {iterations} searches for ID: {transaction_id}")
        
        # Benchmark linear search (without debug prints)
        start_time = time.perf_counter()
        for _ in range(iterations):
            self.linear_search(transaction_id, verbose=False)
        linear_time = time.perf_counter() - start_time
        
        # Benchmark dictionary lookup (without debug prints)
        start_time = time.perf_counter()
        for _ in range(iterations):
            self.dictionary_lookup(transaction_id, verbose=False)
        dict_time = time.perf_counter() - start_time
        
        results = {
            'linear_search_time': linear_time,
            'dictionary_lookup_time': dict_time,
            'speedup_factor': linear_time / dict_time if dict_time > 0 else float('inf'),
            'iterations': iterations
        }
        
        if results['speedup_factor'] > 10:
            print(f"Dictionary is {results['speedup_factor']:.1f}x faster - significant improvement")
        else:
            print(f"Dictionary is {results['speedup_factor']:.1f}x faster")
            
        return results


def load_transactions_from_json(filepath: str) -> List[Dict[str, Any]]:
    """
    Load transactions from JSON file - this should match Ulrich's parsed data
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'transactions' in data:
                return data['transactions']
            else:
                print("JSON format not recognized - expected list or dict with 'transactions' key")
                return []
    except FileNotFoundError:
        print(f"File {filepath} not found - using sample data instead")
        return []
    except json.JSONDecodeError:
        print(f"Invalid JSON in {filepath} - using sample data instead")
        return []
    except Exception as e:
        print(f"Error loading {filepath}: {e} - using sample data instead")
        return []


def create_sample_transactions(count: int = 25) -> List[Dict[str, Any]]:
    """
    Create sample data that matches our actual MoMo transaction structure
    Based on the typical SMS transaction format
    """
    print(f"Creating {count} sample MoMo transactions for testing...")
    transactions = []
    
    # Using realistic MoMo transaction types
    transaction_types = ['received', 'sent', 'withdrawal', 'deposit', 'payment']
    
    for i in range(1, count + 1):
        transaction = {
            'id': i,  # Using integer IDs which are common in datasets
            'transaction_type': transaction_types[i % len(transaction_types)],
            'amount': f"{1500 + (i * 237)}",
            'sender': f"25078{100000 + i:06d}",  # Rwandan phone number format
            'receiver': f"25072{200000 + i:06d}",
            'timestamp': f"2024-01-{(i % 28) + 1:02d}T08:{30 + i % 30:02d}:00Z",
            'message': f"Payment for goods #{i}",
            'status': 'completed'
        }
        transactions.append(transaction)
    
    return transactions


def run_comprehensive_test(transactions: List[Dict[str, Any]]):
    """
    Run comprehensive tests and comparisons for our DSA assignment
    """
    print("\n" + "=" * 80)
    print("DSA INTEGRATION: LINEAR SEARCH VS DICTIONARY LOOKUP")
    print("Team Data Raiders | Selena - DSA Implementation")
    print("=" * 80)
    print(f"\nDataset Size: {len(transactions)} transactions\n")
    
    # Initialize searcher
    searcher = TransactionSearcher(transactions)
    
    # Test with different transaction IDs (beginning, middle, end)
    test_ids = [
        str(transactions[0]['id']),  # First transaction
        str(transactions[len(transactions) // 2]['id']),  # Middle transaction  
        str(transactions[-1]['id'])  # Last transaction
    ]
    
    print("SEARCH PERFORMANCE TESTS")
    print("-" * 80)
    
    for test_id in test_ids:
        print(f"\nSearching for Transaction ID: {test_id}")
        
        # Test searches with verbose output
        print("Linear search:", end=" ")
        start = time.perf_counter()
        result_linear = searcher.linear_search(test_id, verbose=True)
        time_linear = time.perf_counter() - start
        
        print("Dictionary lookup:", end=" ")
        start = time.perf_counter()
        result_dict = searcher.dictionary_lookup(test_id, verbose=True)
        time_dict = time.perf_counter() - start
        
        print(f"  Linear Search: {time_linear * 1000000:.2f} µs")
        print(f"  Dict Lookup:   {time_dict * 1000000:.2f} µs")
        print(f"  Speedup:       {time_linear / time_dict:.2f}x faster")
    
    # Comprehensive benchmark (without verbose output)
    print("\n" + "=" * 80)
    print("PERFORMANCE BENCHMARK (1000 iterations)")
    print("=" * 80)
    
    # Test with middle element (average case)
    middle_id = str(transactions[len(transactions) // 2]['id'])
    results = searcher.benchmark_search(middle_id, iterations=1000)
    
    print(f"\nTransaction ID: {middle_id}")
    print(f"Linear Search Total Time:    {results['linear_search_time'] * 1000:.4f} ms")
    print(f"Dictionary Lookup Total Time: {results['dictionary_lookup_time'] * 1000:.4f} ms")
    print(f"Speedup Factor:              {results['speedup_factor']:.2f}x")
    print(f"\nPer Operation:")
    print(f"  Linear Search:    {results['linear_search_time'] / results['iterations'] * 1000000:.2f} µs")
    print(f"  Dictionary Lookup: {results['dictionary_lookup_time'] / results['iterations'] * 1000000:.2f} µs")
    
    # Memory analysis
    print("\n" + "=" * 80)
    print("MEMORY ANALYSIS")
    print("=" * 80)
    
    list_size = sys.getsizeof(searcher.transactions)
    # Calculate dictionary size more accurately
    dict_size = sys.getsizeof(searcher.transaction_dict)
    for key, value in searcher.transaction_dict.items():
        dict_size += sys.getsizeof(key) + sys.getsizeof(value)
    
    print(f"List Size:       {list_size} bytes")
    print(f"Dictionary Size: {dict_size} bytes")
    print(f"Memory Overhead: {dict_size - list_size} bytes ({((dict_size - list_size) / list_size * 100):.1f}%)")


def main():
    """
    Main function for our DSA assignment - testing search algorithms
    """
    print("\n" + "="*60)
    print("MoMo Transaction Search - DSA Implementation")
    print("Team Data Raiders | Selena - DSA Lead")
    print("="*60)
    
    # Try loading from multiple possible locations
    possible_paths = [
        '../api/transactions.json',
        './transactions.json',
        '../transactions.json'
    ]
    
    transactions = []
    for path in possible_paths:
        transactions = load_transactions_from_json(path)
        if transactions:
            print(f"Loaded transactions from {path}")
            break
    
    if not transactions:
        print("Using sample data (real parsing in progress by Ulrich)")
        transactions = create_sample_transactions(25)
    
    # Run our comparison tests
    run_comprehensive_test(transactions)
    
    # Save sample data for API testing
    with open('sample_transactions.json', 'w', encoding='utf-8') as f:
        json.dump(transactions, f, indent=2)
    print(f"Sample data saved to 'sample_transactions.json'")
    
    print("\nKey Insight: Dictionary lookup is essential for fast API responses!")
    print("Ready for integration with Beulla's API endpoints!")


if __name__ == "__main__":
    main()
