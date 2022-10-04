import gnupg

filename = './demo.txt.gpg'

gpg = gnupg.GPG()
with open(filename, 'rb') as f:
    status = gpg.decrypt_file(f)

print('ret: ', status)
print('ok: ', status.ok)
print('status: ', status.status)

# print('stderr: ', status.stderr)

