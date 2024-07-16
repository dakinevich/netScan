import pyshark
import matplotlib.pyplot as plt

def plot_packet_timings(file_path):
    cap = pyshark.FileCapture(file_path)
    timings = []
    for i in range(5000):  # Limiting to first 5000 packets
        try:
            timings.append(float(cap[i].frame_info.time_relative))
        except:
            break
    print(f"Last timing value: {timings[-1]}")
    bins = int(timings[-1] / 2)  # Determining the number of bins
    return timings, bins

# Paths to your pcapng files
normal_pcap_path = '172.16.1.9_normal.pcapng'
anomaly_pcap_path = '172.16.1.9_anomaly.pcapng'

# Extract timings and determine bins for both files
normal_timings, normal_bins = plot_packet_timings(normal_pcap_path)
anomaly_timings, anomaly_bins = plot_packet_timings(anomaly_pcap_path)

# Plotting the histograms
plt.figure(figsize=(12, 8))  # Adjust figure size as needed
plt.hist(normal_timings, bins=normal_bins, alpha=0.5, label='172.16.1.9_normal', color='blue')  # Normal traffic in blue
plt.hist(anomaly_timings, bins=anomaly_bins, alpha=0.5, label='172.16.1.9_anomal', color='red')  # Anomaly traffic in red

# Adding title, labels, and legend
plt.title('Распределение трафика')
plt.xlabel('Время (s)')
plt.ylabel('Частота пакетов (в течении 2 секунд)')
plt.legend()

plt.show()













exit(0)
line = cap[5]
cmds = [
    'captured_length', 'eth', 'frame_info', 'get_multiple_layers', 'get_raw_packet', 'highest_layer', 'interface_captured',
 'ip', 'layers', 'length', 'number', 'pretty_print', 'show', 'sniff_time', 'sniff_timestamp', 'snmp', 'transport_layer', 'udp'
]
for i in cmds:
    try:
        print(i, getattr(line, i))
    except:
        pass
for i in ['time_delta', 'time_delta_displayed', 'time_epoch', 'time_relative', 'time_utc']:
    print(i, getattr(line.frame_info,i))

print(line.frame_info.time_relative)
print(dir(cap))
    

