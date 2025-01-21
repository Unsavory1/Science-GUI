import React from 'react'
import Sensor from './Sensor'

const Soil = ({ data }) => {
  return (
    <div className='soil'>
      <div className='subheader'>Soil Probe</div>
      {data.soil_probe && (
        <>
          <Sensor id='soil-temp' name='Temperature' value={data.soil_probe.temperature} unit='°C' />
          <Sensor id='soil-moisture' name='Moisture' value={data.soil_probe.moisture} unit='%' />
          <Sensor id='soil-ph' name='pH Value' value={data.soil_probe.ph_value} unit='' />
        </>
      )}
    </div>
  )
}

export default Soil
