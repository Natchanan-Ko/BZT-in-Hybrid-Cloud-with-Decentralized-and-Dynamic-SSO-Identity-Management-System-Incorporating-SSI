from web3 import Web3
import json
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY") # Or hardcode for local testing (not recommended)
# PRIVATE_KEY = "0x..."  # ⚠️ For local testing only

ALCHEMY_URL = "https://eth-sepolia.g.alchemy.com/v2/BzOut2aj1tiT-J63nHeO9_iZPHjwKz9x"
CONTRACT_ADDRESS = "0x23f7341535b33BDF2076778293Bc2d304d1c3134"

ABI_JSON = """[
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_ssoTokenId",
				"type": "string"
			}
		],
		"name": "decryptAllResources",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_ssoTokenId",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "field",
				"type": "string"
			}
		],
		"name": "decryptField",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_did",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_licenseNumber",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_department",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_role",
				"type": "string"
			},
			{
				"internalType": "uint8",
				"name": "_userLevel",
				"type": "uint8"
			},
			{
				"internalType": "uint256",
				"name": "_trustScore",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_expirationDateTime",
				"type": "uint256"
			},
			{
				"internalType": "string[]",
				"name": "_accessibleResources",
				"type": "string[]"
			}
		],
		"name": "generateSSOToken",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_ssoTokenId",
				"type": "string"
			}
		],
		"name": "isValidSSOToken",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_ssoTokenId",
				"type": "string"
			}
		],
		"name": "revokeSSOToken",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "ssoTokens",
		"outputs": [
			{
				"internalType": "string",
				"name": "ssoTokenId",
				"type": "string"
			},
			{
				"internalType": "bytes",
				"name": "encryptedDID",
				"type": "bytes"
			},
			{
				"internalType": "bytes",
				"name": "encryptedLicenseNumber",
				"type": "bytes"
			},
			{
				"internalType": "bytes",
				"name": "encryptedDepartment",
				"type": "bytes"
			},
			{
				"internalType": "bytes",
				"name": "encryptedRole",
				"type": "bytes"
			},
			{
				"internalType": "uint8",
				"name": "userLevel",
				"type": "uint8"
			},
			{
				"internalType": "uint256",
				"name": "trustScore",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "expirationDateTime",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "tokenCounter",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_ssoTokenId",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_day",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_month",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_year",
				"type": "uint256"
			}
		],
		"name": "updateExpirationDate",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]"""  # Replace with full ABI JSON string
ABI = json.loads(ABI_JSON)

# ========== Setup ==========
w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
if not w3.is_connected():
    print("❌ Failed to connect to Ethereum network.")
    exit()
print("✅ Connected to Ethereum network.")

acct = w3.eth.account.from_key(PRIVATE_KEY)
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"⏱️ {func.__name__} took {time.time() - start:.2f} seconds")
        return result
    return wrapper

@timer
def generate_sso_token(did, license_number, department, role, user_level, trust_score, expiration_datetime, resources):
    try:
        nonce = w3.eth.get_transaction_count(acct.address, "pending")
        gas_price = w3.to_wei('12', 'gwei')

        tx = contract.functions.generateSSOToken(
            did, license_number, department, role, user_level, trust_score, expiration_datetime, resources
        ).build_transaction({
            'from': acct.address,
            'nonce': nonce,
            'gas': 500000,
            'gasPrice': gas_price
        })

        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"📤 Transaction sent: {tx_hash.hex()}")

        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"✅ Mined in block: {receipt.blockNumber}")
        return receipt

    except Exception as e:
        print(f"❌ Error generating SSO token: {e}")

@timer
def get_latest_token_id():
    try:
        counter = contract.functions.tokenCounter().call()
        if counter == 0:
            print("⚠️ No tokens created yet.")
            return None
        return f"SSO-{counter - 1}"
    except Exception as e:
        print(f"❌ Error getting token ID: {e}")
        return None

@timer
def check_validity(token_id):
    try:
        is_valid = contract.functions.isValidSSOToken(token_id).call()
        print(f"🔍 Validity of '{token_id}': {'✅ Valid' if is_valid else '❌ Invalid'}")
    except Exception as e:
        print(f"❌ Error checking validity: {e}")

@timer
def revoke_sso_token(token_id):
    try:
        nonce = w3.eth.get_transaction_count(acct.address)
        tx = contract.functions.revokeSSOToken(token_id).build_transaction({
            "from": acct.address,
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": w3.to_wei("10", "gwei")
        })

        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"🛑 Token revoked. Tx hash: {tx_hash.hex()}")
    except Exception as e:
        print(f"❌ Error revoking token: {e}")

if __name__ == "__main__":
    generate_sso_token("did:example:123456", "XY88512", "Finance", "Analyst", 1, 40, 1805000000, ["Budget", "Invoices"])

    token_id = get_latest_token_id()
    if token_id:
        check_validity(token_id)
        revoke_sso_token(token_id)
        check_validity(token_id)
