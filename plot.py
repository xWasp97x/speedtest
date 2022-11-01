import pickle
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams.update({'figure.autolayout': True})

results = pickle.load(open('results.pkl', 'rb'))

times = [result['time'].strftime('%Y-%m-%d %H:%M:%S') for result in results]

fig, ax1 = plt.subplots()

x = range(len(results))
plt.xticks(x, times, rotation=90)

ax2 = ax1.twinx()
downloads = [result['download'] for result in results]
downloads_avg = sum(downloads) / len(downloads)
ax1.plot(x, downloads, 'b-', label=f'Download (avg: {downloads_avg:.2f} MB/s)')

uploads = [result['upload'] for result in results]
uploads_avg = sum(uploads) / len(uploads)
ax1.plot(x, uploads, 'r-', label=f'Upload (avg: {uploads_avg:.2f} MB/s)')
ax1.set_ylabel('Speed (MB/s)')
ax1.legend(loc='upper left')

pings = [result['ping'] for result in results]
pings_avg = sum(pings) / len(pings)
ax2.plot(x, pings, 'g-', label=f'Ping (avg: {pings_avg:.0f} ms)')
ax2.set_ylabel('Ping (ms)', color='g')
ax2.legend(loc='upper right')

plt.savefig('speedtest.png')
