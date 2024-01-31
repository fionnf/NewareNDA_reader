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


def plot_capacity(file_path, theoretical_capacity):
    data = pd.DataFrame(nda.read(file_path))

    grouped = data.groupby('Cycle')
    max_charge = grouped['Charge_Capacity(mAh)'].max()
    max_discharge = grouped['Discharge_Capacity(mAh)'].max()

    coulombic_efficiency = (max_discharge / max_charge) * 100

    fig, ax1 = plt.subplots()

    charge_capacity_scatter = ax1.scatter(max_charge.index, max_charge, label='Charge Capacity', color='blue', s=10)
    discharge_capacity_scatter = ax1.scatter(max_discharge.index, max_discharge, label='Discharge Capacity', color='green', s=10)
    ax1.set_xlabel('Cycle Number')
    ax1.set_ylabel('Capacity (mAh)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_ylim(0, max(max_charge.max(), max_discharge.max()) * 1.1)
    ax1.set_xlim(0, max(max_charge.index.max(), max_discharge.index.max()) * 1.1)

    ax2 = ax1.twinx()
    coulombic_efficiency_scatter = ax2.scatter(max_charge.index, coulombic_efficiency, label='Coulombic Efficiency', color='red', s=10)
    ax2.set_ylabel('Coulombic Efficiency (%)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_ylim(0, 110)
    ax2.set_xlim(0, max(max_charge.index.max(), max_discharge.index.max()) * 1.1)

    if theoretical_capacity is not None:
        theoretical_capacity_line = ax1.axhline(theoretical_capacity, color='orange', linestyle='--', label='Theoretical Capacity')

    # Calculate the time in days for each cycle
    cycle_start_times = grouped['Timestamp'].min()
    first_measurement_time = cycle_start_times.min()
    time_since_start = (cycle_start_times - first_measurement_time).dt.total_seconds() / 86400  # Convert to days

    # Create a second x-axis for time since the start in days per cycle
    ax3 = ax1.twiny()
    ax3.set_xlabel('Time Since Start (days)')
    ax3.scatter(max_charge.index, time_since_start, color='gray', marker='.', s=0.005)  # Reduced marker size
    ax3.xaxis.set_ticks_position('top')  # Move to the top
    ax3.xaxis.set_label_position('top')  # Move to the top
    ax3.set_xlim([0, time_since_start.max()])  # Set x-axis limits

    # Collecting legend handles and labels from both axes
    handles, labels = [], []
    for ax in [ax1, ax2]:
        ax_handles, ax_labels = ax.get_legend_handles_labels()
        handles.extend(ax_handles)
        labels.extend(ax_labels)


    # Creating a single legend with the collected handles and labels
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=4)

    plt.show()



print_ndax_as_csv(r"G:\.shortcut-targets-by-id\1gpf-XKVVvMHbMGqpyQS5Amwp9fh8r96B\RUG shared\Master Project\Experiment files\FF042\FF042batt_a.ndax")
plot_capacity(r"G:\.shortcut-targets-by-id\1gpf-XKVVvMHbMGqpyQS5Amwp9fh8r96B\RUG shared\Master Project\Experiment files\FF042\FF042batt_a.ndax",
              theoretical_capacity=0.8)
