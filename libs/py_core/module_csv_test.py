import csv
import unittest


class TestCsv(unittest.TestCase):
    def test_read(self):
        with open("data/data.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)

    def test_sniffer(self):
        with open("data/data.csv") as f:
            dialect = csv.Sniffer().sniff(f.read(1024))
            f.seek(0)
            has_header = csv.Sniffer().has_header(f.read(1024))
            f.seek(0)

            print('has_header:', has_header)
            print('dialect::delimiter', dialect.delimiter)
            print('dialect::escapechar', dialect.escapechar)
            print('dialect::quotechar', dialect.quotechar)

    def test_write(self):
        with open("tmp/data.csv", mode="w") as f:
            writer = csv.writer(f)
            writer.writerow(["Type", "Country", "Profit"])
            writer.writerow(["Meat", "Indonesia", "600.00"])

    if __name__ == '__main__':
        unittest.main()
