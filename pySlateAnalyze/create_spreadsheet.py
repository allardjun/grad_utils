

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

input_file_name = 'MCSB_Admissions_Committee 20240114-144314'  # Replace with your file path

file_path = data_path + input_file_name + '.xlsx'

df = pd.read_excel(file_path)

# Sorting the DataFrame
df.sort_values(by=['Country', 'UCI Citizenship', 'Legal Last'], ascending=[False, True, True], inplace=True)

# Resetting the index after sorting
df.reset_index(drop=True, inplace=True)

# Paste in Jun's rubric
source_file_path = data_path + 'from_Juns_rubric.xlsx'  
source_columns = ['Name', 'Jun score']
source_df = pd.read_excel(source_file_path)
extracted_columns = source_df[source_columns]

df = pd.concat([df, extracted_columns], axis=1)


# Set the Excel formula for each row in column 'X'
# Assuming data starts from row 2 (including headers) and columns A to W contain potential numeric values
for i in df.index:
    this_row = i + 2  # Excel rows start at 1, and we add 1 more for the header
    df.at[i, 'Number of evaluations'] = f'=SUMPRODUCT(--ISNUMBER(I{this_row}:Y{this_row}))'
    df.at[i, 'Numbers > 3.0'] = f'=COUNTIF(A{this_row}:Y{this_row}, ">3.0")'
    #df.at[i, 'Numbers > 3.0'] = f'=SUMPRODUCT(--(I{this_row}:W{this_row}>3))'

# Add a new summary row at the bottom
summary_row_index = len(df)
df.loc[summary_row_index, 'Country'] = 'Summary'
df.loc[summary_row_index, 'Number of evaluations'] = f'=COUNTIF(Z2:Z{summary_row_index}, ">1")'
df.loc[summary_row_index, 'Numbers > 3.0'] = f'=COUNTIF(AA2:AA{summary_row_index}, ">1")'


# Save to a new Excel file
# Splitting the string into words
words = input_file_name.split()
# Extracting the last word
last_word = words[-1]
output_file_path = data_path + f'modified_file_{last_word}.xlsx'  # Replace with your desired file path
df.to_excel(output_file_path, index=False)

print("File processed and saved as:", output_file_path)