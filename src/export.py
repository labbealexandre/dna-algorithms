import csv

def exportToCSV(file, headers, results):
    n = len(results)

    with open(file, 'wb') as file:
        writer = csv.writer(file, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        for i in range(n):
            writer.writerow(results[i])