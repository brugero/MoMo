## 📋 Overview

This module implements and compares different search algorithms for efficiently finding transactions in the MoMo SMS data processing system. It demonstrates the practical application of Data Structures and Algorithms (DSA) concepts in API development.

##  Objectives

1. Implement **Linear Search** algorithm for transaction lookup
2. Implement **Dictionary (Hash Table) Lookup** for O(1) access
3. Compare performance and efficiency of both methods
4. Provide recommendations for optimal data structure selection
5. Demonstrate real-world DSA applications in API development

##  Module Structure

```
dsa/
├── search_comparison.py    # Main implementation file
├── test_search.py          # Unit tests
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

##  Quick Start

### Prerequisites

```bash
Python 3.8+
```

### Installation

```bash
# Navigate to the dsa directory
cd dsa/

# Install dependencies (if any)
pip install -r requirements.txt
```

### Running the Code

```bash
# Run the main comparison
python search_comparison.py

# Run unit tests
python test_search.py
```

##  Implementation Details

### 1. Linear Search

**Algorithm:** Sequential scan through the list of transactions

**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def linear_search(self, transaction_id: str) -> Optional[Dict[str, Any]]:
    for transaction in self.transactions:
        if str(transaction['id']) == str(transaction_id):
            return transaction
    return None
```

**Pros:**
- No preprocessing required
- No additional memory needed
- Simple to implement

**Cons:**
- Slow for large datasets
- Performance degrades linearly with size
- Not suitable for frequent searches

### 2. Dictionary Lookup

**Algorithm:** Hash table-based direct access

**Time Complexity:** O(1) average case  
**Space Complexity:** O(n)

```python
def dictionary_lookup(self, transaction_id: str) -> Optional[Dict[str, Any]]:
    return self.transaction_dict.get(str(transaction_id))
```

**Pros:**
- Extremely fast lookups
- Constant time regardless of dataset size
- Ideal for APIs with frequent searches

**Cons:**
- Requires additional memory
- Preprocessing step needed to build dictionary
- Hash collisions possible (rare)

##  Performance Results

### Test Configuration
- Dataset: 20 transactions
- Iterations: 1000 per benchmark
- Test cases: First, middle, and last transaction IDs

### Sample Results

```
SEARCH TESTS
--------------------------------------------------------------------------------
Searching for Transaction ID: 1
  Linear Search: 2.34 µs | Found: True
  Dict Lookup:   0.18 µs | Found: True
  Speedup:       13.00x faster

Searching for Transaction ID: 10
  Linear Search: 4.56 µs | Found: True
  Dict Lookup:   0.19 µs | Found: True
  Speedup:       24.00x faster

Searching for Transaction ID: 20
  Linear Search: 8.92 µs | Found: True
  Dict Lookup:   0.18 µs | Found: True
  Speedup:       49.56x faster
```

### Key Findings

1. **Dictionary lookup is 13-50x faster** than linear search on 20 records
2. **Linear search degrades** as target ID is further in the list
3. **Dictionary lookup remains constant** regardless of position
4. For 1000+ records, speedup can reach **100-500x**

##  Analysis: Why Dictionary Lookup is Faster

### Hash Table Mechanism

1. **Hash Function:** Computes index from key
   ```
   hash("123") → 7 → dict[7] = transaction_object
   ```

2. **Direct Access:** No iteration needed
   - Linear Search: Must check items 1, 2, 3, ..., n
   - Dictionary: Jump directly to item using hash

3. **Scaling Properties:**
   - Linear Search: Time ∝ Dataset Size
   - Dictionary: Time ≈ Constant

### Big O Notation Comparison

| Operation | Linear Search | Dictionary Lookup |
|-----------|---------------|-------------------|
| Search    | O(n)          | O(1)              |
| Insert    | O(1)          | O(1)              |
| Delete    | O(n)          | O(1)              |
| Memory    | O(n)          | O(n)              |

##  Alternative Data Structures

### 1. Binary Search Tree (BST)

**Time Complexity:** O(log n)

**Best For:**
- Need sorted order traversal
- Range queries (e.g., transactions between dates)
- Balanced read/write operations

**Example Use Case:**
```python
# Find all transactions between $100 and $500
tree.range_search(100, 500)
```

### 2. Binary Search (on Sorted List)

**Time Complexity:** O(log n)

**Best For:**
- Read-heavy workloads
- Data rarely changes
- Memory-constrained environments

**Trade-off:** Requires O(n log n) sorting first

### 3. Trie (Prefix Tree)

**Time Complexity:** O(k) where k = key length

**Best For:**
- Phone number prefix search
- Auto-complete features
- String-based keys

**Example Use Case:**
```python
# Find all transactions from numbers starting with "25470"
trie.prefix_search("25470")
```

### 4. B-Tree / B+ Tree

**Time Complexity:** O(log n)

**Best For:**
- Database indexes
- Disk-based storage
- Range queries with pagination

**Why Databases Use This:**
- Optimized for block storage
- Reduces disk I/O operations

### 5. Bloom Filter

**Time Complexity:** O(k) where k = hash functions

**Best For:**
- Quick membership testing
- Space-constrained scenarios
- Can tolerate false positives

**Trade-off:** 
- Can have false positives
- Cannot retrieve actual data
- Good for "does this transaction exist?" checks

##  Recommendations for MoMo API

### Primary Recommendation: Dictionary (Hash Table)

**Why:**
1.  O(1) lookup for transaction IDs
2.  Fast enough for real-time API responses
3.  Memory overhead acceptable for performance gain
4.  Easy to maintain and understand

### Hybrid Approach for Advanced Features

```python
class OptimizedTransactionStore:
    def __init__(self):
        # Fast ID lookup
        self.id_index = {}  # transaction_id → transaction
        
        # Fast phone number lookup
        self.phone_index = {}  # phone → list of transactions
        
        # Sorted structure for range queries
        self.date_sorted = []  # sorted by timestamp
        
        # Prefix search for phone numbers
        self.phone_trie = Trie()
```

### Implementation Strategy

1. **For Exact Match Queries:**
   - Use dictionary/hash table
   - Examples: GET /transactions/{id}

2. **For Range Queries:**
   - Use sorted list + binary search
   - Examples: GET /transactions?start_date=X&end_date=Y

3. **For Prefix Searches:**
   - Use Trie
   - Examples: GET /transactions?phone_prefix=25470

4. **For Existence Checks:**
   - Use Bloom Filter
   - Examples: "Has this transaction been processed?"

##  Testing

### Run Unit Tests

```bash
python test_search.py
```

### Expected Output

```
DSA UNIT TESTS
================================================================================
Running test suite...

test_linear_search_found ... ok
test_dictionary_lookup_found ... ok
test_both_methods_return_same_result ... ok
test_dictionary_is_faster ... ok

TEST SUMMARY
================================================================================
Tests Run: 10
Successes: 10
Failures: 0
Errors: 0
```

##  Performance Benchmarking

### Scaling Test Results

| Dataset Size | Linear Search | Dictionary | Speedup |
|--------------|---------------|------------|---------|
| 20 records   | 5.2 µs        | 0.2 µs     | 26x     |
| 100 records  | 24.1 µs       | 0.2 µs     | 120x    |
| 1000 records | 248.7 µs      | 0.2 µs     | 1244x   |
| 10000 records| 2.5 ms        | 0.2 µs     | 12500x  |

##  Integration with API

### Example Usage in API Endpoints

```python
from dsa.search_comparison import TransactionSearcher

# Initialize once when server starts
transactions = load_transactions()
searcher = TransactionSearcher(transactions)

# In your API endpoint handler
def handle_get_transaction(transaction_id):
    # Fast O(1) lookup
    transaction = searcher.dictionary_lookup(transaction_id)
    
    if transaction:
        return json_response(transaction, 200)
    else:
        return json_response({'error': 'Transaction not found'}, 404)
```

### API Performance Impact

**Without Optimization (Linear Search):**
- 1000 transactions: ~250 µs per request
- 10,000 transactions: ~2.5 ms per request
- 100,000 transactions: ~25 ms per request (Too slow!)

**With Optimization (Dictionary):**
- Any dataset size: ~0.2 µs per request  (Excellent!)

##  Security Considerations

While implementing search algorithms, consider:

1. **Input Validation:**
   ```python
   # Prevent injection attacks
   transaction_id = sanitize_input(transaction_id)
   ```

2. **Rate Limiting:**
   ```python
   # Prevent DoS via excessive searches
   if search_count > MAX_SEARCHES_PER_MINUTE:
       return error_response('Rate limit exceeded')
   ```

3. **Memory Management:**
   ```python
   # Limit dictionary size to prevent memory exhaustion
   if len(transaction_dict) > MAX_TRANSACTIONS:
       implement_cache_eviction()
   ```

##  Learning Outcomes

### Key Concepts Demonstrated

1. **Time Complexity Analysis**
   - Understanding Big O notation
   - Comparing algorithmic efficiency
   - Predicting performance at scale

2. **Space-Time Trade-offs**
   - Dictionary uses more memory but faster
   - Choosing appropriate data structure for use case

3. **Hash Table Internals**
   - How Python dictionaries work
   - Hash functions and collision handling
   - Average vs worst-case performance

4. **Practical Algorithm Application**
   - Real-world use in API development
   - Performance benchmarking
   - Data structure selection criteria

##  Experimental Results

### Memory Usage Analysis

```
Dataset: 20 transactions

List Size:       920 bytes
Dictionary Size: 736 bytes
Overhead:        -184 bytes (-20.0%)
Note: Overhead becomes positive with larger datasets
```

### Detailed Benchmark Output

```
PERFORMANCE BENCHMARK (1000 iterations)
Transaction ID: 10
Linear Search Total Time:    4.5621 ms
Dictionary Lookup Total Time: 0.1823 ms
Speedup Factor:              25.02x

Per Operation:
  Linear Search:    4.56 µs
  Dictionary Lookup: 0.18 µs
```

##  Development Notes

### Code Quality

-  Type hints for better code clarity
-  Comprehensive docstrings
-  Error handling for edge cases
-  Unit tests for all methods
-  Performance benchmarking included

### Dependencies

```txt
# requirements.txt
# No external dependencies required!
# Uses only Python standard library:
# - json
# - time
# - typing
# - unittest
```

##  References & Further Reading

### Academic Resources

1. **Introduction to Algorithms** (CLRS)
   - Chapter 11: Hash Tables
   - Chapter 12: Binary Search Trees

2. **Python Documentation**
   - [dict objects](https://docs.python.org/3/library/stdtypes.html#dict)
   - [time.perf_counter()](https://docs.python.org/3/library/time.html#time.perf_counter)

### Online Resources

1. [Big O Cheat Sheet](https://www.bigocheatsheet.com/)
2. [Python Time Complexity](https://wiki.python.org/moin/TimeComplexity)
3. [Hash Table Visualization](https://visualgo.net/en/hashtable)

##  Contributing

### Team Members

- **Selena ISIMBI** - DSA Integration Lead
- **Ulrich RUKAZAMBUGA** - Data Parsing
- **Albert NIYONSENGA** - Authentication & Security
- **Beulla RUGERO** - API Implementation
- **Sonia KIBYEYI** - API Documentation

### Code Review Checklist

- [ ] All tests pass
- [ ] Performance benchmarks run successfully
- [ ] Code follows team style guide
- [ ] Documentation updated
- [ ] No security vulnerabilities

##  Support

For questions or issues:

1. Check this README first
2. Review code comments and docstrings
3. Contact team lead: Selena ISIMBI
4. Create issue in GitHub repository

##  License

MIT License - See LICENSE file in repository root

##  Acknowledgments

- Team Data Raiders for collaboration
- Course instructors for guidance
- Python community for excellent documentation
