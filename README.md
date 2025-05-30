# BZT-in-Hybrid-Cloud-with-Decentralized-and-Dynamic-SSO-Identity-Management-System-Incorporating-SSI
## Features

- Issuer VC
- Verifier VC
- 2 Factor Authentication

## 🏁 Getting Started

### Prerequisites
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

### Upload Schema (if not already published)

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

### Issue VC to User

- Open the **Issuer Portal**:
  👉 [https://issuer-demo.privado.id](https://issuer-demo.privado.id)

- Select the uploaded schema from step 1

- Input the credential values

- Choose the **recipient DID** (e.g., from a mobile wallet)

- Deliver the VC to the user via:
- 🔳 **QR Code** – scan using the **Privado Wallet**
- 🔗 **Shareable link** – user can open directly in their wallet

> 🧠 The user now has a signed VC stored in their privacy-preserving wallet.

---

### Verify VC Using Query Builder

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

- Connect your network and smart contract address

- Generate the QR code or verification link

- Ask the user to scan with their **Privado Wallet app** or open the link

> 📬 The wallet will present the VC with only the selected fields revealed, and the verifier will validate it against the ZKP proof.

---
