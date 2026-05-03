document.addEventListener("DOMContentLoaded", () => {
  
  const videos = document.querySelectorAll(".videos");
  
  videos.forEach((video) => {
    
    if (video.paused) {
      video.currentTime = Math.floor(video.currentTime + 0.1);
    }
    
    video.addEventListener('mouseover', () => {
      video.play();
    });
    
    video.addEventListener('mouseout', () => {
      video.pause();
      video.currentTime = Math.floor(video.currentTime + 0.1);
    });
    
  });
  
});