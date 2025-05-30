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

---
