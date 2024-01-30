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
    """
    Plots the charge and discharge capacities, Coulombic Efficiency, theoretical capacity, and time since the start of the experiment for each cycle.

    Parameters:
    file_path (str): Path to the data file.
    theoretical_capacity (float or None): Theoretical capacity value to plot as a horizontal line. Default is None.
    """

    data = pd.DataFrame(nda.read(file_path))

    # Group by Cycle and get maximum capacity for charge and discharge
    grouped = data.groupby('Cycle')
    max_charge = grouped['Charge_Capacity(mAh)'].max()
    max_discharge = grouped['Discharge_Capacity(mAh)'].max()

    # Calculate Coulombic Efficiency
    coulombic_efficiency = (max_discharge / max_charge) * 100

    # Plotting
    fig, ax1 = plt.subplots()

    ax1.scatter(max_charge.index, max_charge, label='Max Charge Capacity', color='blue', s=10)
    ax1.scatter(max_discharge.index, max_discharge, label='Max Discharge Capacity', color='green', s=10)
    ax1.set_xlabel('Cycle Number')
    ax1.set_ylabel('Capacity (mAh)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_ylim(0, 1)

    # Create a second y-axis for Coulombic Efficiency
    ax2 = ax1.twinx()
    ax2.scatter(max_charge.index, coulombic_efficiency, label='Coulombic Efficiency', color='red', s=10)
    ax2.set_ylabel('Coulombic Efficiency (%)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_ylim(0, 110)

    # Add a legend
    ax1.legend(loc='lower left')
    ax2.legend(loc='lower right')

    # Add a horizontal line for theoretical capacity if provided
    if theoretical_capacity is not None:
        ax1.axhline(theoretical_capacity, color='orange', linestyle='--', label='Theoretical Capacity')

    # Add a second x-axis for time since the start in days per cycle
    ax3 = ax1.twiny()
    ax3.set_xlabel('Time Since Start (days)')

    # Calculate the time in days for each cycle
    cycle_start_times = grouped['Timestamp'].min()
    time_since_start = (cycle_start_times - cycle_start_times.min()).dt.days

    ax3.scatter(max_charge.index, time_since_start, color='gray', marker='.', s=0.005)  # Reduce marker size
    ax3.xaxis.set_ticks_position('top')  # Move to the top
    ax3.xaxis.set_label_position('top')  # Move to the top
    ax3.set_xlim([0, time_since_start.max()])  # Set x-axis limits

    # Show the plot
    plt.show()

print_ndax_as_csv(r"G:\.shortcut-targets-by-id\1gpf-XKVVvMHbMGqpyQS5Amwp9fh8r96B\RUG shared\Master Project\Experiment files\FF041\FF041Batt_b.ndax")
plot_capacity(r"G:\.shortcut-targets-by-id\1gpf-XKVVvMHbMGqpyQS5Amwp9fh8r96B\RUG shared\Master Project\Experiment files\FF027\FF027Ba.ndax",
              theoretical_capacity=0.8)
