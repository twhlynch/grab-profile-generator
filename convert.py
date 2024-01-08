import os

input = "sgm"
output = "cosmetics"

for root, dirs, files in os.walk(input):
    for file in files:
        path = os.path.join(root, file)
        output_path = os.path.join(output, path[len(input)+1:])
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        output_path = output_path[:-4]+".obj"
        print(f"Converting {path} to {output_path}")
        os.system(f"python sgm2obj.py {path} {output_path}")