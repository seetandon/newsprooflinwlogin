import React, { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { db } from "../firebase";
import liff from '@line/liff';
import "./App.css";


const Camera = () => {
  const videoRef = useRef(null);
  const photoRef = useRef(null);
  const stripRef = useRef(null);
  const [userId, setUserId] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [idToken, setIdToken] = useState("");
  let navigate = useNavigate();


  const initLine = () => {
    liff.init({ liffId: '1656553430-MzgGexx9' }, () => {
      if (liff.isLoggedIn()) {
        runApp();
      } else {
        liff.login();
      }
    }, err => console.error(err));
  }
  const runApp = () => {
    const idToken = liff.getIDToken();
    setIdToken(idToken);
    liff.getProfile().then(profile => {
      console.log(profile);
      setDisplayName(profile.displayName);
      setUserId(profile.userId);
    }).catch(err => console.error(err));
  }
  useEffect(() => {
    initLine();
  }, []);


  useEffect(() => {
    getVideo();
  }, [videoRef]);

  const getVideo = () => {
    navigator.mediaDevices
      .getUserMedia({ video: { width: 300 } })
      .then(stream => {
        let video = videoRef.current;
        video.srcObject = stream;
        video.play();
      })
      .catch(err => {
        console.error("error:", err);
      });
  };



  const takePhoto = () => {
    let photo = photoRef.current;
    let strip = stripRef.current;
    let video = videoRef.current;
    
    
    const width = 648;
    const height = 480;
    photo.width = width;
    photo.height = height;

    let ctx = photo.getContext("2d");
    ctx.drawImage(video, 0, 0, width, height);

    console.warn(strip);

    const data = photo.toDataURL("image/jpeg");
    const UserID = userId
    const Username = displayName

    console.warn(data);
    console.log("Data:", data)

    
    const a = document.createElement('a'); 
    a.href = data;
    strip.insertBefore(a, strip.firstChild);
    a.download = 'screenshot.jpg';
    
    document.getElementById('btn1').innerText = 'Pleas wait...';
    
    navigate("./Form")
    

  db.collection("Camera Data")
      .add({
        picturebase64: data,
        UserID: UserID,
        Username : Username,
      })
  };


  return (
    <div class = "Main">
      <p><b>Welcome!</b>{displayName}</p>
      <p><a>Please take your eye photo below</a></p>
      <h><video ref={videoRef} /></h>
      <c><button onClick={takePhoto} id="btn1">Take a photo</button></c>
      <canvas ref={photoRef} />
      <div>
        <div ref={stripRef} />
      </div>
    </div>
  );
};

export default Camera;