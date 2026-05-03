document.addEventListener("DOMContentLoaded", () => {
  
  const video = document.getElementById('video');
  const play = document.getElementById('play');
  const forward = document.getElementById('forward');
  const backward = document.getElementById('backward');
  const control_overlay = document.getElementById('control-overlay');
  const video_progress = document.getElementById('video-progress-bar');
  const time = document.getElementById('time');
  
  // Immediately play the video
  video.play();
  
  // play event ✅
  play.addEventListener("click", () => {
    // Pause and Play Video with a click 
    if (video.paused) {
      video.play();
      play.textContent = "⏸️";
    } else {
      video.pause();
      play.textContent = "▶️";
    };
  });
  
  // video clicking event 
  video.addEventListener("click", () => {
    video_progress.classList.toggle('hidden');
    time.classList.toggle('hidden');
    control_overlay.classList.toggle('hidden');
  });
  
  // Forward Video by 10(s) ✅
  forward.addEventListener("dblclick", () => {
    video.currentTime = Math.min(video.duration, video.currentTime + 10);
  });
  
  // Backward Video by 10(s) ✅
  backward.addEventListener("dblclick", () => {
    video.currentTime = Math.max(0, video.currentTime - 10);
  });
  
  
  // When page is loaded ✅
  video.addEventListener("loadedmetadata", () => {
    video_progress.max = video.duration;
    video_progress.value = 0;
  });

  // show the time update ✅
  video.addEventListener("timeupdate", () => {
    
    video_progress.value = video.currentTime;
    video_progress.max = video.duration;
    
    const current = video.currentTime;
    const duration = video.duration;
    // Current Time
    const curMin = Math.floor(current / 60);
    const curSec = Math.floor(current % 60);
    // Duration 
    const durMin = Math.floor(duration / 60);
    const durSec = Math.floor(duration % 60);
    // Formatted
    const currentTimeFormatted = `0${curMin}:${curSec.toString().padStart(2, "0")}`;
    const durationFormatted = `0${durMin}:${durSec.toString().padStart(2, "0")}`;
    
    time.textContent = `${currentTimeFormatted} / ${durationFormatted}`;
  });
  
  // Control video current time using the range input ✅
  video_progress.addEventListener("input", () => {
    video.currentTime = Number(video_progress.value);
  });
  
  // when the video end ✅
  video.addEventListener("ended", () => {
    video_progress.value = 0;
    control_overlay.classList.remove('hidden');
    time.classList.remove('hidden');
    video_progress.classList.remove('hidden');
  });
  
});