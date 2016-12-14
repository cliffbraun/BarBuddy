import csv
import argparse
from matplotlib import pyplot
from scipy.signal import butter, filtfilt
import numpy as np

def parse_csv(filename):
    """ Function to parse the file from input, takes in a filename, outputs x and y arrays"""
    with open(args.filename, 'rb') as csvfile:
        plotReader = csv.reader(csvfile, delimiter=',')
        rowcounter = 1
        time = []
        orientations = []
        accelerationx = []
        accelerationy = []
        accelerationz = []
        temps = []

        for row in plotReader:
            if len(row[0]) > 0  and row[0][0] == "#":
                print "Skipping commented row: " + str(rowcounter)
            else:
                try:
                    time.append(float(row[0]))
                    orientations.append([(float(row[1])+380)%360, float(row[2]), float(row[3])])
                    accelerationx.append([(float(row[4]))])#, float(row[5]), float(row[6])])
                    accelerationy.append([(float(row[5]))])
                    accelerationz.append([(float(row[6]))])#
                    temps.append(int(float(row[7])))
                except ValueError:
                    print row
                    print "Invalid data in row: " + str(rowcounter) + " skipping"

            rowcounter = rowcounter + 1
    return time, orientations, accelerationx, accelerationy, accelerationz, temps

def plot_array(xvalues, yvalues, zvalues=None):
    """ Function to plot values and provide some python references"""
    pyplot.plot(xvalues, yvalues)
    if zvalues is not None:
        pyplot.plot(xvalues, zvalues, 'r')
    pyplot.title("Curl Orientation Values")
    pyplot.xlabel("Time(ms)")
    pyplot.ylabel("Degrees")
    pyplot.legend(["Heading", "Roll", "Pitch"])
    pyplot.autoscale()
    pyplot.show()

def butter_lowpass(cutoff, fs=25, order=5):
    nyq = fs*0.5
    normal_cutoff = cutoff/nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filtfilt(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data, padlen=2)
    return y



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    time, orientations, accelerationx, accelerationy, accelerationz, temps = parse_csv(args.filename)
    pyplot.plot(time, orientations)
    print(np.array(accelerationx))
    accelerationx_filtered = butter_lowpass_filtfilt(10*np.array(accelerationx).transpose(), 25, 2100)
    pyplot.plot(time, accelerationx_filtered.transpose())
    accelerationy_filtered = butter_lowpass_filtfilt(10*np.array(accelerationy).transpose(), 25, 2100)
    pyplot.plot(time, accelerationy_filtered.transpose())
    accelerationz_filtered = butter_lowpass_filtfilt(10*np.array(accelerationz).transpose(), 25, 2100)
    pyplot.plot(time, accelerationz_filtered.transpose())
    pyplot.legend(["heading", "roll", "pitch", "x", "y", "z"], fontsize='small')
    pyplot.title("Motion Data from Excercise")
    pyplot.xlabel("Time (ms)")
    pyplot.ylabel("Gravity (m/s^2), Orientation(degrees)")
    pyplot.autoscale()
    pyplot.show()
    #plot_array(time, orientations)
    #plot_array(time, accelerationx_filtered.transpose(), accelerationy_filtered.transpose())
    #plot_array(time, temps)


