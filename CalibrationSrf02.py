import srf02
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

outFilename = "srf02Calibration.txt"
s = srf02.srf02()
muestra = []
#print(numero_muestras)
for i in range(0,100):
    muestra.append(i)

def getStats(values, field):
  # where field is a string that's either "distance" or "mindistance"
  #todo: replace with implementation of EEP.js or at least something that accumulates the mean without a sum
  # todo: probably move the speed calculation elsewhere so we can use this function to smooth its inputs
  # speed is in m/s, assumes distance is in cm and we're always sensing the same object relative to the sensor
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

with open(outFilename, "a") as outFile:
  outFile.write("measured,senseMin,senseMax,senseMean,senseMinRangeMean\n")
  while (True):
    opc = input("Enter: 1)Presencia persona, 2)No hay presencia, 3)Quitar, 4)Plotear datos: ")
    if(opc == "1"):
      break
    if(opc == "2"):
      break
    if(opc == "3"):
      break
    if(opc == "4"):
      sensed = s.getValues(100)
      fig, ax = plt.subplots( nrows=1, ncols=1 )
      ax.plot(np.array(muestra), np.array(sensed),'o', color='b')
      #plt.set_title("Distance SRF02")
      #plt.set_ylabel("cms")
      #plt.set_xlabel("# samples")
      fig.savefig("Samples.png")
      rangeStats =  getStats(sensed, "distance")
      minRangeStats =  getStats(sensed, "mindistance")
      print ("measured: " + measured + ", sensed: " + str(rangeStats["mean"])  + ", minrange: " + str(minRangeStats["mean"]))
