import json
import boto3
from accesspolicy import access_policy_check

# Set up S3 client
s3_client = boto3.client('s3')
bucket_name = '454logbucket'  # Replace with your S3 bucket name
log_file_key = 'log.json'  # S3 object key for the log file

def get_next_session_number():
    try:
        # Try fetching the log file from S3
        log_file_data = s3_client.get_object(Bucket='454logbucket', Key='log.json')
        logs = json.loads(log_file_data['Body'].read())

        if logs:
            last_tx = logs[-1].get('sessionId', 0)
            return last_tx + 1
        return 1
    except s3_client.exceptions.NoSuchKey:
        # If no logs file exists in S3, create a new one
        print("No logs found in S3, starting with sessionId 1.")
        return 1
    except Exception as e:
        print(f"Error reading session number from S3: {e}")
        return 1

def write_access_log(entry):
    """
    This function writes an access log entry to logs.json in S3.
    """
    try:
        # Fetch existing logs from S3
        try:
            log_file_data = s3_client.get_object(Bucket=bucket_name, Key=log_file_key)
            logs = json.loads(log_file_data['Body'].read())
        except s3_client.exceptions.NoSuchKey:
            logs = []  # Create an empty list if no log file exists

        # Append the new log entry
        logs.append(entry)

        # Write the updated logs back to S3
        s3_client.put_object(Bucket=bucket_name, Key=log_file_key, Body=json.dumps(logs, indent=2))
        print("Access log updated successfully in S3.")

    except Exception as e:
        print(f"Error writing access log: {e}")
        import traceback
        print("Stack trace:", traceback.format_exc())

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        body = event.get('body')
        if isinstance(body, str):
            body = json.loads(body)

        if not isinstance(body, list) or len(body) == 0:
            raise ValueError("Body must be a list of VC data.")

        sessionId = get_next_session_number()
        print(f"Generated sessionId: {sessionId}")

        # Log the structure of the body for debugging
        print(f"Body structure: {json.dumps(body)}")

        # Extract "to" from the event body
        issuedid = None
        clientdid = None
        licensenumber = None
        department = None
        role = None
        access_policies = []
        trustScore = 0  # Initialize trustScore here

        issuedid = body[0].get('To') or body[0].get('to')
        clientdid = body[0].get('From') or body[0].get('from')
        for vc in body:
            if 'circuitId' not in vc or 'credentialSubject' not in vc:
                raise ValueError("Invalid VC format")

            credential_subject = vc["credentialSubject"]
            if licensenumber is None:
                licensenumber = credential_subject.get('LicenseNumber')
            department = credential_subject.get('Department')
            role = credential_subject.get('Role')
            

            if issuedid and clientdid and department and role and licensenumber:
                result = access_policy_check(issuedid, department, role, sessionId, licensenumber)
                access_policies.append({
                    "clientdid": clientdid,
                    "accessPolicy": result
                })

                # Extract the trust score from the result and accumulate
                trustScore += result["trustScore"]  # You can adjust this logic as needed

        # Log the generated access policies
        write_access_log({
            "sessionId": sessionId,
            "accessPolicies": access_policies
        })

        # Return the response
        return {
            "statusCode": 200,
            "body": json.dumps({
                "sessionId": sessionId,
                "trustScore" : trustScore,  # Correctly return the trustScore here
                "accessPolicies": access_policies
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error", "error": str(e)})
        }
