import { useState } from "react";
import sidebar from "./assets/d398b495e8864660aba62a6fa0dd0c82.webp";
import main from "./assets/Screenshot 2024-12-08 235305 (1).png";
import tweet_sub from "./assets/822bbbb8c4674bd5a777c9f995d9cdea.webp";
import { FaUserCircle } from "react-icons/fa";
import "./App.css";
import axios from "axios";

type TweetResponse = {
  tweet: string;
};

function App() {
  const [tweet, setTweet] = useState<string>("Loading");
  const [genre, setGenre] = useState<string>();
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
          genre,
        }
      );
      const tweet = response.data.tweet;

      setTweet(tweet)
    } catch (err: unknown) {
      console.log("Failed to generate tweet. Please try again.", err);
    }
  };

  return (
    <div className="body">
      <div className="sidebar">
        <img className="sidebar-img" src={sidebar} />
      </div>
      <div className="main">
        <h1>Create your hit tweet!</h1>
        <div className="tweet-input">
          <div className="img-input">
            <FaUserCircle size={40} />
            <input
              onChange={(e) => setGenre(e.target.value)}
              className="tweet-genre"
              placeholder="What genre do you want your tweet to fall under?"
            />
          </div>
          <div className="img-input">
            <FaUserCircle size={40} />
            <input
            onChange={(e) => setInfo(e.target.value)}
              className="tweet-genre"
              placeholder="What should the tweet be about? "
            />
          </div>
          <button
            className="post"
            style={{ margin: "0px", marginTop: "40px" }}
            onClick={handleSubmit}
            disabled={generating || !info || !genre}
          >            
            <span>Post</span>
          </button>
          <img className="tweet-sub" src={tweet_sub} />
        </div>
        <div className="main">
          <img className="main-img" src={main} />
        </div>
      </div>
      <div className="tweet">
        <h1>Response</h1>
        <span className="generated">{tweet ? tweet : ""}</span>
      </div>
    </div>
  );
}

export default App;
