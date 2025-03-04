import pandas as pd
import os
from openpyxl import Workbook

def csv_to_xlsx(input_dir='.', output_file='combined.xlsx'):
    """
    Combine all CSV files in a directory into a single Excel workbook with separate sheets
    """
    # Get list of CSV files
    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print("No CSV files found in the directory!")
        return

    # Create Excel writer object
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for csv_file in csv_files:
            # Read CSV file
            csv_path = os.path.join(input_dir, csv_file)
            df = pd.read_csv(csv_path)
            
            # Clean sheet name (Excel sheet name restrictions)
            sheet_name = os.path.splitext(csv_file)[0]
            sheet_name = sheet_name.split("_")[2]
            # Remove invalid characters
            invalid_chars = ['[', ']', ':', '*', '?', '/', '\\']
            for char in invalid_chars:
                sheet_name = sheet_name.replace(char, '')
            # Truncate to 31 characters (Excel limit)
            sheet_name = sheet_name[:31]
            
            # Write to Excel
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"Added: {csv_file} -> Sheet: {sheet_name}")

    print(f"\nSuccessfully created {output_file} with {len(csv_files)} sheets!")

csv_to_xlsx(input_dir='.', output_file='exchange_rates.xlsx')
