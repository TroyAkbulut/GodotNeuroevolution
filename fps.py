import matplotlib.pyplot as plt
from matplotlib import gridspec
import statistics

framesHistories = []

with open("frames.txt", "r") as f:
    for readFrames in f.readlines():
        frames = [int(frame) for frame in readFrames.split(", ")]
        framesHistories.append(frames)


labels = [1, 10, 20, 30, 40, 50]
i = 0
fig = plt.figure()
fig.set_figheight(8)
fig.set_figwidth(8)
spec = gridspec.GridSpec(ncols=2, nrows=3, width_ratios=[2,2], wspace=0.5, hspace=0.5, height_ratios=[2,2,2])
for frameHistory in framesHistories:
    ax = fig.add_subplot(spec[i])
    ax.plot(range(len(frameHistory)), frameHistory)
    ax.set_ylabel("Frames per second")
    ax.set_xlabel("Seconds elapsed")
    ax.set_title(f"{labels[i]} Agents evaluated simultaneously")
    i+=1
    
plt.show()