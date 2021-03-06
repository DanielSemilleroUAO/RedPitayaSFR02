#Author: Jhonatan Narvaez 
#Matrikelnummer: 1329832 

#Libraries
import srf02
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import csv
#Import object SRF02
s = srf02.srf02()
#Variable for samples
muestra = []
#Create #samples for graphs
for i in range(0,100):
    muestra.append(i)

def _roll(a, shift):
  if not isinstance(a, np.ndarray):
      a = np.asarray(a)
  idx = shift % len(a)
  return np.concatenate([a[-idx:], a[:-idx]])

def _into_subchunks(x, subchunk_length, every_n=1):
  len_x = len(x)
  assert subchunk_length > 1
  assert every_n > 0
  num_shifts = (len_x - subchunk_length) // every_n + 1
  shift_starts = every_n * np.arange(num_shifts)
  indices = np.arange(subchunk_length)
  indexer = np.expand_dims(indices, axis=0) + np.expand_dims(shift_starts, axis=1)
  return np.asarray(x)[indexer]

#Get mean of signal
def Mean(signal):
  mean = np.mean(signal)
  return mean

#Get Standard deviation
def St_des(signal):
  st_des = np.std(signal)
  return st_des

#Get Variance
def Variance(signal):
  variance = np.var(signal)
  return variance

#Get Energy signal time
def Abs_Energy(signal):
  signal = np.asarray(signal)
  abs_energy = np.dot(signal,signal)
  return abs_energy

#Get sum absolute of change:
def Sum_Absolute_Change(signal):
  sum_absolute_change = np.sum(np.abs(np.diff(signal)))
  return sum_absolute_change

#Get agg correlation

#Get autocorrelation
def Autocorrelation(signal):
  x = signal
  lag = 2
  if len(x) < lag:
        return 0
  # Slice the relevant subseries based on the lag
  y1 = x[:(len(x) - lag)]
  y2 = x[lag:]
  # Subtract the mean of the whole series x
  x_mean = np.mean(x)
  # The result is sometimes referred to as "covariation"
  sum_product = np.sum((y1 - x_mean) * (y2 - x_mean))
  # Return the normalized unbiased covariance
  v = np.var(x)
  if np.isclose(v, 0):
      return 0
  else:
      return sum_product / ((len(x) - lag) * v)

#Get counts above the threshold
def Above_Threshold(signal):
  signal = np.array(signal)
  above_threshold = np.sum(signal[signal <= 80])/len(signal)
  return above_threshold

#Get count above mean
def Above_Median(signal):
  signal = np.array(signal)
  m = np.mean(signal)
  above_median = np.where(signal[signal > m])[0].size
  return above_median

def Below_Threshold(signal):
  signal = np.array(signal)
  below_threshold = np.sum(signal[signal <= 80])/len(signal)
  return below_threshold

def Below_Median(signal):
  signal = np.array(signal)
  m = np.mean(signal)
  below_median = np.where(signal[signal < m])[0].size
  return below_median

def Mean_Abs(signal):
  signal = np.array(signal)
  mean_abs = np.mean(np.abs(np.diff(signal)))
  return mean_abs

def Crossing_M(signal):
  x = np.asarray(signal)
  positive = x > 80
  crossign_m = np.where(np.diff(positive))[0].size
  return crossign_m

def Number_Peak(signal):
  signal = np.array(signal)
  x = signal
  n = int(np.max(signal))
  x_reduced = x[n:-n]
  res = None
  for i in range(1, n + 1):
    result_first = (x_reduced > _roll(x, i)[n:-n])
    if res is None:
        res = result_first
    else:
        res &= result_first
    res &= (x_reduced > _roll(x, -i)[n:-n])
  number_peak = np.sum(res)
  return number_peak

def Sample_Entropy(signal):
  x = np.array(signal)
  if np.isnan(x).any():
      return 0
  m = 2
  tolerance = 0.2 * np.std(x)
  xm = _into_subchunks(x, m)
  B = np.sum([np.sum(np.abs(xmi - xm).max(axis=1) <= tolerance) - 1 for xmi in xm])
  xmp1 = _into_subchunks(x, m + 1)
  A = np.sum([np.sum(np.abs(xmi - xmp1).max(axis=1) <= tolerance) - 1 for xmi in xmp1])
  sample_entropy = -np.log(A / B)
  return sample_entropy

def Variation_Coef(signal):
  signal = np.array(signal)
  mean = np.mean(signal)
  if mean != 0:
      return np.std(signal) / mean
  else:
      return 0

def Fft_energy(signal):
  return np.sum(np.abs(np.fft.fft(signal))**2)

def Fft_std(signal):
  return np.std(np.fft.fft(signal))

def Fft_mean(signal):
  return np.abs(np.mean(np.fft.fft(signal)))

def getStats(values, field):
  results = {"min": values[0][field], 
             "max": values[0][field],
             "mean": 0, 
             "count": 0,
             "sum": 0,
             "distanceDelta": 0,
             "timeDelta": 0,
             "speed":0,}
  for value in values:
    results["min"] = min(results["min"], value[field])
    results["max"] = max(results["max"], value[field])
    results["count"] += 1
    results["sum"] += value[field]
  results["mean"] = results["sum"] / results["count"]
  # distance delta in cm
  results["distanceDelta"] =  values[len(values) - 1][field] - values[0][field]
  results["timeDelta"] = (values[len(values) - 1]["elapsed"] - values[0]["elapsed"]).total_seconds()
  results["speed"] = results["distanceDelta"] / (100 * results["timeDelta"])
  return results

def PlotData(distance,mindistance,TimeElapse,isPresence):
  presence = "yes"
  if(isPresence):
    presence = "yes"
  else:
    presence = "no"
  #Plot distance
  fig, ax = plt.subplots( nrows=1, ncols=1 )
  ax.plot(muestra, distance,'o', color='b')
  ax.grid()
  ax.set_title("Distance SRF02")
  ax.set_ylabel("cm")
  ax.set_xlabel("# samples")
  fig.savefig("Distance"+presence+".png")
  #Plot distance
  fig, ax = plt.subplots( nrows=1, ncols=1 )
  ax.plot(muestra, mindistance,'o', color='b')
  ax.set_title("Min Distance SRF02")
  ax.set_ylabel("cm")
  ax.set_xlabel("# samples")
  fig.savefig("Mindistance"+presence+".png")
  #Plot distance
  fig, ax = plt.subplots( nrows=1, ncols=1 )
  ax.plot(muestra, TimeElapse,'o', color='b')
  ax.set_title("Time elapse SRF02")
  ax.set_ylabel("seconds")
  ax.set_xlabel("# samples")
  fig.savefig("TimeElapse"+presence+".png")

with open("data.csv", 'w', newline='') as file:
  writer = csv.writer(file)
  #Titles of data
  writer.writerow(["distance_min", "distance_max", "distance_mean","distance_delta","variance", "st_des","autocorrelation","above_Threshold","above_Median","below_Threshold","below_Median","crossing_m","sample_entropy","variation_coef","fft_power","fft_std","fft_mean","presence"])
  #Start Program
  while (True):
    #Input option
    opc = input("Enter:\n 1)Presencia persona\n 2)No hay presencia\n 3)Quitar\n 4)Plotear datos presencia\n 5)Plotear datos no presencia\n")
    #Get data for presence
    if(opc == "1"):
      sensed,distance,mindistance,TimeElapse = s.getValues(100)
      rangeStats =  getStats(sensed, "distance")
      print("distance_min "+str(rangeStats["min"]))
      print("distance_max "+str(rangeStats["max"]))
      print("distance_mean "+str(rangeStats["mean"]))
      print("distance_delta "+str(rangeStats["distanceDelta"]))
      print("Variance "+str(Variance(distance)))
      print("St_des "+str(St_des(distance)))
      #print(str(Mean(distance))+"\n")
      print("Autocorrelation "+str(Autocorrelation(distance)))
      print("Above_Threshold "+str(Above_Threshold(distance)))
      print("Above_Median "+str(Above_Median(distance)))
      print("Below_Threshold "+str(Below_Threshold(distance)))
      print("Below_Median "+str(Below_Median(distance)))
      #print(str(Mean_Abs(Mean_Abs))+"\n")
      print("Crossing_M "+str(Crossing_M(distance)))
      #print(str(Number_Peak(distance))+"\n")
      print("Sample_Entropy "+str(Sample_Entropy(distance)))
      print("Variation_Coef "+str(Variation_Coef(distance)))
      print("Fft_power "+str(Fft_energy(distance)))
      print("Fft_std "+str(Fft_std(distance)))
      print("Fft_mean "+str(Fft_mean(distance)))
      print("Presence = 1 ")
      for i in range(50):
        sensed,distance,mindistance,TimeElapse = s.getValues(100)
        rangeStats =  getStats(sensed, "distance")
        writer.writerow([rangeStats["min"], rangeStats["max"], rangeStats["mean"],rangeStats["distanceDelta"],Variance(distance),St_des(distance),Autocorrelation(distance),Above_Threshold(distance),Above_Median(distance),Below_Threshold(distance),Below_Median(distance),Crossing_M(distance),Sample_Entropy(distance),Variation_Coef(distance),Fft_energy(distance),Fft_std(distance),Fft_mean(distance),1])
      
      print("Terminado captura datos con presencia")
    #Get data for not presence
    if(opc == "2"):
      sensed,distance,mindistance,TimeElapse = s.getValues(100)
      rangeStats =  getStats(sensed, "distance")
      print("distance_min "+str(rangeStats["min"]))
      print("distance_max "+str(rangeStats["max"]))
      print("distance_mean "+str(rangeStats["mean"]))
      print("distance_delta "+str(rangeStats["distanceDelta"]))
      print("Variance "+str(Variance(distance)))
      print("St_des "+str(St_des(distance)))
      #print(str(Mean(distance))+"\n")
      print("Autocorrelation "+str(Autocorrelation(distance)))
      print("Above_Threshold "+str(Above_Threshold(distance)))
      print("Above_Median "+str(Above_Median(distance)))
      print("Below_Threshold "+str(Below_Threshold(distance)))
      print("Below_Median "+str(Below_Median(distance)))
      #print(str(Mean_Abs(Mean_Abs))+"\n")
      print("Crossing_M "+str(Crossing_M(distance)))
      #print(str(Number_Peak(distance))+"\n")
      print("Sample_Entropy "+str(Sample_Entropy(distance)))
      print("Variation_Coef "+str(Variation_Coef(distance)))
      print("Fft power "+str(Fft_energy(distance)))
      print("Fft_std "+str(Fft_std(distance)))
      print("Fft_mean "+str(Fft_mean(distance)))
      print("Presence = 0 ")
      for i in range(50):
        sensed,distance,mindistance,TimeElapse = s.getValues(100)
        rangeStats =  getStats(sensed, "distance")
        writer.writerow([rangeStats["min"], rangeStats["max"], rangeStats["mean"],rangeStats["distanceDelta"],Variance(distance),St_des(distance),Autocorrelation(distance),Above_Threshold(distance),Above_Median(distance),Below_Threshold(distance),Below_Median(distance),Crossing_M(distance),Sample_Entropy(distance),Variation_Coef(distance),Fft_energy(distance),Fft_std(distance),Fft_mean(distance),0])
      print("Terminado captura de datos sin presencia")
    #Close Program
    if(opc == "3"):
      break
    #Plot data and get image presence
    if(opc == "4"):
      sensed,distance,mindistance,TimeElapse = s.getValues(100)
      PlotData(distance,mindistance,TimeElapse,True)
    #Plot data and get image no presence
    if(opc == "5"):
      sensed,distance,mindistance,TimeElapse = s.getValues(100)
      PlotData(distance,mindistance,TimeElapse,False)