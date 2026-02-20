from werkzeug.security import generate_password_hash, check_password_hash

password = "my_secure_password2377"

# Hash the password twice
hash1 = generate_password_hash(password)
hash2 = generate_password_hash(password)

print(f"Password: {password}")
print(f"Hash 1: ({len(hash1)}) {hash1}")
print(f"Hash 2: ({len(hash2)}) {hash2}")
print(f"Are they the same? {'YES' if hash1 == hash2 else 'NO'}")

# Verify they both work
print(f"Verify Hash 1: {check_password_hash(hash1, password)}")
print(f"Verify Hash 2: {check_password_hash(hash2, password)}")
