# BZT in Hybrid Cloud with Decentralized and Dynamic SSO Identity Management System Incorporating SSI

## Features

> - Issuer VC  
> - Verifier VC  
> - 2 Factor Authentication  

## Prerequisites

### Software Requirements

> - [Node.js](https://nodejs.org/) (v14 or above recommended)  
> - npm (comes with Node.js)  
> - cURL installed (used via `child_process.spawn`)  
>   - macOS / Linux: usually preinstalled  
>   - Windows: [https://curl.se/windows/](https://curl.se/windows/)  

### Node.js Packages

```bash
npm install axios
```

## Getting Started

### Issue and Verify VC on Chain

#### Upload Schema (if not already published)

> - Go to the **Privado Issuer Schema Dashboard**  
>   👉 [Schema Dashboard](https://issuer-demo.privado.id/schemas?identifier=did%3Aiden3%3Apolygon%3Aamoy%3Ax7UPbuoupPoHo6v69MejJp17We3xNskZjijEsBFFS)

> - Use the following schema reference hosted on IPFS defining:
>   - `Name`
>   - `Surname`
>   - `LicenseNumber`
>   - `Department`
>   - `Role`

#### Issue VC to User

> - Open the **Issuer Portal**  
>   👉 [https://issuer-demo.privado.id](https://issuer-demo.privado.id)  
> - Select the uploaded schema  
> - Enter credential values  
> - Choose recipient DID (e.g., via mobile wallet)  
> - Deliver via:
>   - QR Code (Privado Wallet)  
>   - Shareable Link  

> 🧠 The user now holds a signed VC in a privacy-preserving wallet.

#### Verify VC Using Query Builder

> - Open the **Privado VC Verifier**  
>   👉 [https://tools.privado.id/query-builder/](https://tools.privado.id/query-builder/)  
> - Paste your schema reference  

> - Set Verification Parameters:
>   - ✅ Selective Disclosure:
>     - `LicenseNumber`, `Department`, `Role`  
>   - 🔐 Proof Type: `Signature-based (SIG)`  
>   - 🧪 Query Type: `Credential Atomic Query v3 (On Chain, experimental)`  

> - Select Network:
>   - Polygon Amoy Testnet  

> - Smart Contract:  
>   👉 [0x2ef1c802355c500a3493f2db8cb9c24af12c42b0](https://www.oklink.com/amoy/address/0x2ef1c802355c500a3493f2db8cb9c24af12c42b0)  

> - Generate verification QR code or link  
> - Ask the user to scan or open with **Privado Wallet**  

> 📬 Wallet reveals only selected fields; verifier checks ZKP proof.

---

## Connect Cloud and Perform Two-Factor Authentication

### Prepare Input File

> After VC verification, user is redirected to:  
> 👉 [https://jwz-validator.privado.id/](https://jwz-validator.privado.id/)  

> - Create a JSON file like `inputnurse.json` with:
>   - Header  
>   - Payload  
>   - Auth Proof (comma-separated)  

### Run Authentication Script

```bash
node testauthen.js inputnurse.json
```

---

## 🛡️ Secure Resource Access via AWS Lambda

### Project Files

```text
| File                     | Description                                                                |
|--------------------------|----------------------------------------------------------------------------|
| lambdafunction_1access.py | Authorizes access to specific resources based on role/trust score          |
| accesspolicy.py          | Enforces fine-grained access control policies                              |
| resource.json            | Defines accessible resources and levels                                    |
```

> 🔗 API Gateway:  
> 👉 [https://ugrw5apgfh.execute-api.ap-southeast-2.amazonaws.com/extract](https://ugrw5apgfh.execute-api.ap-southeast-2.amazonaws.com/extract)

```text
| File                     | Description                                                       |
|--------------------------|-------------------------------------------------------------------|
| lambdafunction_authen.py | Verifies OTP, password, fingerprint from logs.json in S3           |
```

> 🔗 API Gateway:  
> 👉 [https://ugrw5apgfh.execute-api.ap-southeast-2.amazonaws.com/verifyauthen](https://ugrw5apgfh.execute-api.ap-southeast-2.amazonaws.com/verifyauthen)

---

## 🔗 On-Chain Credential Context with Smart Contract

> After VC verification, the system references a smart contract storing second-factor authentication context.

### Second-Factor Credential Types

> - Password  
> - OTP  
> - Fingerprint  
# BZT in Hybrid Cloud with Decentralized and Dynamic SSO Identity Management System Incorporating SSI

## Features

> - Issuer VC  
> - Verifier VC  
> - 2 Factor Authentication  

## Prerequisites

### Software Requirements

> - [Node.js](https://nodejs.org/) (v14 or above recommended)  
> - npm (comes with Node.js)  
> - cURL installed (used via `child_process.spawn`)  
>   - macOS / Linux: usually preinstalled  
>   - Windows: [https://curl.se/windows/](https://curl.se/windows/)  

### Node.js Packages

```bash
npm install axios
```

## Getting Started

### Issue and Verify VC on Chain

#### Upload Schema (if not already published)

> - Go to the **Privado Issuer Schema Dashboard**  
>   👉 [Schema Dashboard](https://issuer-demo.privado.id/schemas?identifier=did%3Aiden3%3Apolygon%3Aamoy%3Ax7UPbuoupPoHo6v69MejJp17We3xNskZjijEsBFFS)

> - Use the following schema reference hosted on IPFS defining:
>   - `Name`
>   - `Surname`
>   - `LicenseNumber`
>   - `Department`
>   - `Role`

#### Issue VC to User

> - Open the **Issuer Portal**  
>   👉 [https://issuer-demo.privado.id](https://issuer-demo.privado.id)  
> - Select the uploaded schema  
> - Enter credential values  
> - Choose recipient DID (e.g., via mobile wallet)  
> - Deliver via:
>   - QR Code (Privado Wallet)  
>   - Shareable Link  

> 🧠 The user now holds a signed VC in a privacy-preserving wallet.

#### Verify VC Using Query Builder

> - Open the **Privado VC Verifier**  
>   👉 [https://tools.privado.id/query-builder/](https://tools.privado.id/query-builder/)  
> - Paste your schema reference  

> - Set Verification Parameters:
>   - ✅ Selective Disclosure:
>     - `LicenseNumber`, `Department`, `Role`  
>   - 🔐 Proof Type: `Signature-based (SIG)`  
>   - 🧪 Query Type: `Credential Atomic Query v3 (On Chain, experimental)`  

> - Select Network:
>   - Polygon Amoy Testnet  

> - Smart Contract:  
>   👉 [0x2ef1c802355c500a3493f2db8cb9c24af12c42b0](https://www.oklink.com/amoy/address/0x2ef1c802355c500a3493f2db8cb9c24af12c42b0)  

> - Generate verification QR code or link  
> - Ask the user to scan or open with **Privado Wallet**  

> 📬 Wallet reveals only selected fields; verifier checks ZKP proof.

---

## Connect Cloud and Perform Two-Factor Authentication

### Prepare Input File

> After VC verification, user is redirected to:  
> 👉 [https://jwz-validator.privado.id/](https://jwz-validator.privado.id/)  

> - Create a JSON file like `inputnurse.json` with:
>   - Header  
>   - Payload  
>   - Auth Proof (comma-separated)  

### Run Authentication Script

```bash
node testauthen.js inputnurse.json
```

---

## 🛡️ Secure Resource Access via AWS Lambda

### Project Files

```text
| File                     | Description                                                                |
|--------------------------|----------------------------------------------------------------------------|
| lambdafunction_1access.py | Authorizes access to specific resources based on role/trust score          |
| accesspolicy.py          | Enforces fine-grained access control policies                              |
| resource.json            | Defines accessible resources and levels                                    |
```

> 🔗 API Gateway:  
> 👉 [https://ugrw5apgfh.execute-api.ap-southeast-2.amazonaws.com/extract](https://ugrw5apgfh.execute-api.ap-southeast-2.amazonaws.com/extract)

```text
| File                     | Description                                                       |
|--------------------------|-------------------------------------------------------------------|
| lambdafunction_authen.py | Verifies OTP, password, fingerprint from logs.json in S3           |
```

> 🔗 API Gateway:  
> 👉 [https://ugrw5apgfh.execute-api.ap-southeast-2.amazonaws.com/verifyauthen](https://ugrw5apgfh.execute-api.ap-southeast-2.amazonaws.com/verifyauthen)

---

## 🔗 On-Chain Credential Context with Smart Contract

> After VC verification, the system references a smart contract storing second-factor authentication context.

### Second-Factor Credential Types

> - Password  
> - OTP  
> - Fingerprint  

### Smart Contract Info

> - **Source Code**: `solidity/verify.sol`  
> - **Blockchain**: Ethereum Sepolia
> - **Address**:  
>   👉 [0xcaddB760BE8C70d773D8F361607Cb3f3c8094db9]

> 🧠 Used immediately post-VC verification to validate MFA via `LicenseNumber`.

### Benefits

> - ✅ Decentralized & immutable authentication  
> - ✅ Enhanced security via VC + MFA separation  
> - ✅ No centralized backend dependency  

---

## 🔐 Decentralized SSO Token Generation with Smart Contract

> After Lambda confirms 2FA, the smart contract generates a session token for secure access.

### Contract Info

> - **Source Code**: `solidity/ssogen.sol`  
> - **Test Script**: `ssogentest.py (add PRIVKEY before testing)`  
> - **Blockchain**: Ethereum Sepolia  
> - **Contract Address**:  
>   👉 [0x23f7341535b33BDF2076778293Bc2d304d1c3134](https://sepolia.etherscan.io/address/0x23f7341535b33BDF2076778293Bc2d304d1c3134)

### What It Stores

> - `ssoTokenId` (plaintext)  
> - XOR Encrypted Fields:
>   - DID  
>   - License Number  
>   - Department  
>   - Role  
>   - Accessible Resources  
> - Plaintext:
>   - `userLevel`  
>   - `trustScore`  
>   - `expirationDateTime`  

### Token Lifecycle Functions

> - `generateSSOToken()`  
> - `isValidSSOToken()`  
> - `revokeSSOToken()`  
> - `updateExpirationDate()`  

> 🛡️ Finalizes decentralized identity lifecycle: VC → 2FA → On-chain token

---

## License

> SIIT
