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

def GetData(int isPresence):
  sensed = s.getValues(100)
  mean = Mean(sensed)
  st_des = St_des(sensed)
  corr_coef = Corr_coef(sensed)
  var = Variance(sensed)
  writer.writerow([mean, st_des, corr_coef, var, isPresence])

def PlotData():
  sensed = s.getValues(100)
  fig, ax = plt.subplots( nrows=1, ncols=1 )
  ax.plot(muestra, sensed,'o', color='b')
  ax.set_title("Distance SRF02")
  ax.set_ylabel("cms")
  ax.set_xlabel("# samples")
  fig.savefig("Samples.png")

with open(outFilename, "data.csv", 'w', newline='') as outFile:
  writer = csv.writer(file)
  #Titles of data
  writer.writerow(["SN", "Name", "Contribution"])
  #Start Program
  while (True):
    #Input option
    opc = input("Enter:\n 1)Presencia persona\n 2)No hay presencia\n 3)Quitar\n 4)Plotear datos\n")
    #Get data for presence
    if(opc == "1"):
      GetData(1)
    #Get data for not presence
    if(opc == "2"):
      GetData(0)
    #Cerrar programa
    if(opc == "3"):
      break
    #Plot data and get image
    if(opc == "4"):
      PlotData()