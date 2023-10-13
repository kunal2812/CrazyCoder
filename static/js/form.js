document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signup-form");
    const signinForm = document.getElementById("signin-form");
    const signupLink = document.getElementById("signup-link");
    const signinLink = document.getElementById("signin-link");
    const heading = document.getElementById("form-heading");
    signupForm.style.display = "block"; // Initially display signup form
    signinForm.style.display = "none"; // Initially hide signin form
    signupLink.addEventListener("click", (e) => {
      e.preventDefault();
      heading.textContent = "Sign Up On Youdemy";
      signupForm.style.display = "block";
      signinForm.style.display = "none";
    });
  
    signinLink.addEventListener("click", (e) => {
      e.preventDefault();
      heading.textContent = "Sign In On Youdemy";
      signinForm.style.display = "block";
      signupForm.style.display = "none";
    });
  });