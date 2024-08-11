import pandas as pd

# Example usage
file_path = "C:\\Users\\Dharmaraj\\Favorites\\Downloads\\SaleData.xlsx"
sheet_name = 'SaleData'
filter_column = 'Unit_price'
filter_condition = lambda x: x < 500
new_column_name = 'High Sales'
new_column_value = 'Moderate Sale'


def add_column_based_on_filter(file_path, sheet_name, filter_column, filter_condition, new_column_name, new_column_value):
  """
  Adds a new column to an Excel file based on a filter condition.

  Args:
    file_path: Path to the Excel file.
    sheet_name: Name of the sheet.
    filter_column: Column to apply the filter condition on.
    filter_condition: Condition to filter the data.
    new_column_name: Name of the new column.
    new_column_value: Value to assign to the new column based on the filter.
  """

  df = pd.read_excel(file_path, sheet_name=sheet_name)

  # Create a new column with default value
  df[new_column_name] = new_column_value

  # Apply the filter condition and assign the specified value
  df.loc[df[filter_column].apply(filter_condition), new_column_name] = new_column_value

  df.to_excel(file_path, sheet_name=sheet_name, index=False)

  print(df)





add_column_based_on_filter(file_path, sheet_name, filter_column, filter_condition, new_column_name, new_column_value)