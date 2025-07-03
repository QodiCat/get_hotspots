

def read_csv(file_path):
    """
    Reads a CSV file and returns its content as a list of dictionaries.
    
    :param file_path: Path to the CSV file.
    :return: List of dictionaries representing the rows in the CSV file.
    """
    import csv
    
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]
    #依次返回每一列
def read_csv_columns(file_path):
    """ Reads a CSV file and returns its content as a list of lists, where each inner list represents a column.
    :param file_path: Path to the CSV file.
    :return: List of lists representing the columns in the CSV file.    
    """
    import csv
    
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        columns = list(zip(*reader))  # Transpose rows to columns
        return [list(column) for column in columns]