"""
ACID Utilities
Common utility functions.
"""
import hashlib
import json
import time
import random


def compute_hash(data, algorithm="sha256"):
    """Compute hash of data."""
    if isinstance(data, dict) or isinstance(data, list):
        data = json.dumps(data, sort_keys=True)
    if isinstance(data, str):
        data = data.encode()
    
    if algorithm == "sha256":
        return hashlib.sha256(data).hexdigest()
    elif algorithm == "md5":
        return hashlib.md5(data).hexdigest()
    elif algorithm == "short":
        return hashlib.sha256(data).hexdigest()[:12]
    return hashlib.sha256(data).hexdigest()


def format_duration(seconds):
    """Format seconds as human-readable duration."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.0f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def format_number(n):
    """Format number with thousands separators."""
    if n >= 1000000:
        return f"{n/1000000:.1f}M"
    elif n >= 1000:
        return f"{n/1000:.1f}K"
    return str(n)


def truncate(text, max_length=50):
    """Truncate text to max length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def retry(fn, max_retries=3, delay=1.0, backoff=2.0):
    """Retry a function with exponential backoff."""
    last_error = None
    
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= backoff
    
    raise last_error


def chunk_list(lst, chunk_size):
    """Split a list into chunks."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def deep_merge(base, override):
    """Deep merge two dicts."""
    result = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def seeded_random(seed):
    """Create a seeded random generator."""
    rng = random.Random(seed)
    return rng


def timer():
    """Context manager for timing."""
    class Timer:
        def __enter__(self):
            self.start = time.time()
            return self
        
        def __exit__(self, *args):
            self.elapsed = time.time() - self.start
    
    return Timer()


def memoize(fn):
    """Simple memoization decorator."""
    cache = {}
    
    def wrapper(*args):
        key = str(args)
        if key not in cache:
            cache[key] = fn(*args)
        return cache[key]
    
    return wrapper


def validate_inputs(inputs, expected_length=None):
    """Validate input list."""
    if not isinstance(inputs, list):
        return False, "inputs must be a list"
    
    if expected_length is not None and len(inputs) != expected_length:
        return False, f"expected {expected_length} inputs, got {len(inputs)}"
    
    for i, val in enumerate(inputs):
        if not isinstance(val, (int, float)):
            return False, f"input {i} must be a number"
    
    return True, "valid"


def sanitize_program(instructions, max_length=200):
    """Sanitize program instructions."""
    valid_ops = {"PUSH", "POP", "DUP", "SWAP", "ADD", "SUB", "MUL", "MOD",
                 "GT", "LT", "EQ", "AND", "OR", "NOT", "JZ", "READ", "WRITE", "HALT"}
    
    sanitized = []
    for instr in instructions[:max_length]:
        if isinstance(instr, (list, tuple)) and len(instr) == 2:
            op, arg = instr
            if op in valid_ops and isinstance(arg, int):
                sanitized.append([op, arg])
    
    return sanitized
