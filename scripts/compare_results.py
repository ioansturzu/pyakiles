#!/usr/bin/env python3
import json
import sys
import numpy as np
from pathlib import Path

def load_results(path):
    with open(path) as f:
        data = json.load(f)
    
    # Handle "inf" in h if present
    h = data["h"]
    if isinstance(h[-1], str) and h[-1] == "inf":
        h[-1] = float("inf")
    # MATLAB might have encoded inf as null or large number, handle if needed
    
    return {k: np.array(v, dtype=float) for k, v in data.items()}

def compare(py_path, ml_path, tolerance=1e-3):
    print(f"Comparing {py_path} vs {ml_path}")
    py_data = load_results(py_path)
    ml_data = load_results(ml_path)
    
    failed = False
    for key in ["h", "phi", "ne", "ni"]:
        if key not in py_data or key not in ml_data:
            print(f"Missing key {key}")
            failed = True
            continue
            
        py_arr = py_data[key]
        ml_arr = ml_data[key]
        
        # Check shapes
        if py_arr.shape != ml_arr.shape:
            print(f"Shape mismatch for {key}: {py_arr.shape} vs {ml_arr.shape}")
            failed = True
            continue
            
        # Handle inf in comparison (skip or mask)
        mask = np.isfinite(py_arr) & np.isfinite(ml_arr)
        
        if not np.allclose(py_arr[mask], ml_arr[mask], rtol=tolerance, atol=tolerance):
            diff = np.abs(py_arr[mask] - ml_arr[mask])
            max_diff = np.max(diff)
            print(f"FAIL: {key} mismatch. Max diff: {max_diff}")
            failed = True
        else:
            print(f"PASS: {key}")
            
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
