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
CONTRACT_ADDRESS = "0x10fAeC32c089897f21B85e874BbC74625119e202"

ABI_JSON = """[
	{
		"inputs": [
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
		"outputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "ssoTokenId",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "licenseNumber",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "department",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "role",
						"type": "string"
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
					},
					{
						"internalType": "string[]",
						"name": "accessibleResources",
						"type": "string[]"
					}
				],
				"internalType": "struct LicenseDataStore.SSO",
				"name": "",
				"type": "tuple"
			}
		],
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
		"name": "revokeSSOToken",
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
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "licenseToTokenIds",
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
				"internalType": "string",
				"name": "licenseNumber",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "department",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "role",
				"type": "string"
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

# ========== Timer Decorator ==========
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"⏱️ {func.__name__} took {time.time() - start:.2f} seconds")
        return result
    return wrapper

# ========== Functions ==========

@timer
def generate_sso_token(license_number, department, role, user_level, trust_score, expiration_datetime, resources):
    try:
        nonce = w3.eth.get_transaction_count(acct.address, "pending")
        gas_price = w3.to_wei('12', 'gwei')

        tx = contract.functions.generateSSOToken(
            license_number, department, role, user_level, trust_score, expiration_datetime, resources
        ).build_transaction({
            'from': acct.address,
            'nonce': nonce,
            'gas': 300000,
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
        if counter == 1:
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

# ========== Main ==========
if __name__ == "__main__":
    generate_sso_token("XY88512", "Finance", "Analyst", 1, 40, 1805000000, ["Budget", "Invoices"])

    token_id = get_latest_token_id()
    if token_id:
        check_validity(token_id)
        revoke_sso_token(token_id)
        check_validity(token_id)
