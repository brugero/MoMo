# DSA Integration: Search Algorithm Comparison

**Author:** Selena ISIMBI  
**Project:** MoMo Transaction API  
**Team:** Data Raiders

##  Overview

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

Running test suite...

test_linear_search_found ... ok
test_dictionary_lookup_found ... ok
test_both_methods_return_same_result ... ok
test_dictionary_is_faster ... ok

TEST SUMMARY
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
| 100 records  |
