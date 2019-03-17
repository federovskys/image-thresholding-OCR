# Image adaptative thresholding for tesseract-OCR
The goal is to create a binary representation of the image, classifying each pixel into one of two categories, such as "black" or "white". This is a common task in many image processing applications, and some computer graphics applications. However, fixed thresholding often fails if the illumination varies spatially in the image or over time in a video stream. 

In order to account for variations in illumination, the common solution is adaptive thresholding. The main difference here is that a different threshold value is computed for each pixel in the image.
