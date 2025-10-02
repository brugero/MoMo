import unittest
import time
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our actual implementation
from search_comparison import TransactionSearcher, create_sample_transactions


class TestTransactionSearcher(unittest.TestCase):
    """Test cases for our transaction search algorithms - MoMo API Project"""
    
    def setUp(self):
        """Setup test data that matches our MoMo transaction format"""
        print("Setting up test data...")
        self.test_transactions = [
            {'id': 'txn_0001', 'transaction_type': 'received', 'amount': '1500 RWF', 'sender': 'MTN 25078000001'},
            {'id': 'txn_0002', 'transaction_type': 'sent', 'amount': '2500 RWF', 'sender': 'AIRTEL 25073000002'},
            {'id': 'txn_0003', 'transaction_type': 'withdrawal', 'amount': '10000 RWF', 'sender': 'MTN 25078000003'},
        ]
        self.searcher = TransactionSearcher(self.test_transactions)
    
    def test_linear_search_found(self):
        """Test that linear search finds existing transactions"""
        print("Testing linear search...")
        result = self.searcher.linear_search('txn_0002')
        self.assertIsNotNone(result)
        self.assertEqual(result['transaction_type'], 'sent')
        self.assertEqual(result['amount'], '2500 RWF')
    
    def test_linear_search_not_found(self):
        """Test linear search with non-existing transaction"""
        result = self.searcher.linear_search('txn_9999')
        self.assertIsNone(result)
    
    def test_dictionary_lookup_found(self):
        """Test dictionary lookup with existing transaction"""
        print("Testing dictionary lookup...")
        result = self.searcher.dictionary_lookup('txn_0001')
        self.assertIsNotNone(result)
        self.assertEqual(result['id'], 'txn_0001')
    
    def test_dictionary_lookup_not_found(self):
        """Test dictionary lookup with non-existing transaction"""
        result = self.searcher.dictionary_lookup('txn_9999')
        self.assertIsNone(result)
    
    def test_both_methods_return_same_result(self):
        """Verify both search methods return identical results"""
        print("Comparing both search methods...")
        for transaction in self.test_transactions:
            tid = str(transaction['id'])
            linear_result = self.searcher.linear_search(tid)
            dict_result = self.searcher.dictionary_lookup(tid)
            self.assertEqual(linear_result, dict_result, 
                           f"Both methods should return same transaction for ID: {tid}")
    
    def test_dictionary_is_faster(self):
        """Test that dictionary lookup is faster than linear search"""
        print("Testing performance difference...")
        # Create larger dataset for meaningful comparison
        large_transactions = create_sample_transactions(50)
        searcher = TransactionSearcher(large_transactions)
        
        # Search for last element (worst case for linear search)
        target_id = 'txn_0050'
        iterations = 100
        
        # Time linear search
        start = time.perf_counter()
        for _ in range(iterations):
            searcher.linear_search(target_id)
        linear_time = time.perf_counter() - start
        
        # Time dictionary lookup
        start = time.perf_counter()
        for _ in range(iterations):
            searcher.dictionary_lookup(target_id)
        dict_time = time.perf_counter() - start
        
        self.assertLess(dict_time, linear_time, 
                        "Dictionary lookup should be faster than linear search")
        print(f"Dictionary was {linear_time/dict_time:.1f}x faster")
    
    def test_edge_cases(self):
        """Test edge cases in our search implementation"""
        print("Testing edge cases...")
        # Empty list
        empty_searcher = TransactionSearcher([])
        self.assertIsNone(empty_searcher.linear_search('txn_0001'))
        self.assertIsNone(empty_searcher.dictionary_lookup('txn_0001'))
        
        # Single element
        single_searcher = TransactionSearcher([{'id': 'txn_single', 'data': 'test'}])
        self.assertIsNotNone(single_searcher.linear_search('txn_single'))
        self.assertIsNotNone(single_searcher.dictionary_lookup('txn_single'))


class TestPerformanceScaling(unittest.TestCase):
    """Test performance scaling with different dataset sizes"""
    
    def test_linear_search_scales_linearly(self):
        """Verify linear search time increases with dataset size"""
        print("Testing linear search scaling...")
        sizes = [10, 20, 30]
        times = []
        
        for size in sizes:
            transactions = create_sample_transactions(size)
            searcher = TransactionSearcher(transactions)
            
            # Search for last element (worst case)
            start = time.perf_counter()
            for _ in range(50):  # Fewer iterations for quicker tests
                searcher.linear_search(f'txn_{size:04d}')
            times.append(time.perf_counter() - start)
        
        # Verify time increases (rough linear relationship)
        self.assertGreater(times[1], times[0])
        self.assertGreater(times[2], times[1])
        print("Linear search shows linear scaling as expected")
    
    def test_dictionary_lookup_constant_time(self):
        """Verify dictionary lookup time remains relatively constant"""
        print("Testing dictionary constant time...")
        sizes = [10, 30, 50]
        times = []
        
        for size in sizes:
            transactions = create_sample_transactions(size)
            searcher = TransactionSearcher(transactions)
            
            start = time.perf_counter()
            for _ in range(50):
                searcher.dictionary_lookup(f'txn_{size:04d}')
            times.append(time.perf_counter() - start)
        
        # Times should be relatively similar (within 2x)
        max_time = max(times)
        min_time = min(times)
        self.assertLess(max_time / min_time, 2.0)
        print("Dictionary shows constant time performance")


def run_all_tests():
    """Run all tests and generate report for our assignment"""
    print("=" * 80)
    print("DSA UNIT TESTS - MoMo Transaction Search")
    print("Team Data Raiders | Selena - DSA Testing")
    print("=" * 80)
    print("\nRunning test suite...\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestTransactionSearcher))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceScaling))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("All tests passed! Ready for API integration.")
    else:
        print("Some tests failed - please check implementation.")
    
    print("=" * 80)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
