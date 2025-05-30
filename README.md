# BZT-in-Hybrid-Cloud-with-Decentralized-and-Dynamic-SSO-Identity-Management-System-Incorporating-SSI
## Features

- Issuer VC
- Verifier VC
- 2 Factor Authentication

## Prerequisites

#### Software Requirements

- **[Node.js](https://nodejs.org/)** (v14 or above recommended)
- **npm** (comes with Node.js)
- **cURL** installed (used via `child_process.spawn`)
  - macOS / Linux: usually preinstalled
  - Windows: [https://curl.se/windows/](https://curl.se/windows/)

#### Node.js Packages

Install project dependencies:

```bash
npm install axios
```

## Get start
### Issue and Verify VC on Chain
#### Upload Schema (if not already published)

If your credential schema is not yet registered:

- Go to the **Privado Issuer Schema Dashboard**:
  👉 [https://issuer-demo.privado.id/schemas?identifier=did%3Aiden3%3Apolygon%3Aamoy%3Ax7UPbuoupPoHo6v69MejJp17We3xNskZjijEsBFFS](https://issuer-demo.privado.id/schemas?identifier=did%3Aiden3%3Apolygon%3Aamoy%3Ax7UPbuoupPoHo6v69MejJp17We3xNskZjijEsBFFS)

- Use the following schema reference hosted on IPFS:


This schema must define fields such as:
- `Name`
- `Surname`
- `LicenseNumber`
- `Department`
- `Role`

#### Issue VC to User

- Open the **Issuer Portal**:
  👉 [https://issuer-demo.privado.id](https://issuer-demo.privado.id)

- Select the uploaded schema from step 1

- Input the credential values

- Choose the **recipient DID** (e.g., from a mobile wallet)

- Deliver the VC to the user via:
- 🔳 **QR Code** – scan using the **Privado Wallet**
- 🔗 **Shareable link** – user can open directly in their wallet

> 🧠 The user now has a signed VC stored in their privacy-preserving wallet.

#### Verify VC Using Query Builder

- Open the **Privado VC Verifier**:
👉 [https://tools.privado.id/query-builder/](https://tools.privado.id/query-builder/)

- Paste the following schema reference to match the issued VC:

- Set your verification parameters:
  - ✅ Selective disclosure fields:
    - `LicenseNumber`
    - `Department`
    - `Role`
  - 🔐 **Proof Type**: `Signature-based (SIG)`
  - 🧪 **Query Type**: `Credential Atomic Query v3 (On Chain, experimental)`

- Select Network and Contract To verify on-chain:

- ✅ **Select Network**:
  - `Polygon Amoy Testnet`

- ✅ **Smart Contract Address**:
0x2ef1c802355c500a3493f2db8cb9c24af12c42b0

- 🔍 View this contract on OkLink:
👉 [https://www.oklink.com/amoy/address/0x2ef1c802355c500a3493f2db8cb9c24af12c42b0](https://www.oklink.com/amoy/address/0x2ef1c802355c500a3493f2db8cb9c24af12c42b0)

- Generate the QR code or verification link

- Ask the user to scan with their **Privado Wallet app** or open the link

> 📬 The wallet will present the VC with only the selected fields revealed, and the verifier will validate it against the ZKP proof.

### Connect cloud and Two authentication

#### Prepare Your Input File

After a successful VC verification using the Privado Query Builder, the user is redirected to a URL like:
👉 [https://jwz-validator.privado.id/]
- Create a JSON file consist of header, payload, auth proof by use comma separate.
- You can refer to the sample file `inputnurse.json` provided in this repository.

#### Run the Tool

Open your terminal and run:

```bash
node testauthen.js inputnurse.json
```

### 🛡️ Secure Resource Access via AWS Lambda

This project implements an authentication and access control system using AWS Lambda, S3, and JSON-based policies.

#### 📁 Project Structure

| File | Description |
|------|-------------|
| `lambdafunction_1access.py` | Authorizes access to specific resources based on role and trust score. |
| `accesspolicy.py` | Contains logic to enforce fine-grained access control policies. |
| `resource.json` | Static file defining accessible resources and access levels. |
|------|-------------|

We redirect these 3 file3 by using 👉 [https://ugrw5apgfh.execute-api.ap-southeast-2.amazonaws.com/extract] (already existing in code)

| File | Description |
|------|-------------|
| `lambdafunction_authen.py` | Authenticates user sessions by verifying OTP, password, and fingerprint data from an S3 `logs.json` file. |
|------|-------------|

We redirect this file by using 👉 [https://ugrw5apgfh.execute-api.ap-southeast-2.amazonaws.com/verifyauthen] (already existing in code)

🔗 On-Chain Credential Context with Smart Contract
After the Verifiable Credential (VC) is successfully verified using the Privado Verifier, the system performs an additional verification step by referencing a smart contract deployed on-chain.

This contract contains the second-factor authentication context, which ensures the user has valid credentials beyond the VC, such as:

Password
OTP
Fingerprint
📄 Source Code

Location: solidity/verify.sol
This file defines the smart contract used for storing and retrieving the authentication context tied to a user’s LicenseNumber.

🧠 When It’s Used

Immediately after VC verification is complete, the system queries this smart contract using the LicenseNumber as the key. This confirms that the user has successfully completed multi-factor authentication (MFA) using verifiable, tamper-proof data stored on-chain.

✅ Benefits

Decentralized and immutable authentication record
Enhanced security through separation of identity (VC) and authentication credentials
No reliance on centralized backend databases
🌐 Network and Deployment Info

Blockchain: Polygon Amoy Testnet
Smart Contract Address:
👉 0xcaddB760BE8C70d773D8F361607Cb3f3c8094db9
🛡️ This second verification layer strengthens decentralized SSO by verifying both who the user is (via VC) and how they authenticate (via smart contract).

🔗 On-Chain Credential Context with Smart Contract
After the Verifiable Credential (VC) is successfully verified using the Privado Verifier, the system performs an additional verification step by referencing a smart contract deployed on-chain.

This contract contains the 'second-factor authentication context', which ensures the user has valid credentials beyond the VC, such as:

'Password'
'OTP'
'Fingerprint'
📄 Source Code

'Location': 'solidity/verify.sol'
'Test Script': 'testverify.py'
This smart contract is used to store and retrieve MFA values linked to a user's 'LicenseNumber'. The testverify.py script demonstrates how to interact with the contract (read fields, check values, etc.) using Python and Web3.py.

🧠 When It’s Used

Immediately after VC verification is complete, the system queries this smart contract using the 'LicenseNumber' as the key. This confirms that the user has successfully completed 'multi-factor authentication (MFA)' using verifiable, tamper-proof data stored on-chain.

✅ Benefits

'Decentralized and immutable' authentication record
'Enhanced security' through separation of identity (VC) and authentication credentials
'No reliance on centralized backend databases'
🌐 Network and Deployment Info

'Blockchain': Ethereum Sepolia Testnet
'Smart Contract Address':
👉 '0xcaddB760BE8C70d773D8F361607Cb3f3c8094db9'
🛡️ This second verification layer strengthens decentralized SSO by verifying both 'who the user is' (via VC) and 'how they authenticate' (via smart contract).
🔐 Decentralized SSO Token Generation with Smart Contract
After AWS Lambda successfully verifies 'two authentication factors' (password, OTP, fingerprint), the system proceeds to 'generate a Single Sign-On (SSO) token' using an on-chain smart contract. This ensures secure session management in a decentralized and privacy-preserving way.

📄 Source Code

'Location': 'solidity/ssogen.sol'
'Test Script': 'ssogentest.py'
This smart contract ('LicenseDataStore') is responsible for:

Creating SSO tokens with encrypted session metadata
Storing user roles, departments, and access levels securely
Validating, revoking, and updating token metadata
The ssogentest.py script demonstrates how to call generateSSOToken(), decrypt fields, and validate tokens using Web3.py from your Python environment.

🧾 What the Contract Stores

Each generated SSO token includes:

'ssoTokenId' (plain text)
Encrypted fields:
DID
License Number
Department
Role
Accessible Resources
Plaintext values:
'userLevel' (used for access logic)
'trustScore'
'expirationDateTime'
🧠 When It’s Used

Immediately 'after successful 2FA verification' by the Lambda function
The smart contract's 'generateSSOToken()' is called to issue a new token
Any system that needs to validate user identity and trust can query this contract using the token ID
✅ Key Features

'XOR Encryption': Lightweight symmetric encryption for on-chain field protection
'Resource-Level Access': Supports per-token access rights to specific resources
'Token Lifecycle Management':
'isValidSSOToken()' for live session checks
'revokeSSOToken()' to immediately disable a session
'updateExpirationDate()' for administrative extension
🌐 Network and Deployment Info

'Blockchain': Ethereum Sepolia Testnet
'Smart Contract Address':
👉 '0x23f7341535b33BDF2076778293Bc2d304d1c3134'
'SSO Token Transactions':
👉 'https://sepolia.etherscan.io/address/0x23f7341535b33BDF2076778293Bc2d304d1c3134'
🔐 This mechanism finalizes the decentralized identity lifecycle: from 'VC issuance', through '2FA verification', to 'on-chain session tokenization'.
---
