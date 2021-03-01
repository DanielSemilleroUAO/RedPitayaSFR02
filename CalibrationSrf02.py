#Libraries
import srf02
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import csv
import tsfresh
#Import object SRF02
s = srf02.srf02()
#Variable for samples
muestra = []
#Create #samples for graphs
for i in range(0,100):
    muestra.append(i)

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
  abs_energy = tsfresh.feature_extraction.feature_calculators.abs_energy(signal)
  return abs_energy
#Get sum absolute of change:
def Sum_Absolute_Change(signal):
  sum_absolute_change = tsfresh.feature_extraction.feature_calculators.absolute_sum_of_changes(signal)
  return sum_absolute_change
#Get agg correlation
def Corr_coef(signal):
  corr_coef = tsfresh.feature_extraction.feature_calculators.agg_autocorrelation(signal, {"f_agg": "mean", "maxlag": 2 })
  return corr_coef

#Get autocorrelation
def Autocorrelation(signal):
  autocorrelation = tsfresh.feature_extraction.feature_calculators.autocorrelation(signal, 2)
  return autocorrelation
#Get counts above the threshold
def Above_Threshold(signal):
  above_threshold = tsfresh.feature_extraction.feature_calculators.count_above(signal, 80)
  return above_threshold
#Get count above mean
def Above_Median(signal):
  above_median = tsfresh.feature_extraction.feature_calculators.count_above_mean(signal)
  return above_median
def Below_Threshold(signal):
  below_threshold = tsfresh.feature_extraction.feature_calculators.count_below(signal, 80)
  return below_threshold
def Below_Median(signal):
  below_median = tsfresh.feature_extraction.feature_calculators.count_below_mean(signal)
  return below_median
def Mean_Abs(signal):
  mean_abs = tsfresh.feature_extraction.feature_calculators.mean_abs_change(signal)
  return mean_abs
def Crossing_M(signal):
  crossign_m = tsfresh.feature_extraction.feature_calculators.number_crossing_m(signal, 80)
  return crossign_m
def Number_Peak(signal):
  number_peak = tsfresh.feature_extraction.feature_calculators.number_peaks(signal, np.max(signal))
  return number_peak
def Sample_Entropy(signal):
  sample_entropy = tsfresh.feature_extraction.feature_calculators.sample_entropy(signal)
  return sample_entropy
def Variation_Coef(signal):
  variation_coef = tsfresh.feature_extraction.feature_calculators.variation_coefficient(signal)
  return variation_coef

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
  ax.set_title("Distance SRF02")
  ax.set_ylabel("cms")
  ax.set_xlabel("# samples")
  fig.savefig("Distance"+presence+".png")
  #Plot distance
  fig, ax = plt.subplots( nrows=1, ncols=1 )
  ax.plot(muestra, mindistance,'o', color='b')
  ax.set_title("Min Distance SRF02")
  ax.set_ylabel("cms")
  ax.set_xlabel("# samples")
  fig.savefig("Mindistance"+presence+".png")
  #Plot distance
  fig, ax = plt.subplots( nrows=1, ncols=1 )
  ax.plot(muestra, TimeElapse,'o', color='b')
  ax.set_title("Time elapse SRF02")
  ax.set_ylabel("cms")
  ax.set_xlabel("# samples")
  fig.savefig("TimeElapse"+presence+".png")

with open("data.csv", 'w', newline='') as file:
  writer = csv.writer(file)
  #Titles of data
  writer.writerow(["distance_min", "distance_max", "distance_mean","distance_delta","Variance", "St_des", "cor_coef","mean","Autocorrelation","Above_Threshold","Above_Median","Below_Threshold","Below_Median","Mean_Abs","Crossing_M","Number_Peak","Sample_Entropy","Variation_Coef","presence"])
  #Start Program
  while (True):
    #Input option
    opc = input("Enter:\n 1)Presencia persona\n 2)No hay presencia\n 3)Quitar\n 4)Plotear datos presencia\n 5)Plotear datos no presencia\n")
    #Get data for presence
    if(opc == "1"):
      sensed,distance,mindistance,TimeElapse = s.getValues(100)
      rangeStats =  getStats(sensed, "distance")
      writer.writerow([rangeStats["min"], rangeStats["max"], rangeStats["mean"],rangeStats["distanceDelta"],Variance(distance), St_des(distance),Corr_coef(distance),Mean(distance),Autocorrelation(distance),Above_Threshold(distance),Above_Median(distance),Below_Threshold(distance),Below_Median(distance),Mean_Abs(Mean_Abs),Crossing_M(distance),Number_Peak(distance),Sample_Entropy(distance),Variation_Coef(distance),1])
    #Get data for not presence
    if(opc == "2"):
      sensed,distance,mindistance,TimeElapse = s.getValues(100)
      rangeStats =  getStats(sensed, "distance")
      writer.writerow([rangeStats["min"], rangeStats["max"], rangeStats["mean"],rangeStats["distanceDelta"],Variance(distance), St_des(distance),Corr_coef(distance),Mean(distance),Autocorrelation(distance),Above_Threshold(distance),Above_Median(distance),Below_Threshold(distance),Below_Median(distance),Mean_Abs(Mean_Abs),Crossing_M(distance),Number_Peak(distance),Sample_Entropy(distance),Variation_Coef(distance),,0])
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