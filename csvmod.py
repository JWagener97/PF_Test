import csv
import numpy as np

output_file = 'data2.csv'

header = ["Timestamp","Volt_Set","Volt Meas","Current_Set", "Current_Meas", "Real Power","PF_Set","PF_Meas","PF_Error",]

with open(output_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)

def read_csv_file(filename):
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            data.append(row)
    return data

# Example usage:
csv_filename = 'data.csv'
csv_data = read_csv_file(csv_filename)

def Cur_set(I):
    I = float(I)
    if (0.1 < I < 0.3):
        I = 0.2
    elif (0.3 < I < 0.9):
        I = 0.5
    elif (0.9 < I < 2.0):
        I = 1.0
    else:
        I = 5.0   
    return I

def PF_sett(PF):
    PF = float(PF)
    if (0.5 < PF < 0.7):
        PF = 0.6
    elif (0.7 < PF < 0.9):
        PF = 0.8
    elif (0.9 < PF < 1.1):
        PF = 1.0
    return PF

def err_percent(val_true,val_test):
    val_true = float(val_true)
    val_test = float(val_test)
    Err = np.abs(val_true- val_test)/val_true
    return Err * 100
def process_csv_data(csv_data, output_file):
    i = 0  # Initialize counter
    
    # Iterate over each row in csv_data
    for row_num, row in enumerate(csv_data):
        if row_num == 0:  # Skip the first row
            continue
        
        Time = row[0]
        Volt_set = 230
        Volt_meas = row[1]
        I_meas = row[2]
        I_set = Cur_set(I_meas)
        P_meas = row[3]
        PF_Meas = row[4]
        PF_set = PF_sett(PF_Meas)
        PF_Error = err_percent(PF_set, PF_Meas)
        new_data = [Time, Volt_set, Volt_meas, I_set, I_meas, P_meas, PF_set, PF_Meas, PF_Error]
        print(new_data)
        
        if PF_Error < 3:
            with open(output_file, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(new_data)
        else:
            i += 1
    
    print(i)
process_csv_data(csv_data, output_file)

    
