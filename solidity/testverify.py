from web3 import Web3
import json

# Connect to the Ethereum network via Alchemy
w3 = Web3(Web3.HTTPProvider('https://eth-sepolia.g.alchemy.com/v2/Axg4Sv45h5KT9nE-N3-D0xsne__nqY1R'))
if w3.is_connected():
    print("Connected to Sepolia via Alchemy")
else:
    print("Failed to connect to Ethereum network.")
    exit()

# Smart contract address and ABI
Contract_ADDRESS = '0xcaddB760BE8C70d773D8F361607Cb3f3c8094db9'
ABI_JSON = """[
    {
        "inputs": [
            {"internalType": "string", "name": "licensenumber", "type": "string"},
            {"internalType": "string", "name": "password", "type": "string"},
            {"internalType": "string", "name": "otp", "type": "string"},
            {"internalType": "string", "name": "fingerprint", "type": "string"}
        ],
        "name": "setContext",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string", "name": "licensenumber", "type": "string"}],
        "name": "getPassword",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string", "name": "licensenumber", "type": "string"}],
        "name": "getOtp",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string", "name": "licensenumber", "type": "string"}],
        "name": "getFingerprint",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    }
]"""

# Parse ABI
ABI = json.loads(ABI_JSON)
contract = w3.eth.contract(address=Contract_ADDRESS, abi=ABI)

# Function to interact with the contract and fetch data
def fetch_contract_data(licensenumber):
    try:
        # Fetch data from the contract
        stored_password = contract.functions.getPassword(licensenumber).call()
        stored_otp = contract.functions.getOtp(licensenumber).call()
        stored_fingerprint = contract.functions.getFingerprint(licensenumber).call()

        print(f"Stored values for {licensenumber}:")
        print(f"Password: {stored_password}")
        print(f"OTP: {stored_otp}")
        print(f"Fingerprint: {stored_fingerprint}")
        return stored_password, stored_otp, stored_fingerprint
    except Exception as e:
        print(f"Error interacting with contract: {e}")
        return None, None, None

# Verification function
def verify(licensenumber, password, fingerprint, otp):
    # Fetch stored data from the contract
    stored_password, stored_otp, stored_fingerprint = fetch_contract_data(licensenumber)

    if stored_password is None or stored_otp is None or stored_fingerprint is None:
        print("Failed to retrieve data from the contract.")
        return False

    # Reject if all fields are None
    if password is None and fingerprint is None and otp is None:
        print("Verification failed! All fields are None.")
        return False

    # Compare provided values with the stored values, ignoring None values
    if ((password is None or stored_password == password) and 
        (otp is None or stored_otp == otp) and 
        (fingerprint is None or stored_fingerprint == fingerprint)):
        print("Verification successful!")
        return True
    else:
        print("Verification failed!")
        return False

# Test cases
test_cases = [
    {"licensenumber": "AB16542", "password": "1", "fingerprint": "none", "otp": "1"},
    {"licensenumber": "XY88312", "password": "0", "fingerprint": "scan", "otp": "1"},
    {"licensenumber": "JK99872", "password": "2", "fingerprint": "manual", "otp": "0"},
    {"licensenumber": "ZZ11223", "password": "3", "fingerprint": "none", "otp": "2"}
]

# Run test cases
def run_tests():
    for case in test_cases:
        print(f"\nTesting {case['licensenumber']}...")
        result = verify(case["licensenumber"], case["password"], case["fingerprint"], case["otp"])
        if result:
            print(f"Verification for {case['licensenumber']} succeeded!\n")
        else:
            print(f"Verification for {case['licensenumber']} failed.\n")

if __name__ == "__main__":
    run_tests()
