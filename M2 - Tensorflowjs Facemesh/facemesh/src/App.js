import React from 'react'

import logo from './logo.svg';
import './App.css';

const faceLandmarksDetection = require('@tensorflow-models/face-landmarks-detection');
require('@tensorflow/tfjs-backend-webgl');

const WIDTH = 1280
const HEIGHT = 720

class App extends React.Component {
  componentDidMount() {
    this.loadFacemesh()
  }

  canvasRef = React.createRef();

  async loadFacemesh() {
    this.model = await faceLandmarksDetection.load(faceLandmarksDetection.SupportedPackages.mediapipeFacemesh);
    console.log(this.model)

    this.video = document.querySelector("video")

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      throw new Error('Browser API navigator.mediaDevices.getUserMedia not available')
    }

    this.stream = await navigator.mediaDevices.getUserMedia({
      audio: false,
      video: {
        facingMode: 'user',
        width: { ideal: 640 },
        height: { ideal: 360 },
        aspectRatio: { exact: 16.0 / 9.0 },
      }
    })

    this.video.srcObject = this.stream
    this.video.onloadedmetadata = async () => {
      console.log(this.stream)
      if (this.stream) {
        await this.video.play()
        requestAnimationFrame(() => this.predict(this.model, this.video))
      }
    }
  }

  async predict() {
    console.log(this.video)
    const predictions = await this.model.estimateFaces({
      input: this.video
    });
    console.log(predictions)

    if (predictions.length > 0) {
      /*
      `predictions` is an array of objects describing each detected face, for example:

      [
        {
          faceInViewConfidence: 1, // The probability of a face being present.
          boundingBox: { // The bounding box surrounding the face.
            topLeft: [232.28, 145.26],
            bottomRight: [449.75, 308.36],
          },
          mesh: [ // The 3D coordinates of each facial landmark.
            [92.07, 119.49, -17.54],
            [91.97, 102.52, -30.54],
            ...
          ],
          scaledMesh: [ // The 3D coordinates of each facial landmark, normalized.
            [322.32, 297.58, -17.54],
            [322.18, 263.95, -30.54]
          ],
          annotations: { // Semantic groupings of the `scaledMesh` coordinates.
            silhouette: [
              [326.19, 124.72, -3.82],
              [351.06, 126.30, -3.00],
              ...
            ],
            ...
          }
        }
      ]
      */
      console.log(this.canvasRef.current)
      const canvas = this.canvasRef.current

      if (!canvas) {
        console.log("!canvas")
        return requestAnimationFrame(() => this.predict())
      }

      const ctx = canvas.getContext('2d')
      ctx.clearRect(0, 0, WIDTH, HEIGHT)
      for (let i = 0; i < predictions.length; i++) {
      
        const keypoints = predictions[i].mesh;
        this.drawFace(ctx, keypoints)
      }
      
      return requestAnimationFrame(() => this.predict())
    }
  }

  drawFace(ctx, scaledMesh) {  
    // Log facial keypoints.
    for (let i = 0; i < scaledMesh.length; i++) {
      const [x, y, z] = scaledMesh[i];

      // console.log(`Keypoint ${i}: [${x}, ${y}, ${z}]`);
      this.drawPoint(ctx, x, y, z)
    }
  }

  drawPoint(context, x, y, z) {
    // console.log(x,y)
    context.save()
    context.fillStyle = `rgba(255,255,255, 0.5)`
    context.beginPath()
    context.arc(x, y, 2, 0, 2 * Math.PI)
    context.fill()
    context.restore()
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <div style={{
              display: 'flex',
              justifyContent: 'center',
              width: WIDTH,
              height: HEIGHT,
          }}>
            <video style={{
              width: WIDTH,
              height: HEIGHT,
              position: 'absolute',
            }}></video>
            <canvas ref={this.canvasRef} style={{
              width: WIDTH,
              height: HEIGHT,
              position: 'absolute',
              zIndex: 10
              }} />
          </div>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
      </div>
    );
  }
}

export default App;