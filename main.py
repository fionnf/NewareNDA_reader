import NewareNDA as nda
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator

def print_ndax_as_csv(file_path):
    data = nda.read(file_path)
    df = pd.DataFrame(data)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_csv_path = os.path.join(os.path.dirname(file_path), base_name + '.csv')
    df.to_csv(output_csv_path, index=False)
    print(f'Data printed to CSV file: {output_csv_path}')
    newaredata = df


def plot_capacity(file_path, theoretical_capacity=None):
    data = pd.DataFrame(nda.read(file_path))

    grouped = data.groupby('Cycle')
    max_charge = grouped['Charge_Capacity(mAh)'].max()
    max_discharge = grouped['Discharge_Capacity(mAh)'].max()

    coulombic_efficiency = (max_discharge / max_charge) * 100

    fig, ax1 = plt.subplots(figsize=(10, 8))

    ax1.scatter(max_charge.index, max_charge, label='Charge Capacity', color='blue', s=10)
    ax1.scatter(max_discharge.index, max_discharge, label='Discharge Capacity', color='green', s=10)
    ax1.set_xlabel('Cycle Number')
    ax1.set_ylabel('Capacity (mAh)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_ylim(0, max(max_charge.max(), max_discharge.max()) * 1.1)
    ax1.set_xlim(0, max(max_charge.index.max(), max_discharge.index.max()) * 1.1)

    ax2 = ax1.twinx()
    ax2.scatter(max_charge.index, coulombic_efficiency, label='Coulombic Efficiency', color='red', s=10)
    ax2.set_ylabel('Coulombic Efficiency (%)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_ylim(0, 110)
    ax2.set_xlim(0, max(max_charge.index.max(), max_discharge.index.max()) * 1.1)

    if theoretical_capacity is not None:
        ax1.axhline(theoretical_capacity, color='orange', linestyle='--', label='Theoretical Capacity')

    # Use legend method of ax1 to create the legend
    ax1.legend(loc='upper right')

    plt.tight_layout()
    plt.show()


print_ndax_as_csv(r"G:\.shortcut-targets-by-id\1gpf-XKVVvMHbMGqpyQS5Amwp9fh8r96B\RUG shared\Master Project\Experiment files\FF042\FF042batt_a.ndax")
plot_capacity(r"G:\.shortcut-targets-by-id\1gpf-XKVVvMHbMGqpyQS5Amwp9fh8r96B\RUG shared\Master Project\Experiment files\FF042\FF042batt_a.ndax",
              theoretical_capacity=0.8)
