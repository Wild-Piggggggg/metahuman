<template>
    <div>
      <h2>人脸识别摄像头</h2>
      <img :src="videoUrl" alt="视频流" style="width: 640px;" />
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        videoUrl: 'http://localhost:5000/video_feed'
      };
    }
  };
  </script>