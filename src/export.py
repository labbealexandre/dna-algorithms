import csv

def exportToCSV(file, headers, results):
    n = len(results)

    with open(file, 'w') as file:
        writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_NONE)
        writer.writerow(headers)
        for i in range(n):
            writer.writerow(results[i])