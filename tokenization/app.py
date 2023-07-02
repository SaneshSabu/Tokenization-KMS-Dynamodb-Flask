#Original 3

import boto3
import hashlib
import uuid
from flask import Flask, request, render_template

app = Flask(__name__)

# Create a Boto3 client for DynamoDB
dynamodb_client = boto3.client('dynamodb', region_name='ap-southeast-2')

# Create a Boto3 client for KMS
kms_client = boto3.client('kms', region_name='ap-southeast-2')

# DynamoDB table name
dynamodb_table_name = 'token-db'

@app.route('/', methods=['GET', 'POST'])
def tokenize():
    if request.method == 'POST':
        # Get the credit card number and name from the request form
        credit_card_number = request.form.get('credit_card_number')
        name = request.form.get('name')

        # Check if the credit card number is provided
        if not credit_card_number:
            return 'Credit card number not provided', 400

        # Generate the checksum (you can use your own hashing algorithm here)
        checksum = generate_checksum(credit_card_number)

        # Check if the token exists in DynamoDB
        response = dynamodb_client.get_item(
            TableName=dynamodb_table_name,
            Key={'token-table-key': {'S': checksum}}
        )

        # If a record is found, return the existing token
        if 'Item' in response:
            token = response['Item']['token']['S']
            return f'Tokenization successful. Token: {token}'

        else:
            # Encrypt the credit card number using KMS
            ciphertext = encrypt_credit_card_number(credit_card_number)

            # Generate a new token (UUID)
            token = generate_token()

            # Store the token, checksum, name, and ciphertext in DynamoDB
            dynamodb_client.put_item(
                TableName=dynamodb_table_name,
                Item={
                    'token-table-key': {'S': checksum},
                    'token': {'S': token},
                    'ciphertext': {'B': ciphertext},
                    'name': {'S': name}
                }
            )

            return f'Tokenization successful. Token: {token}'

    # If it's a GET request, render the HTML form
    return render_template('index.html')

def generate_checksum(credit_card_number):
    # Implement your checksum generation logic here
    # For example, you can use the SHA-256 hashing algorithm
    # to generate a checksum from the credit card number
    checksum = hashlib.sha256(credit_card_number.encode()).hexdigest()
    return checksum

def encrypt_credit_card_number(credit_card_number):
    # Use the KMS client to encrypt the credit card number
    # Replace 'your-kms-key-id' with the actual KMS key ID
    response = kms_client.encrypt(
        KeyId='055e121c-723e-49d1-90b7-049f827793d2',
        Plaintext=credit_card_number.encode('utf-8')
    )
    ciphertext = response['CiphertextBlob']
    return ciphertext

def generate_token():
    # Generate a UUID (Universally Unique Identifier) as the token
    token = str(uuid.uuid4())
    return token

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

