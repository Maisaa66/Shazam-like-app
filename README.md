# Shazam-like-app
DSP-Team17
## Genereating executable file

1- run this command in terminal
```
pyinstaller --hidden-import "sklearn.utils._weight_vector" app.py
```
2- clone [Librosa](https://github.com/librosa/librosa)
 repo 

 3- Inside librosa you will find another folder named librosa, copy this folder to dist/app

 4- Copy the ui file and the xls file to dist/app

 5- Finally, double click on app.exe   
