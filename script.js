document.addEventListener("DOMContentLoaded", function () {
    const submitButton = document.getElementById("submitButton");

    submitButton.addEventListener("click", function () {
        const provider = document.getElementById("provDP").value;
        const consumer = document.getElementById("consDP").value;

        // Call the Python script using command-line execution
        const command = `getDcSpec.py ${provider} ${consumer}`;
        const { exec } = require("child_process");

        exec(command, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error: ${error.message}`);
                return;
            }
            console.log(`stdout: ${stdout}`);
            console.error(`stderr: ${stderr}`);
        });
    });
});
