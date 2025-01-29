import React from 'react'
import Sensor from './Sensor'

const Soil = ({ data }) => {
  return (
    <div className='soil'>
      <div className='subheader'>Soil Probe</div>
      {data.soil_probe && (
        <>
          <Sensor id='soil-temp' name='Soil_Temperature' value={data.soil_probe.soil_temperature} unit='°C' />
          <Sensor id='soil-moisture' name='Soil_Moisture' value={data.soil_probe.soil_moisture} unit='%' />
        </>
      )}
    </div>
  )
}

export default Soil
