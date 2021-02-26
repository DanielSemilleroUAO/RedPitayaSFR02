import srf02
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import csv

s = srf02.srf02()
muestra = []
#print(numero_muestras)
for i in range(0,100):
    muestra.append(i)

def getStats(values, field):
  results = {"min": values[0][field], 
             "max": values[0][field],
             "mean": 0, 
             "count": 0,
             "sum": 0,
             "distanceDelta": 0,
             "timeDelta": 0,
             "speed":0 }
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

def Mean(signal):
  mean = np.mean(signal)
  return mean

def St_des(signal):
  st_des = np.std(signal)
  return st_des

def Variance(signal):
  variance = np.var(signal)
  return variance

def Corr_coef(signal):
  corr_coef = np.corrcoef(signal)
  return corr_coef

def GetData():
  sensed,distance,mindistance,TimeElapse = s.getValues(100)
  mean = Mean(distance)
  st_des = St_des(distance)
  corr_coef = Corr_coef(distance)
  var = Variance(distance)
  return mean,st_des,corr_coef,var

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



with open("data.csv", 'w', newline='') as outFile:
  writer = csv.writer(outfile)
  #Titles of data
  writer.writerow(["distance_min", "distance_max", "distance_mean","distance_delta","mindistance_min", "mindistance_max", "mindistance_mean","mindistance_delta","timeDelta","speed","presence"])
  #Start Program
  while (True):
    #Input option
    opc = input("Enter:\n 1)Presencia persona\n 2)No hay presencia\n 3)Quitar\n 4)Plotear datos presencia\n 5)Plotear datos no presencia\n")
    #Get data for presence
    if(opc == "1"):
      sensed,distance,mindistance,TimeElapse = s.getValues(100)
      rangeStats =  getStats(sensed, "distance")
      minRangeStats =  getStats(sensed, "mindistance")
      elapsedRangeStats = getStats(sensed, "elapsed")
      writer.writerow([rangeStats["min"], rangeStats["max"], rangeStats["mean"],rangeStats["distanceDelta"],minRangeStats["min"], minRangeStats["max"], minRangeStats["mean"],minRangeStats["distanceDelta"],elapsedRangeStats["timeDelta"],elapsedRangeStats["speed"],1])
      #GetData(1)
    #Get data for not presence
    if(opc == "2"):
      sensed,distance,mindistance,TimeElapse = s.getValues(100)
      rangeStats =  getStats(sensed, "distance")
      minRangeStats =  getStats(sensed, "mindistance")
      elapsedRangeStats = getStats(sensed, "elapsed")
      writer.writerow([rangeStats["min"], rangeStats["max"], rangeStats["mean"],rangeStats["distanceDelta"],minRangeStats["min"], minRangeStats["max"], minRangeStats["mean"],minRangeStats["distanceDelta"],elapsedRangeStats["timeDelta"],elapsedRangeStats["speed"],0])
      #GetData(0)
    #Cerrar programa
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