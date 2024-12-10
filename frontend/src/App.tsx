import { useState } from "react";
import sidebar from "./assets/d398b495e8864660aba62a6fa0dd0c82.webp";
import main from "./assets/main.png";
import { FaUserCircle } from "react-icons/fa";
import "./App.css";
import axios from "axios";
import verified from "./assets/Twitter_Verified_Badge.svg.png";

type TweetResponse = {
  tweet: string;
};

function App() {
  const [tweet, setTweet] = useState<string>("");
  const [prompt, setPrompt] = useState<string>();
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
          prompt,
        }
      );
      const tweet = response.data.tweet;

      setTweet(tweet);
    } catch (err: unknown) {
      console.log("Failed to generate tweet. Please try again.", err);
    }
  };

  return (
    <div className="container">
      <div className="cell" style={{ gridRow: "1/3", gridColumn: "1/2" }}>
        <img className="sidebar-img" src={sidebar} />
      </div>
      <div className="cell" style={{ gridRow: "3/4", gridColumn: "1/2" }}></div>
      <div className="cell" style={{ gridRow: "1/2", gridColumn: "2/3" }}>
        <h2>Create your hit tweet!</h2>
        <div className="tweet-input">
          <div className="img-input">
            <FaUserCircle size={40} />
            <input
              onChange={(e) => setPrompt(e.target.value)}
              className="tweet-genre"
              placeholder="What should the tweet be about? "
            />
          </div>
          <button
            className="post"
            onClick={handleSubmit}
            disabled={generating || !prompt}
          >
            <span>Post</span>
          </button>
        </div>
      </div>
      <div className="cell" style={{ gridRow: "2/3", gridColumn: "2/3" }}>
        <div className="main">
          <img className="main-img" src={main} />
        </div>
      </div>
      <div className="cell" style={{ gridRow: "3/4", gridColumn: "2/3" }}></div>
      <div
        className="cell response-cell"
        style={{ gridRow: "1/3", gridColumn: "3/4" }}
      >
        {tweet && (
          <>
            <h2>Response</h2>{" "}
            <div className="tweet-profile">
              <FaUserCircle size={40} />
              <span>Twitter_User</span>{" "}
              <span className="tweet-profile-name">
                @User <img className="verified" src={verified} />{" "}
              </span>{" "}
            </div>{" "}
            <div className="generated">
              {generating ? (
                <span className="loader"></span>
              ) : (
                tweet.split("\n").map((l) => <p>{l}</p>)
              )}{" "}
            </div>
          </>
        )}
      </div>
      <div className="cell" style={{ gridRow: "3/4", gridColumn: "3/4" }}></div>
    </div>
  );
}

export default App;
