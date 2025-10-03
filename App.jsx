
import React from 'react'
import ReactorDesigner from './components/ReactorDesigner'
import Dashboard from './components/Dashboard'

export default function App(){
  return (
    <div className="p-4 grid grid-cols-3 gap-4">
      <div className="col-span-1"><ReactorDesigner/></div>
      <div className="col-span-2"><Dashboard/></div>
    </div>
  )
}
