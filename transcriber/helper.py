import csv

def read_csv(path):
    with open(path, 'r') as file:
        csv_reader = csv.DictReader(file)
        return [row for row in csv_reader]
    
def write_csv(path, obj):
    with open(path, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=obj.keys())
        writer.writeheader()
        writer.writerows(obj)