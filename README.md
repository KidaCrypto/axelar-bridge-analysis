# For Mac OS
- Needs to run /Applications/Python\ 3.11/Install\ Certificates.command ; exit;
- Replace 3.11 with your python version

# Predictive Analysis
1. Download all top 100k SQL results except those that timed out.
2. Move all the raw data into the raw folder.
3. In command line, type python3 process.py raw
4. In command line, type python3 process.py advanced
5. In command line, type python3 process.py train
6. Done! Now you have all the models used for this analysis.