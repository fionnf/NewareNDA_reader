import NewareNDA as nda

def print_ndax_as_csv(file_path):
    data = nda.read(file_path)
    print(data.to_csv())

print_ndax_as_csv(r"G:\.shortcut-targets-by-id\1gpf-XKVVvMHbMGqpyQS5Amwp9fh8r96B\RUG shared\Master Project\Experiment files\FF041\FF041Batt_b.ndax")
