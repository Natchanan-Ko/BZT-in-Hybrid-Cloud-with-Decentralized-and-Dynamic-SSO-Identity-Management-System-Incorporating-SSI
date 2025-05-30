import json
import boto3

# Setup S3 client
s3_client = boto3.client('s3')
bucket_name = '454logbucket'
log_file_key = 'logs.json'

# Simulated credentials from blockchain (or some source)
checkpw = "1"
checkotp = "1"
checkfingerprint = "1"

def get_required_auth_methods(session_id):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=log_file_key)
        logs = json.loads(response['Body'].read().decode('utf-8'))

        for entry in logs:
            sid = entry.get('sessionId')
            if sid == session_id:
                return entry.get('requiredAuthMethods', [])
        print(f"No matching sessionId {session_id} found in logs.")
        return []
    except Exception as e:
        print(f"❌ Error reading or parsing S3 logs.json: {e}")
        return []

def lambda_handler(event, context):
    try:
        print("📥 Received event:", json.dumps(event))

        # Parse event body
        body = event.get('body')
        if isinstance(body, str):
            body = json.loads(body)
        if isinstance(body, list):
            body = body[0]
        if not isinstance(body, dict):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid body format."})
            }

        # Extract fields
        sessionId = body.get('sessionId')
        password = body.get('password')
        otp = body.get('otp')
        fingerprint = body.get('fingerprint')

        if sessionId is None:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing sessionId"})
            }

        try:
            sessionId = int(sessionId)  # Force integer for comparison
        except ValueError:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "sessionId must be an integer"})
            }

        # 🔍 Fetch required auth methods
        required_methodsin = get_required_auth_methods(sessionId)
        print(f"🔐 Required methods for session {sessionId}: {required_methodsin}")

        # Validate only required methods
        errors = False
        if not required_methodsin:
            print("⚠️ No required auth methods for this session.")
            errors = True
        if "Password" in required_methodsin and password != checkpw:
            print("❌ Password mismatch")
            errors = True
        if "OTP" in required_methodsin and otp != checkotp:
            print("❌ OTP mismatch")
            errors = True
        if "Fingerprint" in required_methodsin and fingerprint != checkfingerprint:
            print("❌ Fingerprint mismatch")
            errors = True

        if errors:
            return {
                "statusCode": 401,
                "body": json.dumps({"error": "Authentication failed"})
            }

        return {
            "statusCode": 200,
            "body": json.dumps({"token": "example onchain token"})
        }

    except Exception as e:
        print("❌ Unexpected Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Internal server error",
                "details": str(e)
            })
        }
