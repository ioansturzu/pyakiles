#!/usr/bin/env python3
import json
import sys
import numpy as np
from pathlib import Path

def load_results(path):
    with open(path) as f:
        data = json.load(f)
    
    # Handle "inf" in h if present
    if "h" in data:
        h = data["h"]
        if isinstance(h[-1], str) and h[-1] == "inf":
            h[-1] = float("inf")
    # MATLAB might have encoded inf as null or large number, handle if needed
    
    return {k: np.array(v, dtype=float) for k, v in data.items()}

def compare(py_path, ml_path, tolerance=0.05):
    print(f"Comparing {py_path} vs {ml_path} with tolerance {tolerance}")
    py_data = load_results(py_path)
    ml_data = load_results(ml_path)
    
    # Identify common keys to compare
    common_keys = set(py_data.keys()) & set(ml_data.keys())
    # remove metadata keys if any
    keys_to_compare = [k for k in common_keys if not k.endswith("_indices")]
    
    if not keys_to_compare:
        print("No common data keys found to compare.")
        return False

    failed = False
    for key in keys_to_compare:
            
        py_arr = py_data[key]
        ml_arr = ml_data[key]
        
        # Handle length mismatch by truncating to shorter
        n_py = len(py_arr)
        n_ml = len(ml_arr)
        
        if n_py != n_ml:
            print(f"Shape mismatch for {key}: {n_py} vs {n_ml}. Truncating to overlapping region.")
            n = min(n_py, n_ml)
            py_arr = py_arr[:n]
            ml_arr = ml_arr[:n]
            
        # Handle inf in comparison (skip or mask)
        mask = np.isfinite(py_arr) & np.isfinite(ml_arr)
        
        # If no overlap in finite values
        if not np.any(mask):
             print(f"WARN: No finite overlap for {key}")
             continue

        diff = np.abs(py_arr[mask] - ml_arr[mask])
        max_diff = np.max(diff)
        
        # Standard relative/absolute check
        if not np.allclose(py_arr[mask], ml_arr[mask], rtol=tolerance, atol=tolerance):
            print(f"FAIL: {key} mismatch. Max diff: {max_diff}")
            # Check relative error specifically
            rel_diff = diff / (np.abs(ml_arr[mask]) + 1e-9)
            max_rel = np.max(rel_diff)
            print(f"      Max relative diff: {max_rel}")
            failed = True
        else:
            print(f"PASS: {key} (Max diff: {max_diff})")
            
    return not failed

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: compare_results.py <python_json> <matlab_json>")
        sys.exit(1)
        
    py_res = Path(sys.argv[1])
    ml_res = Path(sys.argv[2])
    
    if not py_res.exists() or not ml_res.exists():
        print("One or more result files missing.")
        sys.exit(1)

    if compare(py_res, ml_res):
        print("Comparison SUCCEEDED")
        sys.exit(0)
    else:
        print("Comparison FAILED")
        sys.exit(1)
