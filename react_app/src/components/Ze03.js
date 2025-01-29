import React from 'react'
import Sensor from './Sensor'

const Ze03 = ({ title, sensorData }) => {
  return (
    <div title={title} className='ze03'>
      <div className='subheader'>ZE03</div>
      <Sensor id='zeCO' name='CO' value={sensorData.ze03.co} unit='ppm' />
    </div>
  )
}

export default Ze03
