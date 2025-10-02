import json
import time
from typing import List, Dict, Optional, Any


class TransactionSearcher:
    """
    Class to implement and compare different search algorithms for transaction data
    """
    
    def __init__(self, transactions: List[Dict[str, Any]]):
        """
        Initialize with list of transactions
        
        Args:
            transactions: List of transaction dictionaries
        """
        self.transactions = transactions
        self.transaction_dict = self._build_dictionary()
        
    def _build_dictionary(self) -> Dict[str, Dict[str, Any]]:
        """
        Build a dictionary for O(1) lookup
        Key: transaction ID, Value: transaction object
        
        Returns:
            Dictionary mapping transaction IDs to transaction objects
        """
        return {str(transaction['id']): transaction for transaction in self.transactions}
    
    def linear_search(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """
        Perform linear search to find transaction by ID
        Time Complexity: O(n) - worst case scans entire list
        Space Complexity: O(1) - no extra space needed
        
        Args:
            transaction_id: ID of transaction to find
            
        Returns:
            Transaction dictionary if found, None otherwise
        """
        for transaction in self.transactions:
            if str(transaction['id']) == str(transaction_id):
                return transaction
        return None
    
    def dictionary_lookup(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """
        Perform dictionary lookup to find transaction by ID
        Time Complexity: O(1) - direct hash table access
        Space Complexity: O(n) - stores all transactions in dictionary
        
        Args:
            transaction_id: ID of transaction to find
            
        Returns:
            Transaction dictionary if found, None otherwise
        """
        return self.transaction_dict.get(str(transaction_id))
    
    def benchmark_search(self, transaction_id: str, iterations: int = 1000) -> Dict[str, float]:
        """
        Benchmark both search methods
        
        Args:
            transaction_id: ID to search for
            iterations: Number of times to repeat search
            
        Returns:
            Dictionary with timing results for both methods
        """
        # Benchmark linear search
        start_time = time.perf_counter()
        for _ in range(iterations):
            self.linear_search(transaction_id)
        linear_time = time.perf_counter() - start_time
        
        # Benchmark dictionary lookup
        start_time = time.perf_counter()
        for _ in range(iterations):
            self.dictionary_lookup(transaction_id)
        dict_time = time.perf_counter() - start_time
        
        return {
            'linear_search_time': linear_time,
            'dictionary_lookup_time': dict_time,
            'speedup_factor': linear_time / dict_time if dict_time > 0 else float('inf'),
            'iterations': iterations
        }


def load_transactions_from_json(filepath: str) -> List[Dict[str, Any]]:
    """
    Load transactions from JSON file
    
    Args:
        filepath: Path to JSON file containing transactions
        
    Returns:
        List of transaction dictionaries
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Handle both list format and dict with 'transactions' key
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'transactions' in data:
                return data['transactions']
            else:
                raise ValueError("Invalid JSON format")
    except FileNotFoundError:
        print(f"Error: File {filepath} not found")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filepath}")
        return []


def create_sample_transactions(count: int = 20) -> List[Dict[str, Any]]:
    """
    Create sample transaction data for testing
    
    Args:
        count: Number of sample transactions to create
        
    Returns:
        List of sample transaction dictionaries
    """
    transactions = []
    transaction_types = ['DEPOSIT', 'WITHDRAWAL', 'TRANSFER', 'PAYMENT']
    
    for i in range(1, count + 1):
        transaction = {
            'id': i,
            'type': transaction_types[i % len(transaction_types)],
            'amount': 1000 + (i * 500),
            'sender': f'254700{100000 + i}',
            'receiver': f'254700{200000 + i}',
            'timestamp': f'2024-01-{(i % 28) + 1:02d}T10:00:00Z',
            'status': 'COMPLETED'
        }
        transactions.append(transaction)
    
    return transactions


def run_comprehensive_test(transactions: List[Dict[str, Any]]):
    """
    Run comprehensive tests and comparisons
    
    Args:
        transactions: List of transactions to test with
    """
    print("=" * 80)
    print("DSA INTEGRATION: LINEAR SEARCH VS DICTIONARY LOOKUP")
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
    
    print("SEARCH TESTS")
    print("-" * 80)
    
    for test_id in test_ids:
        print(f"\nSearching for Transaction ID: {test_id}")
        
        # Linear search
        start = time.perf_counter()
        result_linear = searcher.linear_search(test_id)
        time_linear = time.perf_counter() - start
        
        # Dictionary lookup
        start = time.perf_counter()
        result_dict = searcher.dictionary_lookup(test_id)
        time_dict = time.perf_counter() - start
        
        print(f"  Linear Search: {time_linear * 1000000:.2f} µs | Found: {result_linear is not None}")
        print(f"  Dict Lookup:   {time_dict * 1000000:.2f} µs | Found: {result_dict is not None}")
        print(f"  Speedup:       {time_linear / time_dict:.2f}x faster")
    
    # Comprehensive benchmark
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
    import sys
    list_size = sys.getsizeof(searcher.transactions)
    dict_size = sys.getsizeof(searcher.transaction_dict)
    
    print(f"List Size:       {list_size} bytes")
    print(f"Dictionary Size: {dict_size} bytes")
    print(f"Overhead:        {dict_size - list_size} bytes ({((dict_size - list_size) / list_size * 100):.1f}%)")


def generate_analysis_report():
    """
    Generate detailed analysis report
    """
    report = """
================================================================================
ANALYSIS REPORT: LINEAR SEARCH VS DICTIONARY LOOKUP
================================================================================

1. WHY IS DICTIONARY LOOKUP FASTER THAN LINEAR SEARCH?

Dictionary lookup is faster due to the underlying hash table data structure:

a) Time Complexity:
   - Linear Search: O(n) - must check each element sequentially
   - Dictionary Lookup: O(1) average case - direct access via hash function
   
b) Hash Table Mechanism:
   - Dictionaries use a hash function to compute an index for each key
   - This allows direct access to the value without iteration
   - Example: For key "123", hash("123") = index, then access dict[index]

c) Performance Scaling:
   - Linear Search: Time increases proportionally with dataset size
   - Dictionary Lookup: Time remains constant regardless of dataset size
   
d) Real-World Impact:
   - For 20 records: Dictionary is ~10-50x faster
   - For 1000 records: Dictionary is ~100-500x faster
   - For 1 million records: Dictionary is ~100,000x faster


2. SUGGESTED DATA STRUCTURES & ALGORITHMS FOR IMPROVED EFFICIENCY

a) Binary Search Tree (BST):
   - Time Complexity: O(log n) for search, insert, delete
   - Maintains sorted order
   - Best when: Need both fast search AND sorted traversal
   - Trade-off: Slower than hash table but maintains order

b) Binary Search on Sorted List:
   - Time Complexity: O(log n) for search
   - Requires pre-sorting: O(n log n)
   - Best when: Data rarely changes, many searches performed
   - Memory efficient: No additional data structure needed

c) Trie (Prefix Tree):
   - Time Complexity: O(k) where k is key length
   - Best when: Searching by prefixes (e.g., phone numbers)
   - Use case: Auto-complete, phone number search

d) B-Tree / B+ Tree:
   - Time Complexity: O(log n)
   - Best when: Database indexes, disk-based storage
   - Optimized for block storage systems

e) Bloom Filter:
   - Time Complexity: O(k) where k is number of hash functions
   - Best when: Need to check membership quickly with space constraints
   - Trade-off: Small false positive rate, no false negatives


3. SPACE-TIME TRADE-OFF ANALYSIS

Linear Search:
  ✓ Space: O(1) - no additional storage
  ✗ Time: O(n) - slow for large datasets

Dictionary Lookup:
  ✓ Time: O(1) - extremely fast
  ✗ Space: O(n) - requires additional hash table

Recommendation for MoMo Transaction API:
- Use Dictionary (Hash Table) for transaction ID lookups
- Primary key searches need to be fast for good user experience
- Memory overhead is acceptable for the performance gain
- For range queries or sorted results, consider hybrid approach with BST


4. OPTIMIZATION SUGGESTIONS FOR MOMO API

a) Indexing Strategy:
   - Create dictionaries for multiple keys: transaction_id, phone_number, date
   - Enables fast lookup on different fields

b) Caching:
   - Cache frequently accessed transactions in memory
   - Use LRU (Least Recently Used) cache to limit memory

c) Database Indexes:
   - Ensure database has B-tree indexes on frequently queried columns
   - Composite indexes for multi-field queries

d) Query Optimization:
   - For range queries (date ranges), use sorted structures or DB queries
   - For exact matches, use hash-based lookups

e) Pagination:
   - For GET /transactions, implement pagination
   - Return limited results to reduce response time

================================================================================
"""
    return report


def main():
    """
    Main execution function
    """
    print("\nMoMo Transaction DSA Analysis")
    print("Author: Selena ISIMBI\n")
    
    # Try to load from file, otherwise create sample data
    transactions = load_transactions_from_json('transactions.json')
    
    if not transactions or len(transactions) < 20:
        print("Creating sample transactions for testing...\n")
        transactions = create_sample_transactions(20)
    
    # Run comprehensive tests
    run_comprehensive_test(transactions)
    
    # Generate and print analysis report
    print("\n")
    print(generate_analysis_report())
    
    # Save sample data for API testing
    with open('sample_transactions.json', 'w', encoding='utf-8') as f:
        json.dump(transactions, f, indent=2)
    print(f"\n✓ Sample data saved to 'sample_transactions.json'")


if __name__ == "__main__":
    main()
