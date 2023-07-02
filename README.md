#descr
# Tokenization


1. User Input: The user enters their credit card number and name in the provided form on the website.

   Example:
   Credit Card Number: 1234 5678 9012 3456
   Name: John Doe

2. Server Receives the Request: The Flask server receives the HTTP POST request containing the credit card number and name.

3. Check for Valid Credit Card Number: The server checks if a credit card number is provided. If not, it returns a response indicating that the credit card number is not provided.

4. Generate Checksum: The server generates a checksum from the credit card number. In this case, the SHA-256 hashing algorithm is used to generate the checksum.

   Example:
   Checksum: d83eaaae4a73f75b75f6a16ea9f8c0a0 (generated from the credit card number 1234 5678 9012 3456)

5. Check if Token Exists in DynamoDB: The server queries the DynamoDB table to check if a token with the same checksum already exists.

6. If Token Exists:
   - The server retrieves the existing token from DynamoDB.
   - It returns a response indicating that the tokenization was successful, along with the existing token.

     Example Response: Tokenization successful. Token: ABC123

7. If Token Doesn't Exist:
   - Encrypt Credit Card Number: The server encrypts the credit card number using the KMS client. The ciphertext is obtained.
   - Generate New Token: The server generates a new token using the UUID (Universally Unique Identifier) method.
   - Store Token, Checksum, and Ciphertext in DynamoDB: The server stores the new token, checksum, and ciphertext in the DynamoDB table.

     Example:
     - Token: DEF456 (generated)
     - Ciphertext: Encrypted credit card number

   - Return Response: The server returns a response indicating that the tokenization was successful, along with the new token.

     Example Response: Tokenization successful. Token: DEF456

8. Front-End Display: The user sees the tokenization successful message on the website.

Now, the credit card number "1234 5678 9012 3456" is replaced with the token "DEF456" and stored securely in the DynamoDB table. This ensures that sensitive information is protected while still allowing the server to perform operations using the token.

#detokenization


1. User Input: The user enters their name in the provided form on the website.

   Example:
   Name: John Doe

2. Server Receives the Request: The Flask server receives the HTTP POST request containing the name.

3. Check for Valid Name: The server checks if a name is provided. If not, it returns a response indicating that the name is not provided.

4. Query DynamoDB for Token and Ciphertext: The server queries the DynamoDB table using the provided name as a filter expression to find the corresponding record.

5. If Record Found:
   - Retrieve Ciphertext and Token: The server retrieves the ciphertext and token from the DynamoDB record.

     Example:
     - Ciphertext: Encrypted credit card number
     - Token: DEF456

6. Decrypt Ciphertext: The server uses the KMS client to decrypt the ciphertext and obtain the original credit card number.

   Example:
   - Decrypted Credit Card Number: 1234 5678 9012 3456

7. Return Decrypted Credit Card Number: The server returns the decrypted credit card number as the response.

   Example Response: Credit Card Number: 1234 5678 9012 3456

8. Front-End Display: The user sees the decrypted credit card number displayed on the website.

Now, the original credit card number "1234 5678 9012 3456" is obtained by decrypting the ciphertext using the corresponding token and displayed to the user. This process allows the server to securely retrieve and display the original credit card number for authorized users.
