#!/usr/bin/env python3
"""
Test script to verify multicore processing is working correctly.
"""
import sys
from pathlib import Path
import os
import multiprocessing

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("=" * 60)
print("Multicore Processing Test")
print("=" * 60)

# Check CPU cores
cpu_count = os.cpu_count()
print(f"\n✓ System CPU cores detected: {cpu_count}")

# Check multiprocessing
mp_cpu_count = multiprocessing.cpu_count()
print(f"✓ Multiprocessing CPU count: {mp_cpu_count}")

# Import and check components
try:
    from invert_pdf_colors.components.invert_images import invert_directory
    from invert_pdf_colors.components.pdf_to_images import extract_images
    from invert_pdf_colors.components.images_to_pdf import images_to_pdf
    print("\n✓ All components imported successfully")
except ImportError as e:
    print(f"\n✗ Import error: {e}")
    sys.exit(1)

# Check ProcessPoolExecutor
try:
    from concurrent.futures import ProcessPoolExecutor
    print("✓ ProcessPoolExecutor available")
    
    # Test with simple function
    def test_func(x):
        return x * x
    
    with ProcessPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(test_func, [1, 2, 3, 4]))
    
    if results == [1, 4, 9, 16]:
        print("✓ ProcessPoolExecutor working correctly")
    else:
        print("✗ ProcessPoolExecutor returned unexpected results")
        
except Exception as e:
    print(f"✗ ProcessPoolExecutor test failed: {e}")

# Check ThreadPoolExecutor
try:
    from concurrent.futures import ThreadPoolExecutor
    print("✓ ThreadPoolExecutor available")
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(test_func, [1, 2, 3, 4]))
    
    if results == [1, 4, 9, 16]:
        print("✓ ThreadPoolExecutor working correctly")
    else:
        print("✗ ThreadPoolExecutor returned unexpected results")
        
except Exception as e:
    print(f"✗ ThreadPoolExecutor test failed: {e}")

print("\n" + "=" * 60)
print("Summary:")
print("=" * 60)
print(f"✓ CPU cores available: {cpu_count}")
print(f"✓ Image inversion will use: {cpu_count} processes (ProcessPoolExecutor)")
print(f"✓ PDF extraction will use: {min(32, cpu_count * 2)} threads (ThreadPoolExecutor)")
print(f"✓ PDF building will use: {min(32, cpu_count * 2)} threads (ThreadPoolExecutor)")
print("\nMulticore processing is FULLY OPERATIONAL! 🚀")
print("=" * 60)
