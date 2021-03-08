#Libraries
import srf02
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
#Import object SRF02
s = srf02.srf02()
#Variable for samples
muestra = []
#Create #samples for graphs
for i in range(0,100):
    muestra.append(i)

def NormalizarDatos(data,opc):
  YMin = -1
  YMax = 1
  Vmax = 0
  Vmin = 0
  data_output = 0
  if opc == 0:
    Vmax = 69.27058823529411
    Vmin = 0.00392156862745098
  elif opc == 1:
    Vmax = 256.0
    Vmin = 51.2
  elif opc == 2:
    Vmax = 74.55368627450973
    Vmin = 50.928941176470495
  elif opc == 3:
    Vmax = 82.32156862745097
    Vmin = -70.27450980392157
  elif opc == 4:
    Vmax = 792.798615626
    Vmin = 0.0197540269127
  elif opc == 5:
    Vmax = 28.1566797692
    Vmin = 0.140549019608
  elif opc == 6:
    Vmax = 0.768904520534
    Vmin = -0.223468321452
  elif opc == 7:
    Vmax = 72.4934509804
    Vmin = 37.1278431373
  elif opc == 8:
    Vmax = 98.0
    Vmin = 5.0
  elif opc == 9:
    Vmax = 72.4934509804
    Vmin = 37.1278431373
  elif opc == 10:
    Vmax = 95.0
    Vmin = 2.0
  elif opc == 11:
    Vmax = 42.0
    Vmin = 0.0
  elif opc == 12:
    Vmax = 2.28916207266
    Vmin = 0.0235241346502
  elif opc == 13:
    Vmax = 0.442236047171
    Vmin = 0.00274617497058
  elif opc == 14:
    Vmax = 60676524.4368
    Vmin = 25939556.9827
  elif opc == 15:
    Vmax = 772.965758863
    Vmin = 506.728852373
  elif opc == 16:
    Vmax = 96.3803921569
    Vmin = 11.0470588235
  else:
    Vmax = 0
    Vmin = 0
  data_output = YMin + ((data - Vmin) * ((YMax - YMin) / (Vmax - Vmin)))
  return data_output
  

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

def FFt(signal):
  return np.abs(np.fft.fft(signal))**2

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

def StringFft(fft):
  data = ""
  for x in range(len(fft)):
    data+="[{x},{y}],".format(x=x*2.5, y=fft[x]/1000000)
  return data

def StringDistance(distance):
  data = ""
  for x in range(len(distance)):
    data+="[{x},{y}],".format(x=x, y=distance[x])
  return data

def PublicarApp(isPresence, porcent,plotDistance,plotFFT):
  f = open("PaginaPrincipal.html", "w")
  estado = """
  <h1 class="d-none d-md-block text-center text-capitalize text-light" style="">
    <b class="mx-2">Hi, Presence {porcent}% </b>
    <span class="blue">-</span>
  </h1>
  """.format(porcent=porcent)
  if(isPresence):
    estado = """
    <h1 class="d-none d-md-block text-center text-capitalize text-light" style="">
      <b class="mx-2">Hi, Presence: {porcent}%</b>
      <span class="grey">-</span>
    </h1>
    """.format(porcent=porcent)
  message = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <!-- Configuración de la pagina -->
  <!-- ICONO PAGINA-->
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="Frankfurt-University-logo.png">
  <!-- NOMBRE PAGINA -->
  <title>Project S3</title>
  <meta name="description" content="Colombia.">
  <meta name="keywords" content="Intelligence network">
  <meta http-equiv="refresh" content="30">
  <!-- CSS ESTILO -->
  <link rel="stylesheet" href="estilo_paginas.css">
  <!-- Importación JS para la barra de navegación -->
  <script src="navbar-ontop.js"></script>
  <script src="smooth-scroll.js" style=""></script>
  <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
  <script type="text/javascript" style="">
    // Load Charts and the corechart package.
    google.charts.load('current', {{
      'packages': ['corechart', 'line']
    }});
    google.charts.setOnLoadCallback(drawBasic1);
    google.charts.setOnLoadCallback(drawBasic2);
    myFunction();
    
    function addZero(i) {{
      if (i < 10) {{
        i = "0" + i;
      }}
      return i;
    }}
    function myFunction() {{
      var d = new Date();
      var dia = d.getDate();
      var ano = d.getFullYear();
      var mes = d.getMonth()+1;
      var x = document.getElementById("demo");
      var h = addZero(d.getHours());
      var m = addZero(d.getMinutes());
      var s = addZero(d.getSeconds());
      x.innerHTML = ano+"/"+mes+"/"+dia+"-"+h + ":" + m + ":" + s;
      //document.getElementById('dia_inicio_t').value = ano+"-"+mes+"-"+(dia-1);
      //document.getElementById('dia_final_t').value = ano+"-"+mes+"-"+dia;
      //document.getElementById('tiempo_inicio_t').value = h+":"+ m +":00"; 
      //document.getElementById('tiempo_final_t').value = h+":"+ m +":00"; 
    }}

    function mueveReloj(){{
    momentoActual = new Date()
    hora = momentoActual.getHours()
    minuto = momentoActual.getMinutes()
    segundo = momentoActual.getSeconds()

    var f = new Date();

    str_segundo = new String (segundo)
    if (str_segundo.length == 1)
       segundo = "0" + segundo

    str_minuto = new String (minuto)
    if (str_minuto.length == 1)
       minuto = "0" + minuto

    str_hora = new String (hora)
    if (str_hora.length == 1)
       hora = "0" + hora

    horaImprimible = f.getDate() + "/" + (f.getMonth() +1) + "/" + f.getFullYear() +" - "+hora + " : " + minuto + " : " + segundo

    document.form_reloj.reloj.value = horaImprimible

    setTimeout("mueveReloj()",1000)
    }}

    function drawBasic1() {{

      var data = google.visualization.arrayToDataTable([  
        ['muestra', 'distance'],
        {dataPlotDistance}
           
        
        ]);  

      var options = {{
        title: 'Distance of SRF02',
        curveType: 'function',
        pointSize: 2,
        hAxis: {{
          title: '# samples',
          viewWindow: {{
            max:100,
            min:0
          }}
        }},
        vAxis: {{
          title: 'Distance (cm)',
          viewWindow: {{
            max:200,
            min:0
          }}
        }},
        series: {{
          0: {{
            type: 'line',
            color:'blue'
          }}
        }},
        width: 450,
        height: 400,
        axes: {{
          x: {{
            0: {{
              side: 'center'
            }}
          }}
        }}
      }};

      var chart = new google.visualization.LineChart(document.getElementById('chart_1'));
      chart.draw(data, options);

    }}

    function drawBasic2() {{

    var data = google.visualization.arrayToDataTable([  
      ['frecuency', 'power'],
      {dataPlotFft}
      
      ]);  

    var options = {{
      title: 'FFT',
      legend: {{ position: 'none' }},
      colors: ['#4285F4'],
      bar: {{ gap: 0 }},
      hAxis: {{
        title: 'frecuency (Hz)',
        viewWindow: {{
          max:2.5,
          min:-2.5
        }},
      }},
      legend: {{ position: 'none' }},
      vAxis: {{
        title: 'Power (x10^6)',
        viewWindow: {{
          max:50,
          min:0
        }}
      }},
      width: 450,
      height: 400,
      bar: {{ groupWidth: "90%" }}
    }};

    var chart = new google.visualization.ColumnChart(document.getElementById('chart_2'));
    chart.draw(data, options);
    }}

  </script>
</head>
    <body class="text-center" onload="mueveReloj()">
    <!-- Barra de navegación  -->
    <nav class="navbar navbar-expand-md fixed-top bg-dark navbar-dark">
      <div class="container">
        <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbar2SupportedContent" aria-controls="navbar2SupportedContent" aria-expanded="false" aria-label="Toggle navigation" style=""> <span class="navbar-toggler-icon"></span> </button>
        <div class="collapse navbar-collapse justify-content-center" id="navbar2SupportedContent">
          <!-- Items de la barra de navegación -->
          <ul class="navbar-nav">
            <li class="nav-item mx-2">
              <a class="btn btn-dark btn-block mx-2 text-white btn-outline-light" href=#>Developer</a>
            </li>
            <li class="nav-item mx-2">
              <a class="btn btn-dark btn-block mx-2 text-white btn-outline-light" href=#>Update Page</a>
            </li>
            <li class="nav-item mx-2">
            </li>
            <li class="nav-item mx-2">
              <img class="img-fluid d-block" src="Frankfurt-University-logo.png" width="100" draggable="true">
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <!-- Portada con imagen de fondo -->
    <div class="d-flex align-items-center p-2 cover" style="background-image: url(&quot;frankfurt-university-fondo.jpg&quot;); background-position: left top; background-size: 100%; background-repeat: repeat;">
      <!-- Container con color negro difuminado -->
      <div class="container" style="	background-image: linear-gradient(to bottom, rgba(0,0,0,0.8), rgba(0,0,0,0.8));	background-position: top left;	background-size: 100%;	background-repeat: repeat;">
        <div class="row" style="">
          <div class="col-lg-12 text-white " style="">
            <br>
            <br>
            <h1 class="d-none d-md-block text-center text-capitalize text-light">
              <form name="form_reloj" class="mx-2">
                <b>Welcome, Date: </b><input class="mx-2" type="text" name="reloj" size="40" style="background-color : Black; color : White; font-family : Verdana, Arial, Helvetica; font-size : 20pt; text-align : center;" onfocus="window.document.form_reloj.reloj.blur()">
              </form>
            </h1>
            <div class="row">
              <div class="column text-white text-center">
                {estado}
              </div>
              <div class="column text-white" hidden>
                <h1 class="d-none d-md-block text-center text-capitalize text-light"hidden>
                  <b class="mx-2">Hi, No Presence </b>
                  <span class="blue">-</span>
                </h1>
              </div>
            </div>
            <div class="row">
              <div class="column mx-2">
                <div class="" id="chart_1" ></div>
              </div>
              <div class="column mx-2">
                <div class="" id="chart_2" ></div>
              </div>
              <br>
              <br>
              <h5 class="mx-2">By: Jhonatan N.</h5>
            </div>
          </div>
        </div>
      </div>
    </div>
    </body>
    </html>
  """.format(estado=estado, dataPlotDistance=plotDistance, dataPlotFft=plotFFT)
  f.write(message)
  f.close()

Wco = [[-1.24946691e-01 , 8.60093057e-01, -4.36390430e-01, 4.58717465e-01, 8.38625431e-01,  9.99379903e-02, -8.28555167e-01, -8.84512484e-01, -6.15577698e-01, -4.36659843e-01], 
 [-1.00126636e+00,  1.29429810e-02,  3.27845216e-01,  3.30699533e-02, 7.39647627e-01, -4.44685787e-01, -7.89498150e-01,  5.70201688e-02, 4.37375635e-01,  2.11906567e-01],
 [-6.89972341e-01,  5.46685696e-01,  9.97882038e-02,  6.32860247e-05, 9.11291122e-01,  4.99984503e-01,  1.10296249e-01,  9.42311168e-01, 3.30857456e-01,  3.03269655e-01],
 [ 2.50887066e-01,  9.76160288e-01,  1.28537074e-01,  2.57075101e-01, -5.75922392e-02,  9.45970714e-01,  7.01739788e-01, -7.15012074e-01, -5.99334061e-01, -4.98267472e-01],
 [ 2.92617500e-01, 7.53529668e-01,  7.88699508e-01,  2.19928801e-01, -6.23367548e-01,  3.14057291e-01,  3.96897286e-01,  1.04215586e+00, 4.23794866e-01,  5.92318833e-01],
 [ 9.47687626e-01, -7.03698695e-01, -7.27491617e-01, -5.09530544e-01, -7.04337060e-01,  1.88659027e-01,  6.05885029e-01,  7.42268562e-01, 1.20174855e-01, -5.39885402e-01],
 [-7.58450031e-02, -5.48458219e-01, -4.39585418e-01, -6.47698283e-01, -2.51858503e-01, -6.90831617e-02,  5.61683357e-01, -8.08860064e-01, -6.16460681e-01, -4.42636818e-01],
 [ 8.59229445e-01, -3.91088009e-01, -1.47157922e-01, -8.30634654e-01, -2.31161624e-01,  1.57954976e-01,  7.48963475e-01,  1.84328020e-01, 3.14275295e-01,  2.32919842e-01],
 [-9.19700041e-02,  1.04523087e+00,  1.06460400e-01, -8.48623753e-01, -6.19625032e-01, -2.96542406e-01,  9.06114817e-01, -8.56466770e-01, -4.63537753e-01, -9.93317127e-01],
 [ 8.19319129e-01,  1.01005189e-01, -7.29904711e-01,  4.10743028e-01, 5.37661277e-02,  7.71806896e-01, -8.41659188e-01, -4.46750462e-01, 8.84273410e-01, -5.55317760e-01],
 [ 9.78272974e-01,  7.06391484e-02, -9.28508401e-01, -6.13673687e-01, -1.58153117e-01, -2.45381370e-01,  3.61127369e-02, -6.15794897e-01, -8.94110799e-02,  3.13183010e-01],
 [ 3.91467959e-01, -2.34076574e-01,  8.14642429e-01,  1.57804877e-01, -6.15036845e-01, -8.34010124e-01, -6.65512741e-01,  5.84463263e-03, -5.83281457e-01, -1.02680576e+00],
 [-1.50776744e-01,  3.59568626e-01,  6.34340286e-01,  8.85935605e-01, -1.32685870e-01, -4.76035953e-01,  4.64369148e-01, -3.18390101e-01, -8.92286062e-01, -2.95460373e-01],
 [ 6.38227820e-01, -4.18500334e-01,  7.93808162e-01, -1.48603618e-02, -8.52705598e-01,  8.36544931e-01, -5.67131698e-01,  4.91172701e-01, -1.03806007e+00, -1.00328612e+00],
 [-6.97439490e-03, -2.73745716e-01,  3.08453012e-02,  9.07592177e-01, 3.29933256e-01, -7.48730183e-01,  6.86738491e-02, -6.34314060e-01, -5.75495422e-01,  4.52900052e-01],
 [ 4.24188763e-01, -3.34749311e-01, -3.40498775e-01,  3.50415021e-01, 7.84554064e-01, -7.83418953e-01, -1.97108567e-01,  2.04248875e-01, -4.55862790e-01, -4.70844626e-01],
 [-1.67058423e-01, -7.99675226e-01,  2.98557818e-01,  3.21959794e-01, 3.13195214e-02,  8.08900654e-01, 1.50122359e-01,  2.53060997e-01, 3.03022712e-01, -5.94672143e-01]] 
bco = [-0.384708, 0.00373114, -0.78191817, -0.2890262, 0.36225918, -0.34249282, -0.6613095, -0.4191356, -0.2806893, 0.28467086] 
Wco_2 = [[ 0.4714574,  -0.4327267,  -0.810854,   -0.8017435,  -0.16108488,  0.6215368, -0.6220325,  -0.41868195,  0.1671191, 0.11616104],
 [ 0.4173611,   0.9109013,   0.2129938,   0.1833222,  -0.85077137,  0.39316982, 1.0053159,  -0.33987477, -0.53023505, -0.56632113],
 [-1.059066,   -1.2682904,   1.0037901,  -0.08328351,  0.2122975,   0.04663752, -0.22311102,  0.6527881,  -0.85615087, -0.28509593],
 [-0.8955536,   0.17279916, -0.6615787,  -0.38319534, -0.77836657, -0.6395497, -0.73418224, -0.06949969,  0.2977006,   0.0301474 ],
 [ 0.9065493,  -0.11982234, -1.0118707,   0.26282597,  0.21532564, -0.15985866, -1.2022296,  -0.38235083, -0.28529996, -0.3987637 ],
 [-0.8839976,   0.02551503,  0.71504635, -0.34806198,  1.0425032,   0.7522061, -0.42747313,  0.78077096,  0.83245045,  0.2473539 ],
 [ 0.81118673, -0.7356287,   0.66726923, -0.3006252,   0.01804885, -0.09009663, -0.825151,   -0.03670776,  0.91025436 , 0.90416527],
 [ 0.61148286,  0.73690957,  0.47550514,  0.01745096, -0.3102192,   0.5811589, 0.64217794, -0.02123649, -0.41071165,  0.84951234],
 [ 0.5812521,   0.6991724,  -0.10828958,  0.0356148,   0.50834614,  0.3217858, 0.07095829, -1.0166068, -0.65996087, -0.47451803],
 [-0.16746055,  0.24903674, -0.74416786,  0.7547184,  -0.62839025,  0.3716488, -0.5250841,  -0.2392053,  -0.55701953, -0.27769873]] 
bco_2 = [ 0.04256948, -0.10216296,  0.611136, 0.26157552, -0.4998442,   0.20326701, -0.02061014,  0.38723573, -0.5643914,  -1.0227141 ] 
Wco_3 = [[-5.04608691e-01,  3.63526165e-01, -9.10683632e-01,  1.10216129e+00, 1.16413459e-01, -9.91211832e-01, -1.10844925e-01,  9.30097699e-01, -1.44994766e-01, -4.85064179e-01],
 [-9.84842062e-01, -9.07716990e-01,  6.86086416e-01,  1.11793065e+00, -6.94632053e-01,  4.10599917e-01, -9.30414721e-02, -8.41931045e-01, 8.90118301e-01,  9.78177249e-01],
 [ 9.60793078e-01,  1.82089716e-01,  1.04108989e-01, -8.08885098e-01, -5.38267493e-01, -5.94696701e-01, -5.58870375e-01,  7.15909302e-01, 6.19586743e-02, -5.41194916e-01],
 [-7.12508023e-01,  7.67725706e-01,  6.32931113e-01,  3.78185481e-01, 1.53868213e-01, -2.98726588e-01, -5.18205643e-01,  5.32494187e-01, 5.51973343e-01,  9.50927794e-01],
 [-3.69137675e-01, -5.73780656e-01,  8.30172420e-01,  6.33680403e-01, 2.96316236e-01, -9.72351581e-02,  7.68889964e-01,  3.18248302e-01, -4.18902427e-01,  1.23949975e-01],
 [-9.24432218e-01, -4.20616388e-01, -3.24329644e-01, -4.85032089e-02, 6.62635148e-01,  1.35567039e-02, -5.63625097e-01,  3.95206898e-01, -8.21871817e-01,  9.59660411e-01],
 [ 3.25922549e-01, -7.87519217e-01,  8.38285863e-01, -5.95653296e-01, -6.31323084e-02, -7.62114227e-01, -9.87534404e-01, -9.09103811e-01, 8.63932133e-01, -2.02593982e-01],
 [ 2.21849933e-01,  5.38490236e-01,  6.86291397e-01,  6.67211294e-01, -3.74878436e-01, -4.24146444e-01, -2.11325213e-01,  7.72132635e-01, -1.02504902e-03,  5.21984339e-01],
 [-8.90191078e-01, -5.98685086e-01,  8.51417422e-01,  2.73876309e-01, 1.62086442e-01, -6.39525533e-01, -1.87855765e-01, -8.40247750e-01, -1.58691064e-01, -3.28787893e-01],
 [-5.63164115e-01 , 1.78120330e-01, -7.59880424e-01, 1.35584518e-01, -9.10794258e-01,  9.28363979e-01, -7.16932654e-01, -7.04997301e-01, -4.62093681e-01, -2.92929441e-01]] 
bco_3 = [-0.24042441,  0.00259069,  0.5570704,   1.0780802,  -0.40850422,  0.6500614, -0.29480502,  0.9119066, 0.14689568, 0.06280377] 
Wcs = [[-0.71456206],
[-0.44386095],
 [-0.27763045],
 [ 1.9996402 ],
 [ 0.67272776],
 [-0.16227892],
 [ 1.1345643 ],
 [ 0.8823637 ],
 [ 0.63377666],
 [ 0.9413014 ]] 
bcs = [-0.23383798]

print("Iniciando ...")
PublicarApp(False,str(0),"[0,0],","[0,0],")
#Main program
while True:
  sensed,distance,mindistance,TimeElapse = s.getValues(10)
  rangeStats =  getStats(sensed, "distance")
  if(rangeStats["mean"] < 100):
    sensed,distance,mindistance,TimeElapse = s.getValues(100)
    rangeStats =  getStats(sensed, "distance")
    Input = [NormalizarDatos(rangeStats["min"],0), NormalizarDatos(rangeStats["max"],1),NormalizarDatos(rangeStats["mean"],2),NormalizarDatos(rangeStats["distanceDelta"],3),NormalizarDatos(Variance(distance),4),NormalizarDatos(St_des(distance),5),NormalizarDatos(Autocorrelation(distance),6),NormalizarDatos(Above_Threshold(distance),7),NormalizarDatos(Above_Median(distance),8),NormalizarDatos(Below_Threshold(distance),9),NormalizarDatos(Below_Median(distance),10),NormalizarDatos(Crossing_M(distance),11),NormalizarDatos(Sample_Entropy(distance),12),NormalizarDatos(Variation_Coef(distance),13),NormalizarDatos(Fft_energy(distance),14),NormalizarDatos(Fft_std(distance),15),NormalizarDatos(Fft_mean(distance),16)]
    Sco_1 = np.tanh(np.matmul(Input,Wco) + bco)
    Sco_2 = np.tanh(np.matmul(Sco_1,Wco_2) + bco_2)
    Sco_3 = np.tanh(np.matmul(Sco_2,Wco_3) + bco_3)
    Sr = np.matmul(Sco_3,Wcs) + bcs
    Sr = 1/(1 + np.exp(-Sr))
    print(Sr)
    if(Sr > 0.7):
      PublicarApp(True,str(Sr*100),StringDistance(distance),StringFft(FFt(distance)))
      now = datetime.now()
      dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
      print("Hola humano "+dt_string)
    else:
      PublicarApp(False,str(Sr*100),StringDistance(distance),StringFft(FFt(distance)))