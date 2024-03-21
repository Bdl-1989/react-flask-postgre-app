import axios from 'axios'
import React, { useEffect, useState } from 'react'

export const Home = () => {
  const [content, setContent] = useState('')
  useEffect(() => {
    
    (
      async ()=>{
        const {data} = await axios.get('/auth/whoami')
        console.log(data)
        setContent(JSON.stringify(data['claims']))
      }
    )();
  }, [])
  


  return (
    <div>{content}</div>
  )
}
