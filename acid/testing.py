"""
ACID Test Framework
Comprehensive testing for all system components.
"""
import time
import json

class TestResult:
    def __init__(self, name, passed, message="", duration=0):
        self.name = name
        self.passed = passed
        self.message = message
        self.duration = duration
    
    def to_dict(self):
        return {
            "name": self.name,
            "passed": self.passed,
            "message": self.message,
            "duration": self.duration
        }


class TestSuite:
    def __init__(self, name):
        self.name = name
        self.tests = []
        self.results = []
    
    def add_test(self, name, test_fn):
        """Add a test to the suite."""
        self.tests.append((name, test_fn))
    
    def run(self):
        """Run all tests."""
        self.results = []
        
        for name, test_fn in self.tests:
            start = time.time()
            try:
                test_fn()
                duration = time.time() - start
                self.results.append(TestResult(name, True, "PASSED", duration))
            except AssertionError as e:
                duration = time.time() - start
                self.results.append(TestResult(name, False, str(e), duration))
            except Exception as e:
                duration = time.time() - start
                self.results.append(TestResult(name, False, f"ERROR: {str(e)}", duration))
        
        return self.results
    
    def summary(self):
        """Get test summary."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        return {
            "suite": self.name,
            "total": total,
            "passed": passed,
            "failed": failed,
            "success_rate": passed / total if total > 0 else 0,
            "results": [r.to_dict() for r in self.results]
        }


def build_substrate_tests():
    """Build substrate test suite."""
    from acid.substrate import Program, Executor, validate_substrate
    
    suite = TestSuite("Substrate")
    
    def test_validation():
        results = validate_substrate()
        assert all(r.get("pass", False) for r in results.values()), "Substrate validation failed"
    
    def test_sum():
        ex = Executor()
        prog = Program([("READ",0),("READ",1),("ADD",0),("WRITE",2),("HALT",0)], [0]*10)
        result = ex.execute(prog, inputs=[2, 3])
        assert result["outputs"] == [5], f"Expected [5], got {result['outputs']}"
    
    def test_determinism():
        ex = Executor()
        prog = Program([("READ",0),("READ",1),("ADD",0),("WRITE",2),("HALT",0)], [0]*10)
        r1 = ex.execute(prog, inputs=[2, 3])
        r2 = ex.execute(prog, inputs=[2, 3])
        assert r1["outputs"] == r2["outputs"], "Non-deterministic execution"
    
    def test_bounded():
        ex = Executor(max_steps=100)
        prog = Program([("JZ", 0), ("HALT", 0)], [0])
        result = ex.execute(prog, inputs=[0])
        assert result["steps"] <= 100, "Exceeded step limit"
    
    suite.add_test("validation", test_validation)
    suite.add_test("sum", test_sum)
    suite.add_test("determinism", test_determinism)
    suite.add_test("bounded", test_bounded)
    
    return suite


def build_verifier_tests():
    """Build verifier test suite."""
    from acid.substrate import Program, Executor
    
    suite = TestSuite("Verifier")
    ex = Executor()
    
    def test_functional():
        prog = Program([("READ",0),("READ",1),("ADD",0),("WRITE",2),("HALT",0)], [0]*10)
        result = ex.execute(prog, inputs=[2, 3])
        assert result["outputs"] == [5], "Functional test failed"
    
    def test_false_positive():
        prog = Program([("PUSH",0),("WRITE",1),("HALT",0)], [5])
        r1 = ex.execute(prog, inputs=[2, 3])
        r2 = ex.execute(prog, inputs=[10, 20])
        assert r1["outputs"] == r2["outputs"] == [5], "Should output constant 5"
    
    suite.add_test("functional", test_functional)
    suite.add_test("false_positive", test_false_positive)
    
    return suite


def run_all_tests():
    """Run all test suites."""
    suites = [
        build_substrate_tests(),
        build_verifier_tests()
    ]
    
    all_results = []
    for suite in suites:
        suite.run()
        summary = suite.summary()
        all_results.append(summary)
        print(f"  {summary['suite']}: {summary['passed']}/{summary['total']} passed")
    
    total_passed = sum(s["passed"] for s in all_results)
    total_tests = sum(s["total"] for s in all_results)
    
    print(f"\n  Total: {total_passed}/{total_tests} passed")
    
    return all_results
