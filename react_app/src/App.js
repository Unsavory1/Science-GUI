import './App.css';
import { useEffect, useState, useRef } from 'react';
import io from 'socket.io-client';
import Chart from 'chart.js/auto';
import Image from './components/Image';
import logo from './MRM_logo.png';
import sm from './sm.jpeg';
import Ze03 from './components/Ze03';
import Sgp from './components/Sgp';
import Bme from './components/Bme';
import Soil from './components/Soil';
import Sensor from './components/Sensor';

function SensorDashboard() {
  const [view, setView] = useState('dashboard'); // State to toggle views
  const [sensorData, setSensorData] = useState({
    ze03: { co: 0 },
    gps: { lat: 0, lon: 0},
    flurometer: { red: 0, green: 0,blue: 0 },
    bme688: { temperature: 0, pressure: 0, humidity: 0 },
    mq4: { methane: 0 },
    sgp30: { tvoc: 0, co2: 0 },
    soil_probe: { soil_temperature: 0, soil_moisture: 0},
    as726x: { s1: 0, s2: 0, s3: 0, s4: 0, s5: 0, s6: 0 },
    tsl2591: { RadiationIntensity: 0 },
    MQ135: { Benzene: 0},
  });

  const chartRef = useRef(null); // Reference for the canvas element
  const [sensorChart, setSensorChart] = useState(null);

  useEffect(() => {
    const socket = io.connect("http://192.168.234.121:5000");
    socket.on('connect', () => {
      console.log('Connected to WebSocket server');
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server');
    });

    socket.on('sensor_data', (data) => {
      setSensorData((prevData) => ({
        ...prevData,
        ...data,
      }));
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  useEffect(() => {
    if (view === 'dashboard' && chartRef.current) {
      const ctx = chartRef.current.getContext('2d');

      if (sensorChart) {
        sensorChart.destroy();
      }

      const newChart = new Chart(ctx, {
        type: 'bar',
        options: {
          legend: { display: false },
          scales: { y: { beginAtZero: true, max: 9000 } },
        },
        data: {
          labels: Object.keys(sensorData.as726x || {}),
          datasets: [
            {
              label: 'AS726x Sensor Data',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1,
              data: Object.values(sensorData.as726x || []),
            },
          ],
        },
      });

      setSensorChart(newChart);

      return () => {
        if (newChart) {
          newChart.destroy();
        }
      };
    }
  }, [view, sensorData.as726x]);

  if (view === 'camera-only') {
    return (
      <span className='camerapage'>
        <div>
          <button className='switch' onClick={() =>setView('dashboard')}>
            Switch to Daskboard
          </button>
          <div className="cameraonly">
            <div className="camsubheader">Camera View</div>
            <div className="video-container">
              <img
                src="http://192.168.234.121:5000/video1"
                alt="Video 1"
                style={{ width: '50%', height: '100%' }}
              />
              <img
                src="http://192.168.234.121:5000/video2"
                alt="Video 2"
                style={{ width: '50%', height: '100%' }}
              />
            </div>
          </div>
        </div>
      </span>
    );
  }
  else{
  
    return (
      <div>
        <span className="left">
          <Image
            title="37th URC lesgooo"
            src={logo}
            style={{ width: '30%', position: 'relative', top: '3%', left: '5%' }}
          />
          <div title="7th ERC lesgooo" className="header">Science GUI</div>
          <Ze03 title="Where is NH3? Where is H2S? Where is NO2? Where is SO2? Where is Cl2?" sensorData={sensorData} />
          <div className="gps">
            <div className="subheader">GPS</div>
            {sensorData.gps && (
              <>
                <Sensor id="lat" name="Latitude" value={sensorData.gps.lat} unit="°" />
                <Sensor id="lon" name="Longitude" value={sensorData.gps.lon} unit="°" />
              </>
            )}
          </div>
          <Image
            title="Anky@9798"
            src={sm}
            style={{
              width: '80%',
              position: 'relative',
              top: '-15%',
              left: '10%',
              borderRadius: 50,
            }}
          />
          <button className="switch" onClick={() => {
              console.log('Switching to: camera'); 
              setView('camera-only');
              }}>          
            Switch to Camera View
          </button>
        </span>

        <span className="right">
          <Sgp data={sensorData} />
          <div title={"Nikhilesh"} className='camera'>
            <div className='subheader'>Cameras</div>
            <div className='video-container'>
              <img
                src='http://192.168.234.121:5000/video1'
                alt='Video 1'
                style={{ width: '50%', height: '300px' }}
              />
              <img
                src='http://192.168.234.121:5000/video2'
                alt='Video 2'
                style={{ width: '50%', height: '300px' }}
              />
            </div>
          </div>
          <Bme data={sensorData} />
          <Soil data={sensorData} />
          <div className="spectral">
            <div className="subheader">AS7626x</div>
            <canvas id="sensorChart" ref={chartRef} width="400" height="170"></canvas>
          </div>

          {sensorData.flurometer && (
            <div className="flu">
              <div className="subheader">Flurometer</div>
              <Sensor id="red" name="Red" value={sensorData.flurometer.red} unit=" " />
              <Sensor id="green" name="Green" value={sensorData.flurometer.green} unit=" " />
              <Sensor id="blue" name="Blue" value={sensorData.flurometer.blue} unit=" " />
            </div>
          )}

          <div className="tsl2591">
            <div className="subheader">TSL2591</div>
            <Sensor id="radiationintensity" name="Radiation Intensity" value={sensorData.tsl2591.RadiationIntensity} unit="lux" />
          </div>
          <div className="mq135">
            <div className="subheader">MQ135</div>
            <Sensor id="benzene" name="Benzene" value={sensorData.MQ135.Benzene} unit="ppm" />
            <Sensor id="sulphur" name="Sulphur" value={sensorData.MQ135.Sulphur} unit="ppm" />
            <Sensor id="ammonia" name="Ammonia" value={sensorData.MQ135.Ammonia} unit="ppm" />
          </div>
        </span>
      </div>
    );
  }
}

export default SensorDashboard;
