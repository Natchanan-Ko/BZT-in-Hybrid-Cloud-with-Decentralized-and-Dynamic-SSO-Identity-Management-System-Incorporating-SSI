const { spawn } = require('child_process');
const fs = require('fs');
const readline = require('readline');
const os = require('os');
const axios = require('axios');

// Function to extract JSON blocks
function extractJsonBlocksByBrace(input) {
  const blocks = [];
  let braceStack = [];
  let start = null
  for (let i = 0; i < input.length; i++) {
    if (input[i] === '{') {
      if (braceStack.length === 0) start = i;
      braceStack.push('{');
    } else if (input[i] === '}') {
      braceStack.pop();
      if (braceStack.length === 0 && start !== null) {
        const jsonBlock = input.slice(start, i + 1);
        try {
          blocks.push(JSON.parse(jsonBlock));
        } catch (err) {
          console.warn("Invalid JSON block skipped:", err.message);
        }
        start = null;
      }
    }
  }
  return blocks;
}

// Function to prompt the user for input
function promptUser(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}

// Function to collect user information
async function collectUserInfo() {
  try {
    const ipResponse = await axios.get('https://api.ipify.org?format=json');
    const ipAddress = ipResponse.data.ip;

    const locationResponse = await axios.get(`https://ipinfo.io/${ipAddress}/json`);
    const location = locationResponse.data.city + ', ' + locationResponse.data.region + ', ' + locationResponse.data.country;

    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    const userAgent = process.env.USER_AGENT || 'Unknown';

    const deviceID = `${os.hostname()}-${Math.random().toString(36).substr(2, 9)}`;

    return {
      ipAddress,
      location,
      timezone,
      userAgent,
      deviceID
    };
  } catch (error) {
    console.error('Error collecting user information:', error.message);
  }
}

// Function to send data to Lambda via cURL
function sendToLambda(data) {
  const lambdaEndpoint = 'https://ugrw5apgfh.execute-api.ap-southeast-2.amazonaws.com/extract'; // Replace with your actual API Gateway endpoint

  // Ensure data is an array (even if it's a single object)
  if (!Array.isArray(data)) {
    data = [data];
  }

  const curlCommand = `curl -X POST "${lambdaEndpoint}" -H "Content-Type: application/json" -d '${JSON.stringify(data)}'`;

  const curl = spawn('curl', ['-X', 'POST', lambdaEndpoint, '-H', 'Content-Type: application/json', '-d', JSON.stringify(data)]);

  let output = '';
  let errorOutput = '';

  curl.stdout.on('data', (data) => {
    output += data.toString();
  });

  curl.stderr.on('data', (data) => {
    errorOutput += data.toString();
  });

  curl.on('close', (code) => {
    if (code === 0) {
      try {
        const lambdaResponse = JSON.parse(output);
        console.log(`SessionID: ${lambdaResponse.sessionId}`);
        console.log(`Trustscore: ${lambdaResponse.trustScore}`);
        if (lambdaResponse.accessPolicies) {
          lambdaResponse.accessPolicies.forEach(async (policy) => {
            if (policy.accessPolicy && policy.accessPolicy.requiredAuthMethods) {
             
              let password = "";
              let otp = "";
              let fingerprint = "";

              for (const method of policy.accessPolicy.requiredAuthMethods) {
                const response = await promptUser(`Please provide ${method}: `);
                if (method === 'Password') password = response;
                if (method === 'OTP') otp = response;
                if (method === 'Fingerprint') fingerprint = response;
              }

              const userInfo = await collectUserInfo();
              const finalData = {
                sessionId: lambdaResponse.sessionId,
                password,
                otp,
                fingerprint,
                ipAddress: userInfo.ipAddress,
                location: userInfo.location,
                timezone: userInfo.timezone,
                userAgent: userInfo.userAgent,
                deviceID: userInfo.deviceID
              };

              //console.log("Final Data to send to the next Lambda:", finalData);
              sendToAnotherLambda([finalData]);
            }
          });
        } else {
          console.log("No access policies found in the response.");
        }
      } catch (error) {
        console.error("Error parsing the Lambda response:", error);
      }
    } else {
      console.error(`Error executing cURL command: ${errorOutput}`);
    }
  });
}

// Function to send data to another Lambda function
function sendToAnotherLambda(data) {
  const anotherLambdaEndpoint = 'https://ugrw5apgfh.execute-api.ap-southeast-2.amazonaws.com/verifyauthen'; // Replace with your actual API Gateway endpoint

  if (!Array.isArray(data)) {
    data = [data];
  }

  const curlCommand = `curl -X POST "${anotherLambdaEndpoint}" -H "Content-Type: application/json" -d '${JSON.stringify(data)}'`;

  const curl = spawn('curl', ['-X', 'POST', anotherLambdaEndpoint, '-H', 'Content-Type: application/json', '-d', JSON.stringify(data)]);

  let output = '';
  let errorOutput = '';

  curl.stdout.on('data', (data) => {
    output += data.toString();
  });

  curl.stderr.on('data', (data) => {
    errorOutput += data.toString();
  });

  curl.on('close', (code) => {
    if (code === 0) {
      console.log(`Receive Your Token: ${output}`);
    } else {
      console.error(`Error executing cURL command: ${errorOutput}`);
    }
  });
}

// Get file path from command line arguments
const filePath = process.argv[2];

if (!filePath) {
  console.error('Please provide a file path as a command line argument.');
  process.exit(1);
}

// Read the JSON file
fs.readFile(filePath, 'utf8', async (err, data) => {
  if (err) {
    console.error('Error reading the file:', err.message);
    return;
  }

  const blocks = extractJsonBlocksByBrace(data);

  if (blocks.length === 0) {
    console.log("No valid JSON blocks found.");
    return;
  }

  const authResponse = blocks.find(obj =>
    typeof obj.type === "string" &&
    obj.type.includes("authorization") &&
    obj.body?.scope
  );

  if (!authResponse) {
    console.log("Authorization response with VPs not found.");
    return;
  }

  const validityBlock = blocks.find(obj =>
    obj.hasOwnProperty("is_valid") && obj.circuit_id === "authV2"
  );

  if (validityBlock && validityBlock.is_valid === false) {
    console.log("❌ VC is not valid. Proof failed!");
    return;
  }

  if (validityBlock && validityBlock.is_valid === true) {
    console.log("✅ VC is valid!");
  }

  const To = authResponse.to || "None";  // Handle 'to' field correctly
  const From = authResponse.from || "None"; 

  const result = authResponse.body.scope.map(scope => {
    const vc = scope.vp?.verifiableCredential;
    const context = vc?.["@context"] || vc?.[0]?.["@context"];
    const claims = vc?.credentialSubject || vc?.[0]?.credentialSubject;

    return {
      circuitId: scope.circuitId,
      context,
      To,  // Make sure 'To' field is extracted
      From,
      credentialSubject: claims
    };
  });

  //console.log(result);
  sendToLambda(result);
});
