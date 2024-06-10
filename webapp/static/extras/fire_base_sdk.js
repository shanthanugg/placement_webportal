  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
  import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-analytics.js";
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyCcG9zS8hJBVQ-c5budSk8QAjSOdMLdJ18",
    authDomain: "placement-web-portal-c3159.firebaseapp.com",
    databaseURL: "https://placement-web-portal-c3159-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "placement-web-portal-c3159",
    storageBucket: "placement-web-portal-c3159.appspot.com",
    messagingSenderId: "450583188029",
    appId: "1:450583188029:web:cf219ec7241ad3c42e5054",
    measurementId: "G-WDB891ZN5Q"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const analytics = getAnalytics(app);
