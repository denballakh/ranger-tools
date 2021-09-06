@echo off
git restore --staged ../
git add .
git commit -m "Script Functions Update: %date%_%time%"
git push
pause
