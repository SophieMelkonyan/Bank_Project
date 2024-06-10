let correctPin = "1234";

let btns = document.getElementsByClassName("pinpad-btn");
let pinInput = document.getElementById("pinpad-input");

for (let i = 0; i < btns.length; i++) {
    let btn = btns.item(i);
    if (btn.id && (btn.id === "submit-btn" || btn.id === "delete-btn"))
        continue;

    // Add onclick event listener to every button from 0 - 9
    btn.addEventListener("click", (e) => {
        // Check if the PIN input value is empty before appending
        if (pinInput.value === "") {
            pinInput.value = e.target.value;
        } else {
            pinInput.value += e.target.value;
        }
    });
}

let submitBtn = document.getElementById("submit-btn");
let delBtn = document.getElementById("delete-btn");
let modal = document.getElementById("modal");
let result = document.getElementById("result");
let closeBtn = document.getElementById("close");

delBtn.addEventListener("click", () => {
    if (pinInput.value)
        pinInput.value = pinInput.value.substr(0, pinInput.value.length - 1);
});



// Function to reset PIN input to "0"
function resetPinInput() {
    pinInput.value = "0";
}

// Reset PIN input to "0" when modal is displayed
modal.addEventListener("displayed", resetPinInput);