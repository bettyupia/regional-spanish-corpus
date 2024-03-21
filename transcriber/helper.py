import csv
import os
def read_csv(path):
    with open(path, 'r') as file:
        csv_reader = csv.DictReader(file)
        return [row for row in csv_reader]
    
def write_csv(path, objs, fieldnames=None):
    if len(objs) > 0:
        if os.path.exists(path):
            os.remove(path)
        
        with open(path, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=set().union(*[obj.keys() for obj in objs]) if not fieldnames else fieldnames)
            writer.writeheader()
            writer.writerows(objs)