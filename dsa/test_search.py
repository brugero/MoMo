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
        self.test_transactions = [
            {'id': 1, 'type': 'payment', 'amount': 5000, 'sender': '36521838', 'receiver': 'Internet Provider', 'timestamp': '2024-06-28T14:30:00'},
            {'id': 2, 'type': 'transfer', 'amount': 2500, 'sender': '25078100001', 'receiver': '25078200001', 'timestamp': '2024-06-28T15:45:00'},
            {'id': 3, 'type': 'withdrawal', 'amount': 10000, 'sender': '25078100002', 'receiver': 'ATM_12345', 'timestamp': '2024-06-28T16:20:00'},
        ]
        self.searcher = TransactionSearcher(self.test_transactions)
    
    def test_linear_search_found(self):
        """Test that linear search finds existing transactions"""
        result = self.searcher.linear_search('2')
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['type'], 'transfer')
        self.assertEqual(result[0]['amount'], 2500)
    
    def test_linear_search_not_found(self):
        """Test linear search with non-existing transaction"""
        result = self.searcher.linear_search('999')
        self.assertEqual(len(result), 0)
    
    def test_dictionary_lookup_found(self):
        """Test dictionary lookup with existing transaction"""
        result = self.searcher.dictionary_lookup('1')
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[0]['sender'], '36521838')
    
    def test_dictionary_lookup_not_found(self):
        """Test dictionary lookup with non-existing transaction"""
        result = self.searcher.dictionary_lookup('999')
        self.assertIsNone(result)
    
    def test_both_methods_return_same_result(self):
        """Verify both search methods return identical results for same ID"""
        # Test with ID that exists
        test_id = '1'
        linear_result = self.searcher.linear_search(test_id)
        dict_result = self.searcher.dictionary_lookup(test_id)
        
        self.assertEqual(linear_result, dict_result)
        
        # Test with ID that doesn't exist
        linear_result = self.searcher.linear_search('999')
        dict_result = self.searcher.dictionary_lookup('999')
        self.assertEqual(len(linear_result), 0)
        self.assertIsNone(dict_result)
    
    def test_dictionary_is_faster(self):
        """Test that dictionary lookup is faster than linear search"""
        # Create larger dataset for meaningful comparison
        large_transactions = create_sample_transactions(50)
        searcher = TransactionSearcher(large_transactions)
        
        # Search for last element (worst case for linear search)
        target_id = '50'
        iterations = 100
        
        # Time linear search
        start = time.perf_counter()
        for _ in range(iterations):
            searcher.linear_search(target_id, verbose=False)
        linear_time = time.perf_counter() - start
        
        # Time dictionary lookup
        start = time.perf_counter()
        for _ in range(iterations):
            searcher.dictionary_lookup(target_id, verbose=False)
        dict_time = time.perf_counter() - start
        
        self.assertLess(dict_time, linear_time, 
                        "Dictionary lookup should be faster than linear search")
    
    def test_edge_cases(self):
        """Test edge cases in our search implementation"""
        # Empty list
        empty_searcher = TransactionSearcher([])
        self.assertEqual(len(empty_searcher.linear_search('1')), 0)
        self.assertIsNone(empty_searcher.dictionary_lookup('1'))
        
        # Test handling of string vs integer IDs
        result_str = self.searcher.linear_search('1')
        result_int = self.searcher.linear_search(1)
        self.assertEqual(result_str, result_int)


class TestPerformanceScaling(unittest.TestCase):
    """Test performance scaling with different dataset sizes"""
    
    def test_linear_search_scales_linearly(self):
        """Verify linear search time increases with dataset size"""
        sizes = [10, 20, 30]
        times = []
        
        for size in sizes:
            transactions = create_sample_transactions(size)
            searcher = TransactionSearcher(transactions)
            
            # Search for last element (worst case)
            start = time.perf_counter()
            for _ in range(50):  # Fewer iterations for quicker tests
                searcher.linear_search(str(size), verbose=False)
            times.append(time.perf_counter() - start)
        
        # Verify time increases (rough linear relationship)
        self.assertGreater(times[1], times[0])
        self.assertGreater(times[2], times[1])
    
    def test_dictionary_lookup_constant_time(self):
        """Verify dictionary lookup time remains relatively constant"""
        sizes = [10, 30, 50]
        times = []
        
        for size in sizes:
            transactions = create_sample_transactions(size)
            searcher = TransactionSearcher(transactions)
            
            start = time.perf_counter()
            for _ in range(50):
                searcher.dictionary_lookup(str(size), verbose=False)
            times.append(time.perf_counter() - start)
        
        # Times should be relatively similar (within reasonable bounds)
        max_time = max(times)
        min_time = min(times)
        # Allow for some variance but should be much more consistent than linear search
        self.assertLess(max_time / min_time, 3.0)


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
        print("\n🎉 All tests passed! Ready for API integration.")
    else:
        print("\n❌ Some tests failed - please check implementation.")
    
    print("=" * 80)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
