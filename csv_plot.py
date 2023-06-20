import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('data2.csv')
df = pd.DataFrame(df, columns=['Timestamp','PF_Set', 'PF_Meas', 'PF_Error'])
Timestamp = pd.to_datetime(df["Timestamp"])
PF_Set = df['PF_Set'].to_numpy()
PF_Meas = df['PF_Meas'].to_numpy()
PF_Error = df['PF_Error'].to_numpy()

# Create the figure and axes
fig, ax1 = plt.subplots(figsize=(16, 9)) # Adjust the figure size to 16:9 aspect ratio

# Plot the first dataset with ax1
ax1.plot(Timestamp,PF_Set, color='tab:blue',label='Set PF')
ax1.plot(Timestamp,PF_Meas, color='tab:green',label='Measured PF')
ax1.set_xlabel('Time')
ax1.set_ylabel('Power Factor', color='k')
ax1.set_ylim(0.55, np.max(PF_Meas))

# Create the second y-axis
ax2 = ax1.twinx()

# Plot the second dataset with ax2
ax2.plot(Timestamp,PF_Error, color='tab:red',alpha=1.0,label='Error')
ax2.set_ylabel('Error (%)', color='k')
ax2.set_ylim(0, 15)

# Add legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2)

plt.title('Power Factor Test Results')

# Display the plot
plt.grid()
plt.tight_layout()

resolution_value = 600
plt.savefig("PF_Results.png", format="png", dpi=resolution_value)
plt.show()

