import os
import re
import pandas as pd

def extract_data_from_exp_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data_lines = []
    start_collecting = False

    for line in lines:
        if line.strip().startswith("$ PLOTTED"):
            start_collecting = True
            continue
        if line.strip().startswith("BLOCKEND"):
            start_collecting = False
            continue
        if start_collecting:
            split_line = line.strip().split()
            if len(split_line) >= 2:
                data_lines.append(split_line[:2])  # 只提取前两列数据

    return pd.DataFrame(data_lines, columns=["Temperature", "LiquidFraction"], dtype=float)

def find_temperatures(data):
    tolerance = 1e-8
    temp_liq_1 = data[(data['LiquidFraction'] >= 1.0 - tolerance) & (data['LiquidFraction'] <= 1.0 + tolerance)][
        'Temperature'].min()
    temp_liq_0 = data[data['LiquidFraction'].round(10) == 0.0]['Temperature'].max()
    return temp_liq_1, temp_liq_0

def process_files_in_folder(folder_path):
    results = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".exp"):
            file_path = os.path.join(folder_path, file_name)
            match = re.match(r"Al(\d+\.\d+)Fe(\d+\.\d+)Si_np-T\.exp", file_name)
            if match:
                x_value = float(match.group(1))
                y_value = float(match.group(2))

                data = extract_data_from_exp_file(file_path)
                temp_liq_1, temp_liq_0 = find_temperatures(data)

                if temp_liq_1 is not None and temp_liq_0 is not None:
                    z_value = temp_liq_1 - temp_liq_0
                    results.append([x_value, y_value, z_value])

    return results

def save_to_excel(data, output_file):
    df = pd.DataFrame(data, columns=["Fe_mass_fraction", "Si_mass_fraction", "Melting_range"])
    df.to_excel(output_file, index=False)

# 文件夹路径
folder_path = r"data\exp"
# 输出Excel文件路径
output_file = "output.xlsx"

# 处理文件夹中的exp文件并保存结果
data = process_files_in_folder(folder_path)
save_to_excel(data, output_file)
