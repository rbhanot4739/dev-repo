import subprocess

process = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE)
print(process.stdout)
print("******************")
print(process.stdout.decode('utf-8'))
