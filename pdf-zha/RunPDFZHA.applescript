set scriptPath to POSIX path of (choose file with prompt "Select the setup-macOS.sh script")
do shell script "cd " & quoted form of scriptPath & " && ./setup-macOS.sh"
