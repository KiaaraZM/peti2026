import hashlib, glob, os

files = glob.glob('evidencias/*.csv') + glob.glob('01_marco/*.csv')
hashes = []
for f in sorted(files):
    with open(f, 'rb') as file:
        h = hashlib.sha256(file.read()).hexdigest()
        hashes.append(f'{h}  {f}')

os.makedirs('evidencias', exist_ok=True)
with open('evidencias/HASHES.txt', 'w', encoding='utf-8') as out:
    out.write('\n'.join(hashes) + '\n')

print("Hashes actualizados con éxito en evidencias/HASHES.txt:")
print('\n'.join(hashes))
