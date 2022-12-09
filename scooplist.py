import re, subprocess

regex = r"^([A-Za-z0-9-_]+)\s+"

output = subprocess.check_output("scoop list", shell=True)
output = output.decode("utf-8")

matches = re.finditer(regex, output, re.MULTILINE)
results = [match.group(1) for match in matches]
results = results[1:] # remove the title


with open("scoop_packages", "w") as f:
    f.write("\n".join(results))
