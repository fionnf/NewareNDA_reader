# Capacity Plotter

## Overview

Capacity Plotter is a Python-based application that allows users to visualize and analyze NDAX files. The application provides functionalities to plot capacity and voltage data, save plots as images, and export data to CSV files. The user interface is built using Tkinter, and plots are generated using Matplotlib.

## Features

- **File Browsing**: Select NDAX files using a file dialog.
- **Plot Capacity**: Visualize capacity data with options to show percentage and start time.
- **Plot Voltage**: Visualize voltage data.
- **Save Plots**: Save generated plots as high-resolution images.
- **Export to CSV**: Export data to CSV format.
- **Dark Theme**: User interface with a dark theme for better visual comfort.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/capacity-plotter.git
    cd capacity-plotter
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```sh
    python main.py
    ```

## Usage

1. **Browse File**: Click the "Browse" button to select an NDAX file.
2. **Set Parameters**: Enter the theoretical capacity, minimum and maximum cycles, and select the desired options (e.g., show percentage, start time).
3. **Choose Plot Type**: Select either "Plot Capacity" or "Plot Voltage".
4. **Execute**: Click the "Execute" button to generate the plot.
5. **Save/Export**: Optionally, save the plot as an image or export the data to CSV.

## Dependencies

- Python 3.x
- Tkinter
- Matplotlib

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Contact

For any questions or issues, please open an issue on GitHub or contact the maintainer at fionn@fionnferreira.com