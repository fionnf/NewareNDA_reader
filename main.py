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



def plot_capacity(file_path, theoretical_capacity=None, styles=None):
    if styles is None:
        styles = {}

    data = pd.DataFrame(nda.read(file_path))

    grouped = data.groupby('Cycle')
    max_charge = grouped['Charge_Capacity(mAh)'].max()
    max_discharge = grouped['Discharge_Capacity(mAh)'].max()
    coulombic_efficiency = (max_discharge / max_charge) * 100

    fig, ax1 = plt.subplots(figsize=styles.get('figure_size', (10, 8)))

    ax1.scatter(max_charge.index, max_charge, label='Charge Capacity', color='blue', s=styles.get('scatter_size', 10))
    ax1.scatter(max_discharge.index, max_discharge, label='Discharge Capacity', color='green', s=styles.get('scatter_size', 10))
    ax1.set_xlabel('Cycle Number', fontsize=styles.get('axis_label_fontsize', 14))
    ax1.set_ylabel('Capacity (mAh)', color='blue', fontsize=styles.get('axis_label_fontsize', 14))
    ax1.tick_params(axis='y', labelcolor='blue', labelsize=styles.get('tick_label_fontsize', 12))
    ax1.tick_params(axis='x', labelsize=styles.get('tick_label_fontsize', 12))
    ax1.set_ylim(0, max(max_charge.max(), max_discharge.max()) * 1.1)
    ax1.set_xlim(0, max(max_charge.index.max(), max_discharge.index.max()) * 1.1)

    ax2 = ax1.twinx()
    ax2.scatter(max_charge.index, coulombic_efficiency, label='Coulombic Efficiency', color='red', s=styles.get('scatter_size', 10))
    ax2.set_ylabel('Coulombic Efficiency (%)', color='red', fontsize=styles.get('axis_label_fontsize', 14))
    ax2.tick_params(axis='y', labelcolor='red', labelsize=styles.get('tick_label_fontsize', 12))
    ax2.set_ylim(0, 110)
    ax2.set_xlim(0, max(max_charge.index.max(), max_discharge.index.max()) * 1.1)

    if theoretical_capacity is not None:
        line_style = styles.get('line_styles', {}).get('theoretical_capacity', {'color': 'orange', 'linestyle': '--'})
        ax1.axhline(theoretical_capacity, label='Theoretical Capacity', **line_style)

    legend = ax1.legend(loc='upper right', fontsize=styles.get('legend_fontsize', 12))

    plt.tight_layout()
    plt.show()

plot_styles = {
    'figure_size': (10, 8),
    'axis_label_fontsize': 18,
    'tick_label_fontsize': 16,
    'legend_fontsize': 16,
    'scatter_size': 10,
    'line_styles': {
        'theoretical_capacity': {'color': 'orange', 'linestyle': '--'}
    }
}

file_path = r"G:\.shortcut-targets-by-id\1gpf-XKVVvMHbMGqpyQS5Amwp9fh8r96B\RUG shared\Master Project\Experiment files\FF042\FF042batt_a.ndax"

#print_ndax_as_csv(file_path)
plot_capacity(file_path, theoretical_capacity=0.8, styles=plot_styles)
