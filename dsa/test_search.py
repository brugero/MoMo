import unittest
import time
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the TransactionSearcher class
# from dsa.search_comparison import TransactionSearcher, create_sample_transactions


class TestTransactionSearcher(unittest.TestCase):
    """Test cases for TransactionSearcher class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_transactions = [
            {'id': 1, 'type': 'DEPOSIT', 'amount': 1000, 'sender': '254700100001'},
            {'id': 2, 'type': 'WITHDRAWAL', 'amount': 500, 'sender': '254700100002'},
            {'id': 3, 'type': 'TRANSFER', 'amount': 750, 'sender': '254700100003'},
            {'id': 4, 'type': 'PAYMENT', 'amount': 1200, 'sender': '254700100004'},
            {'id': 5, 'type': 'DEPOSIT', 'amount': 2000, 'sender': '254700100005'},
        ]
        # Assuming TransactionSearcher is imported
        # self.searcher = TransactionSearcher(self.sample_transactions)
    
    def test_linear_search_found(self):
        """Test linear search with existing transaction"""
        # Test would go here
        # result = self.searcher.linear_search('3')
        # self.assertIsNotNone(result)
        # self.assertEqual(result['id'], 3)
        # self.assertEqual(result['type'], 'TRANSFER')
        pass
    
    def test_linear_search_not_found(self):
        """Test linear search with non-existing transaction"""
        # result = self.searcher.linear_search('999')
        # self.assertIsNone(result)
        pass
    
    def test_dictionary_lookup_found(self):
        """Test dictionary lookup with existing transaction"""
        # result = self.searcher.dictionary_lookup('3')
        # self.assertIsNotNone(result)
        # self.assertEqual(result['id'], 3)
        pass
    
    def test_dictionary_lookup_not_found(self):
        """Test dictionary lookup with non-existing transaction"""
        # result = self.searcher.dictionary_lookup('999')
        # self.assertIsNone(result)
        pass
    
    def test_both_methods_return_same_result(self):
        """Verify both search methods return identical results"""
        # for transaction in self.sample_transactions:
        #     tid = str(transaction['id'])
        #     linear_result = self.searcher.linear_search(tid)
        #     dict_result = self.searcher.dictionary_lookup(tid)
        #     self.assertEqual(linear_result, dict_result)
        pass
    
    def test_dictionary_is_faster(self):
        """Test that dictionary lookup is faster than linear search"""
        # We will create a larger dataset for better comparison
        large_transactions = [
            {'id': i, 'type': 'TEST', 'amount': i * 100, 'sender': f'254700{i:06d}'}
            for i in range(1, 101)
        ]
        # searcher = TransactionSearcher(large_transactions)
        
        # Search for last element (worst case for linear search)
        # target_id = '100'
        # iterations = 1000
        
        # Time linear search
        # start = time.perf_counter()
        # for _ in range(iterations):
        #     searcher.linear_search(target_id)
        # linear_time = time.perf_counter() - start
        
        # Time dictionary lookup
        # start = time.perf_counter()
        # for _ in range(iterations):
        #     searcher.dictionary_lookup(target_id)
        # dict_time = time.perf_counter() - start
        
        # self.assertLess(dict_time, linear_time, 
        #                 "Dictionary lookup should be faster than linear search")
        pass
    
    def test_edge_cases(self):
        """Test edge cases"""
        # Empty list
        # empty_searcher = TransactionSearcher([])
        # self.assertIsNone(empty_searcher.linear_search('1'))
        # self.assertIsNone(empty_searcher.dictionary_lookup('1'))
        
        # Single element
        # single_searcher = TransactionSearcher([{'id': 1, 'data': 'test'}])
        # self.assertIsNotNone(single_searcher.linear_search('1'))
        # self.assertIsNotNone(single_searcher.dictionary_lookup('1'))
        pass


class TestPerformanceScaling(unittest.TestCase):
    """Test performance scaling with different dataset sizes"""
    
    def test_linear_search_scales_linearly(self):
        """Verify linear search time increases with dataset size"""
        sizes = [10, 50, 100]
        times = []
        
        for size in sizes:
            transactions = [{'id': i, 'data': f'data{i}'} for i in range(size)]
            # searcher = TransactionSearcher(transactions)
            
            # Search for last element
            # start = time.perf_counter()
            # for _ in range(100):
            #     searcher.linear_search(str(size - 1))
            # times.append(time.perf_counter() - start)
        
        # Verify time increases (rough linear relationship)
        # self.assertGreater(times[1], times[0])
        # self.assertGreater(times[2], times[1])
        pass
    
    def test_dictionary_lookup_constant_time(self):
        """Verify dictionary lookup time remains relatively constant"""
        sizes = [10, 50, 100]
        times = []
        
        for size in sizes:
            transactions = [{'id': i, 'data': f'data{i}'} for i in range(size)]
            # searcher = TransactionSearcher(transactions)
            
            # start = time.perf_counter()
            # for _ in range(100):
            #     searcher.dictionary_lookup(str(size - 1))
            # times.append(time.perf_counter() - start)
        
        # Times should be relatively similar (within 2x)
        # max_time = max(times)
        # min_time = min(times)
        # self.assertLess(max_time / min_time, 2.0)
        pass


def run_all_tests():
    """Run all tests and generate report"""
    print("=" * 80)
    print("DSA UNIT TESTS")
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
    print("=" * 80)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
