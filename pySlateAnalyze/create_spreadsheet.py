

'''
Remove Citizenship Status. Gender Identity is blank.

https://apply.grad.uci.edu/manage/query/

Sort by Country, and then by UCI Citizenship, then by last name

Query results

How many files has each committee member read?
How many evaluations does each file have?

In the first 

Any scores below 3? 

'''


import pandas as pd

# Load the Excel file

data_path = '/Volumes/Carrot/Dropbox/science/service/MCSB/Admissions/2024Entry/02Committee/'

file_name = 'MCSB_Admissions_Committee 20240111-114854.xlsx'  # Replace with your file path

file_path = data_path + file_name

df = pd.read_excel(file_path)

# Sorting the DataFrame
df.sort_values(by=['Country', 'UCI Citizenship', 'Legal Last'], ascending=[False, True, True], inplace=True)

# Resetting the index after sorting
df.reset_index(drop=True, inplace=True)

# Set the Excel formula for each row in column 'X'
# Assuming data starts from row 2 (including headers) and columns A to W contain potential numeric values
for i in df.index:
    this_row = i + 2  # Excel rows start at 1, and we add 1 more for the header
    df.at[i, 'Number of evaluations'] = f'=SUMPRODUCT(--ISNUMBER(I{this_row}:W{this_row}))'
    df.at[i, 'Numbers > 3.0'] = f'=COUNTIF(A{this_row}:W{this_row}, ">3.0")'
    #df.at[i, 'Numbers > 3.0'] = f'=SUMPRODUCT(--(I{this_row}:W{this_row}>3))'

# Add a new summary row at the bottom
summary_row_index = len(df)
df.loc[summary_row_index, 'Country'] = 'Summary'
df.loc[summary_row_index, 'Number of evaluations'] = f'=COUNTIF(X2:X{summary_row_index}, ">1")'
df.loc[summary_row_index, 'Numbers > 3.0'] = f'=COUNTIF(Y2:Y{summary_row_index}, ">1")'


# Save to a new Excel file
output_file_path = data_path + 'modified_file.xlsx'  # Replace with your desired file path
df.to_excel(output_file_path, index=False)

print("File processed and saved as:", output_file_path)