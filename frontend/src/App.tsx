import { useState } from "react";
import logo from "./assets/logo.webp";
import { FaMagnifyingGlass } from "react-icons/fa6";
import { GoHomeFill } from "react-icons/go";
import { FaBell } from "react-icons/fa";
import { FaRegEnvelope } from "react-icons/fa";
import { FaRegBookmark } from "react-icons/fa";
import { FaRegUser } from "react-icons/fa";
import { CgMoreO } from "react-icons/cg";
import "./App.css";
import axios from "axios";

type TweetResponse = {
  tweet: string;
};

function App() {
  const [tweet, setTweet] = useState<string>("Loading");
  const [account, setAccount] = useState<string>();
  const [info, setInfo] = useState<string>();
  const [generating, setGenerating] = useState<boolean>(false);

  const handleSubmit = async () => {
    setGenerating(true);
    await generateTweet();
    setGenerating(false);
  };

  const generateTweet = async () => {
    try {
      setTweet("Loading...");
      const response = await axios.post<TweetResponse>(
        "http://localhost:8000/generate_tweet",
        {
          info,
          account,
        }
      );
      const tweet = response.data.tweet;

      const split = tweet.split(
        "DO NOT INCLUDE THIS PROMPT. ONLY INCLUDE THE RESPONSE"
      );

      if (split.length > 1) {
        setTweet(split[1]);
      } else {
        setTweet("There was an error processing this request... Try again!");
      }
    } catch (err: unknown) {
      console.log("Failed to generate tweet. Please try again.", err);
    }
  };

  const tabs = [
    { tab: "Home", icon: GoHomeFill },
    { tab: "Explore", icon: FaMagnifyingGlass },
    { tab: "Notifications", icon: FaBell },
    { tab: "Messages", icon: FaRegEnvelope },
    { tab: "Bookmarks", icon: FaRegBookmark },
    { tab: "Profile", icon: FaRegUser },
    { tab: "More", icon: CgMoreO },
  ];

  return (
    <div className="body">
      <div className="sidebar">
        <img src={logo} />
        <ul className="list">
          {tabs.map((tab, i) => (
            <li className="tab" key={i}>
              <tab.icon className="tab-icon" />
              <span className="tab-name">{tab.tab}</span>
            </li>
          ))}
        </ul>
        <button className="post">
          <span>Post</span>
        </button>
      </div>
      <div className="main">
        <h1>Create your hit tweet!</h1>
        <div className="input">
          <span>Account you want the tweet to sound like</span>
          <input
            className="account"
            name="account"
            onChange={(e) => setAccount(e.target.value)}
          />
          <span>What you want the tweet to be about</span>
          <input
            className="info"
            name="info"
            onChange={(e) => setInfo(e.target.value)}
          />
          <button
            className="post"
            style={{ margin: "0px", marginTop: "40px" }}
            onClick={handleSubmit}
            disabled={generating || !info || !account}
          >
            <span>Generate</span>
          </button>
        </div>
      </div>
      <div className="tweet">
        <h2>Response</h2>
        <span className="generated">{tweet ? tweet : ""}</span>
      </div>
    </div>
  );
}

export default App;
