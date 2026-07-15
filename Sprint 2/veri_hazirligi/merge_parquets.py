import os
import glob
import time
import sys

def merge_parquet_files():
    print("=== Volti Parquet Dataset Merger ===")
    
    # 1. Search for parquet files in dataset/ directory
    input_pattern = "dataset/block_*.parquet"
    output_path = "dataset/combined_data.parquet"
    
    files = sorted(glob.glob(input_pattern))
    
    if not files:
        print(f"[!] Error: No files found matching pattern: {input_pattern}")
        print("    Make sure your parquet files are located in the 'dataset/' folder.")
        sys.exit(1)
        
    print(f"[*] Found {len(files)} files to merge:")
    for f in files:
        size_mb = os.path.getsize(f) / (1024 * 1024)
        print(f"    - {os.path.basename(f)} ({size_mb:.2f} MB)")
        
    # 2. High-performance PyArrow concatenation
    # PyArrow is extremely fast and memory-efficient for binary files compared to Pandas
    try:
        import pyarrow.parquet as pq
        import pyarrow as pa
        
        t0 = time.time()
        print("\n[*] Reading and concatenating Parquet tables using PyArrow...")
        
        # Read all files into memory as PyArrow Tables
        tables = [pq.read_table(f) for f in files]
        
        # Concatenate tables in memory without duplicate copying
        combined_table = pa.concat_tables(tables)
        
        print(f"[*] Combined Table Stats:")
        print(f"    - Total Rows: {combined_table.num_rows:,}")
        print(f"    - Total Columns: {combined_table.num_columns}")
        
        # Write out to a single Snappy-compressed Parquet file
        print(f"[*] Writing combined parquet to: {output_path}...")
        pq.write_table(combined_table, output_path, compression="snappy")
        
        elapsed = time.time() - t0
        output_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        
        print("==========================================")
        print(f"[OK] Successfully combined into {output_path} ({output_size_mb:.2f} MB) in {elapsed:.2f}s!")
        
    except ImportError:
        # Fallback to Pandas if PyArrow is not installed (though pyarrow is standard)
        print("\n[!] PyArrow not detected, falling back to Pandas...")
        try:
            import pandas as pd
            t0 = time.time()
            
            # Read and concatenate using Pandas
            dfs = [pd.read_parquet(f) for f in files]
            combined_df = pd.concat(dfs, ignore_index=True)
            
            print(f"[*] Combined DataFrame Stats:")
            print(f"    - Total Rows: {len(combined_df):,}")
            
            # Export
            combined_df.to_parquet(output_path, index=False, compression="snappy")
            
            elapsed = time.time() - t0
            output_size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print("==========================================")
            print(f"[OK] Successfully combined (via Pandas) in {elapsed:.2f}s! Size: {output_size_mb:.2f} MB")
            
        except Exception as e:
            print(f"[!] Error during Pandas merge: {e}")
            sys.exit(1)
            
    except Exception as e:
        print(f"[!] Error during PyArrow merge: {e}")
        sys.exit(1)

if __name__ == "__main__":
    merge_parquet_files()
