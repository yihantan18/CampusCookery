document.addEventListener("DOMContentLoaded", function () {
    const editButton = document.getElementById("edit-profile-button");
    const formInputs = document.querySelectorAll(".profile-form input");

    editButton.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent default form submission

        const isDisabled = formInputs[0].disabled;
        formInputs.forEach(input => {
            if (isDisabled) {
                input.disabled = false;
                input.classList.add("editable"); // Add styling for editable state
            } else {
                input.disabled = true;
                input.classList.remove("editable"); // Remove styling
            }
        });

        editButton.textContent = isDisabled ? "Save" : "Edit";

        // If the button is "Save", enable form submission
        if (!isDisabled) {
            editButton.setAttribute("type", "submit");
        } else {
            editButton.setAttribute("type", "button");
        }
    });
});
