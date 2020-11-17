import matplotlib.pyplot as plt

def on_close(event):
    event.canvas.figure.axes[0].has_been_closed = True
    print('Closed Figure')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.has_been_closed = False
ax.plot(range(10))

fig.canvas.mpl_connect('close_event', on_close)

plt.show()

print(ax.has_been_closed)
