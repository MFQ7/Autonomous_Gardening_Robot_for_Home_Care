const firebaseConfig = {
    apiKey: "AIzaSyAeKB3BtG6AHbQ0KymGHuhjJbVCHadxv28",
    authDomain: "plantcare-5de83.firebaseapp.com",
    databaseURL: "https://plantcare-5de83-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "plantcare-5de83",
    storageBucket: "plantcare-5de83.appspot.com",
    messagingSenderId: "346549534845",
    appId: "1:346549534845:web:6f37e1d27d528d4e19b114"
};

firebase.initializeApp(firebaseConfig);

const predictionsRef = firebase.database().ref('predictions');

function displayData(snapshot) {
    const tableBody = document.getElementById('predictionsTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';

    snapshot.forEach(childSnapshot => {
        const data = childSnapshot.val();
        const row = `
            <tr>
                <td>${data.position}</td>
                <td>${data.prediction}</td>
                <td>${data.moisture}</td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });
}
predictionsRef.on('value', displayData, error => {
    console.error("Error fetching data from Firebase:", error);
});
function displayLastUpdate(snapshot) {
    const updateElement = document.getElementById('lastUpdateTime');
    if (snapshot.exists() && snapshot.val().time) {
        const lastUpdateTime = snapshot.val().time;  // Accessing the 'time' child
        updateElement.textContent = `Last Update: ${lastUpdateTime}`;
    } else {
        updateElement.textContent = "Last Update: --";
        console.log("No 'time' data or 'date' node does not exist.");
    }
}

const dateRef = firebase.database().ref('date');
dateRef.on('value', displayLastUpdate, error => {
    console.error("Error fetching last update time from Firebase:", error);
});
