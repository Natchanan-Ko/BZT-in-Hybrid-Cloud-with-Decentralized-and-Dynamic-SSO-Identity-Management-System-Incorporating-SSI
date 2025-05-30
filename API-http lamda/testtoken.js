const readline = require('readline');
const { spawn } = require('child_process');

// ✅ Replace this with your deployed Lambda endpoint
const lambdaEndpoint = 'https://ugrw5apgfh.execute-api.ap-southeast-2.amazonaws.com/verifytk';

// 🔄 Setup readline interface for CLI input
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// 🔧 Helper to ask question and return promise
function promptUser(question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer);
    });
  });
}

// 🚀 Main logic to get input and send to Lambda
async function main() {
  try {
    const token = await promptUser("🔐 Please enter your token: ");
    const patient = await promptUser("👤 Please enter the patient name: ");

    const payload = {
      token,
      patient
    };

    const curl = spawn('curl', [
      '-X', 'POST',
      lambdaEndpoint,
      '-H', 'Content-Type: application/json',
      '-d', JSON.stringify(payload)
    ]);

    let output = '';
    let errorOutput = '';

    curl.stdout.on('data', (data) => {
      output += data.toString();
    });

    curl.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });

    curl.on('close', (code) => {
      rl.close(); // Always close readline

      if (code === 0) {
        try {
          const response = JSON.parse(output);
          console.log("✅ User Verification Response:");
          console.log(JSON.stringify(response, null, 2));
        } catch (err) {
          console.error("❌ Failed to parse Lambda response:", err);
        }
      } else {
        console.error(`❌ Error executing cURL command: ${errorOutput}`);
      }
    });

  } catch (err) {
    console.error("❌ Unexpected error:", err);
    rl.close();
  }
}

main();
