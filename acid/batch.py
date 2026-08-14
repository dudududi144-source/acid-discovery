"""
ACID Batch System
Run multiple discovery tasks in sequence or parallel.
"""
import time
import json
import os

from acid.client import ACIDClient


class BatchRunner:
    """Run multiple tasks in batch."""
    
    def __init__(self, client=None):
        self.client = client or ACIDClient()
        self.results = []
    
    def run_tasks(self, tasks, delay=1.0):
        """Run a list of tasks sequentially."""
        for i, task in enumerate(tasks):
            print(f"Running task {i+1}/{len(tasks)}: {task.get('name', 'unknown')}")
            
            result = self.client.solve(
                problem=task.get("problem", ""),
                inputs=task.get("inputs"),
                expected=task.get("expected")
            )
            
            self.results.append({
                "task": task,
                "result": result,
                "timestamp": time.time()
            })
            
            if delay > 0 and i < len(tasks) - 1:
                time.sleep(delay)
        
        return self.results
    
    def run_task_library(self, max_difficulty=None, category=None):
        """Run tasks from the task library."""
        from acid.task_library import TASKS
        
        tasks = []
        for name, task_def in TASKS.items():
            if max_difficulty and task_def["difficulty"] > max_difficulty:
                continue
            if category and task_def["category"] != category:
                continue
            
            tasks.append({
                "name": name,
                "problem": task_def["description"],
                "inputs": task_def["inputs"],
                "expected": task_def["expected"]
            })
        
        return self.run_tasks(tasks)
    
    def get_summary(self):
        """Get summary of batch results."""
        total = len(self.results)
        solved = sum(1 for r in self.results if r["result"].get("status") == "solved")
        failed = sum(1 for r in self.results if r["result"].get("status") in ["not_found", "verification_failed"])
        
        return {
            "total": total,
            "solved": solved,
            "failed": failed,
            "success_rate": solved / total if total > 0 else 0,
            "results": self.results
        }
    
    def save_results(self, filename="output/batch_results.json"):
        """Save results to file."""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            json.dump(self.get_summary(), f, indent=2)
        return filename


class ParallelRunner:
    """Run tasks in parallel (requires concurrent.futures)."""
    
    def __init__(self, max_workers=5):
        self.max_workers = max_workers
        self.results = []
    
    def run_tasks(self, tasks):
        """Run tasks in parallel."""
        try:
            from concurrent.futures import ThreadPoolExecutor, as_completed
        except ImportError:
            print("concurrent.futures not available, falling back to sequential")
            runner = BatchRunner()
            return runner.run_tasks(tasks, delay=0)
        
        def run_one(task):
            client = ACIDClient()
            result = client.solve(
                problem=task.get("problem", ""),
                inputs=task.get("inputs"),
                expected=task.get("expected")
            )
            return {"task": task, "result": result, "timestamp": time.time()}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(run_one, task): task for task in tasks}
            for future in as_completed(futures):
                result = future.result()
                self.results.append(result)
                print(f"Completed: {result['task'].get('name', 'unknown')}")
        
        return self.results
    
    def get_summary(self):
        """Get summary of results."""
        total = len(self.results)
        solved = sum(1 for r in self.results if r["result"].get("status") == "solved")
        
        return {
            "total": total,
            "solved": solved,
            "success_rate": solved / total if total > 0 else 0
        }
