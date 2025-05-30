import json
import boto3

# Set up S3 client
s3_client = boto3.client('s3')
bucket_name = '454logbucket'
log_file_key = 'logs.json'

def load_policy_data():
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key='resources.json')
        policy_json = response['Body'].read().decode('utf-8')
        return json.loads(policy_json)
    except Exception as e:
        print(f"Failed to load policy data from S3: {e}")
        return {}

def write_access_log(entry):
    try:
        try:
            log_file_data = s3_client.get_object(Bucket=bucket_name, Key=log_file_key)
            logs = json.loads(log_file_data['Body'].read())
        except s3_client.exceptions.NoSuchKey:
            logs = []

        logs.append(entry)
        s3_client.put_object(Bucket=bucket_name, Key=log_file_key, Body=json.dumps(logs, indent=2))
        print("Access log updated successfully in S3.")
    except Exception as e:
        print(f"Error writing access log: {e}")
        import traceback
        print("Stack trace:", traceback.format_exc())

def access_policy_check(issuerdid, department, role, session_id, license_number):
    policy_data = load_policy_data()
    role_map = policy_data.get("checkrole", {}).get(issuerdid)
    auth_policies = policy_data.get("checkAuthen", {})
    trust_score_map = policy_data.get("trustScore", {})

    if not role_map:
        raise ValueError(f"Issuer {issuerdid} not supported or missing in policy data.")

    if department not in role_map or role not in role_map[department]:
        raise ValueError(f"No mapping for role '{role}' in department '{department}' for issuer '{issuerdid}'.")

    user_level = role_map[department][role]

    accessible_resources = []
    required_auth_methods = []

    for level_key, resource in auth_policies.items():
        if not resource.get("isActive", False):
            continue

        level_number = int(level_key.replace("Lv", ""))
        if user_level >= level_number:
            accessible_resources.append(f"{department} {level_key}")
            required_auth_methods.extend(resource["authMethod"])

    hardest_auth_methods = determine_hardest_auth_methods(required_auth_methods, policy_data.get("authPriority", {}))
    trust_score = trust_score_map.get(str(user_level), 0)

    write_access_log({
        "sessionId": session_id,
        "issuerDid": issuerdid,
        "licenseNumber": license_number,
        "department": department,
        "role": role,
        "userLevel": user_level,
        "trustScore": trust_score,
        "accessibleResources": accessible_resources,
        "requiredAuthMethods": hardest_auth_methods
    })

    return {
        "sessionId": session_id,
        "userLevel": user_level,
        "trustScore": trust_score,
        "accessibleResources": accessible_resources,
        "requiredAuthMethods": hardest_auth_methods
    }

def determine_hardest_auth_methods(auth_methods, auth_priority):
    if not auth_methods or not auth_priority:
        return []

    unique_methods = list(set(auth_methods))
    sorted_methods = sorted(
        unique_methods,
        key=lambda m: auth_priority.get(m, 0),
        reverse=True
    )
    return sorted_methods[:2]

