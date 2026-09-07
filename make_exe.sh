  GNU nano 8.7.1                                         make_exe.sh *                                                
#!/bin/bash

sudo source env/bin/activate

pyinstaller --onefile --noconsole --name NetBadger main.py

sudo chown ubi /dist/NetBadger
