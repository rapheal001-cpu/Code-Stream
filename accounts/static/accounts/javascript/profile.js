// Mobile 
const mobileProfile = document.querySelector(".mobile-profile");
const mobileProfileOptions =
document.querySelector(".mobile-profile-options");

// Desktop 
const desktopProfile = document.querySelector(".desktop-profile");
const desktopProfileOptions =
document.querySelector(".desktop-profile-options");

// Mobile 
mobileProfile.addEventListener("click", (e) => {
  e.stopPropagation();
  mobileProfileOptions.classList.toggle('hidden');
});
document.addEventListener("click", (e) => {
  if (!mobileProfile.contains(e.target) &&
  !mobileProfileOptions.contains(e.target)) {
    mobileProfileOptions.classList.add('hidden');
  }
});

// Desktop 
desktopProfile.addEventListener("click", (e) => {
  e.stopPropagation();
  desktopProfileOptions.classList.toggle('hidden');
});
document.addEventListener("click", (e) => {
  if (!desktopProfile.contains(e.target) &&
  !desktopProfileOptions.contains(e.target)) {
    desktopProfileOptions.classList.add('hidden');
  }
});