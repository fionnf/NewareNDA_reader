import NewareNDA as nda
import pandas as pd
import os
import matplotlib.pyplot as plt



def print_ndax_as_csv(file_path):
    data = nda.read(file_path)
    df = pd.DataFrame(data)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_csv_path = os.path.join(os.path.dirname(file_path), base_name + '.csv')
    df.to_csv(output_csv_path, index=False)
    print(f'Data printed to CSV file: {output_csv_path}')
    newaredata = df


def plot_capacity(file_path, start_min, theoretical_capacity=None, styles=None, min_cycle=None, max_cycle=None, save_image=False):
    if styles is None:
        styles = {}

    data = pd.DataFrame(nda.read(file_path))

    # Filter cycles if specified
    if min_cycle is not None:
        data = data[data['Cycle'] >= min_cycle]
    if max_cycle is not None:
        data = data[data['Cycle'] <= max_cycle]

    # Adjust cycle number and time if start_min is checked
    if start_min:  # assuming start_min is a BooleanVar
        min_cycle = data['Cycle'].min()
        data['Adjusted Cycle'] = data['Cycle'] - min_cycle
        # Adjust the timestamp to start from 0
        min_timestamp = pd.to_datetime(data['Timestamp']).min()
        data['Adjusted Time'] = (pd.to_datetime(data['Timestamp']) - min_timestamp).dt.total_seconds() / 86400  # days
    else:
        data['Adjusted Cycle'] = data['Cycle']
        data['Adjusted Time'] = (pd.to_datetime(data['Timestamp']) - pd.to_datetime(data['Timestamp']).min()).dt.total_seconds() / 86400  # days

    grouped = data.groupby('Adjusted Cycle')
    max_charge = grouped['Charge_Capacity(mAh)'].max()
    max_discharge = grouped['Discharge_Capacity(mAh)'].max()
    coulombic_efficiency = (max_discharge / max_charge) * 100

    fig, ax1 = plt.subplots(figsize=styles.get('figure_size', (10, 8)))
    fig.subplots_adjust(top=0.9, bottom=0.1)

    charge_plot = ax1.scatter(max_charge.index, max_charge, label='Charge Capacity', color='blue', s=styles.get('scatter_size', 10))
    discharge_plot = ax1.scatter(max_discharge.index, max_discharge, label='Discharge Capacity', color='green', s=styles.get('scatter_size', 10))
    ax1.set_xlabel('Cycle Number', fontsize=styles.get('axis_label_fontsize', 14))
    ax1.set_ylabel('Capacity (mAh)', color='blue', fontsize=styles.get('axis_label_fontsize', 14))
    ax1.tick_params(axis='y', labelcolor='blue', labelsize=styles.get('tick_label_fontsize', 12))
    ax1.tick_params(axis='x', labelsize=styles.get('tick_label_fontsize', 12))
    ax1.set_ylim(0, max(max_charge.max(), max_discharge.max()) * 1.1)
    ax1.set_xlim(0, max(max_charge.index.max(), max_discharge.index.max()) * 1.1)

    ax2 = ax1.twinx()
    efficiency_plot = ax2.scatter(max_charge.index, coulombic_efficiency, label='Coulombic Efficiency', color='red', s=styles.get('scatter_size', 10))
    ax2.set_ylabel('Coulombic Efficiency (%)', color='red', fontsize=styles.get('axis_label_fontsize', 14))
    ax2.tick_params(axis='y', labelcolor='red', labelsize=styles.get('tick_label_fontsize', 12))
    ax2.set_ylim(0, 110)
    ax2.set_xlim(0, max(max_charge.index.max(), max_discharge.index.max()) * 1.1)

    # Add a second x-axis for time since the start in days
    ax3 = ax1.twiny()
    ax3.set_xlabel('Time Since Start (days)', fontsize=styles.get('axis_label_fontsize', 14))
    ax3.scatter(max_charge.index, data.groupby('Adjusted Cycle')['Adjusted Time'].first(), color='gray', marker='.',
                s=styles.get('scatter_size', 0.005))
    ax3.xaxis.set_ticks_position('top')
    ax3.xaxis.set_label_position('top')
    ax3.tick_params(axis='x', labelsize=styles.get('tick_label_fontsize', 12))
    ax3.set_xlim([0, data['Adjusted Time'].max()])

    # Optional theoretical capacity line
    if theoretical_capacity is not None:
        line_style = styles.get('line_styles', {}).get('theoretical_capacity', {'color': 'orange', 'linestyle': '--'})
        ax1.axhline(theoretical_capacity, label='Theoretical Capacity', **line_style)

    # Adding a comprehensive legend that includes elements from both ax1 and ax2
    plots = [charge_plot, discharge_plot, efficiency_plot]
    labels = [plot.get_label() for plot in plots]
    ax1.legend(plots, labels, loc='lower right', fontsize=styles.get('legend_fontsize', 12))

    plt.tight_layout()

    # Save plot if requested
    if save_image:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_directory = os.path.dirname(file_path)
        output_image_path = os.path.join(output_directory, base_name + '.png')
        plt.savefig(output_image_path, dpi=600)

    return fig

plot_styles = {
    'figure_size': (10, 8),
    'axis_label_fontsize': 18,
    'tick_label_fontsize': 16,
    'legend_fontsize': 16,
    'scatter_size': 20,
    'line_styles': {
        'theoretical_capacity': {'color': 'orange', 'linestyle': '--'}
    }
}

def plot_voltage(file_path, min_cycle=None, max_cycle=None, save_image=False, styles=None):
    if styles is None:
        styles = {}

    # Load data
    data = pd.DataFrame(nda.read(file_path))

    # Filter cycles if specified
    if min_cycle is not None:
        data = data[data['Cycle'] >= min_cycle]
    if max_cycle is not None:
        data = data[data['Cycle'] <= max_cycle]

    # Convert Timestamps to datetime and then to elapsed time in hours
    data['Time'] = pd.to_datetime(data['Timestamp'])
    start_time = data['Time'].min()
    data['Elapsed Time'] = (data['Time'] - start_time).dt.total_seconds() / 3600  # Convert to hours

    # Plotting voltage over time
    fig, ax1 = plt.subplots(figsize=styles.get('figure_size', (10, 8)))
    fig.subplots_adjust(top=0.9, bottom=0.1)

    ax1.plot(data['Elapsed Time'], data['Voltage'], label='Voltage', color='black')
    ax1.set_xlabel('Time (hours)', fontsize=styles.get('axis_label_fontsize', 14))
    ax1.set_ylabel('Voltage (V)', color='black', fontsize=styles.get('axis_label_fontsize', 14))
    ax1.tick_params(axis='y', labelcolor='black', labelsize=styles.get('tick_label_fontsize', 12))
    ax1.tick_params(axis='x', labelsize=styles.get('tick_label_fontsize', 12))

    ax1.legend(loc='upper right', fontsize=styles.get('legend_fontsize', 12))

    plt.tight_layout()

    # Construct the save path using the same basename and directory as the input file
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_directory = os.path.dirname(file_path)
    output_image_path = os.path.join(output_directory, base_name + '_voltage.png')

    # Save the plot to the constructed file path
    if save_image:
        plt.savefig(output_image_path, dpi=600)

    # plt.show()  # Uncomment this line to display the plot when not running in a script
    return fig



