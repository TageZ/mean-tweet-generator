import { useState } from 'react'
import logo from './assets/logo.webp'
import { FaMagnifyingGlass } from "react-icons/fa6";
import { GoHomeFill } from "react-icons/go";
import { FaBell } from "react-icons/fa";
import { FaRegEnvelope } from "react-icons/fa";
import { FaRegBookmark } from "react-icons/fa";
import { FaRegUser } from "react-icons/fa";
import { CgMoreO } from "react-icons/cg";
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const tabs = [
    {tab: "Home", icon: GoHomeFill}, 
    {tab: "Explore", icon: FaMagnifyingGlass}, 
    {tab: "Notifications", icon: FaBell},
    {tab: "Messages", icon: FaRegEnvelope},
    {tab: "Bookmarks", icon: FaRegBookmark},
    {tab: "Profile", icon: FaRegUser},
    {tab: "More", icon: CgMoreO}
  ]

  return (
    <div className="body">
      <div className="sidebar">
        <img src={logo}/>
        <ul className="list">
          {tabs.map((tab, i) => (
            <li className="tab" key={i}>
              <tab.icon className='tab-icon'/>
              <span className='tab-name'>{tab.tab}</span>
            </li>
          ))}
        </ul>
        <button className='post'><span>Post</span></button>
      </div>
      <div className="main">
        <h1>Create your tweet!</h1>
        <div className='input'>
          <span>Account you want the tweet to sound like</span>
          <span>What you want the tweet to be about</span>
          <button className='post' 
            style={{margin: '0px'}}
          >
            <span>Generate</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default App