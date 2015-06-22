# ASTronomic Image Rendering #


---



## A new release is coming, everything was rebuilded (with a new kernel) ##


---





![http://wiki.astir.googlecode.com/hg/images/us_uk.gif](http://wiki.astir.googlecode.com/hg/images/us_uk.gif) _(French section below)_

Astir is an interactive shell which gives couple of functions of image processing and image rendering. Functions are specially design to enhance astronomic images from pictures or videos. Purpose of this project is to give powerful functions to any amateur astronomers. The blueprint of Astir is to design complete feature of mosaicing, super-resolution, filtering, analysis, etc.

# Features #
  * Interactive shell with workspace and basic function: ls, cp, mv, ...
  * Able to run a script of command (script astir shell .sas)
  * Read and write images (32 bit bmp and png)
  * GUI to display images
  * Load video (avi)
  * Split video in sequence of images (stacking)
  * Cut off images sequence
  * Color transformation (luminance, RGB, false-color)
  * Averaging method to increase signal-noise-ratio from video sequence
  * Automatic movement tracking between frame video
  * Image anaglyph
  * Image operations (add, sub, mul, div, ...)
  * Image transformation (homography, flip, rotation, interpolation bilinear, bicubic) **IN PROGRESS**
  * Image analysis (average, variance, power, power spectra, rotational power spectra, histogram...) **IN PROGRESS**
  * Image mosaicing with semi-automatic procedure (homographic registration, progressing blending, ...) **IN PROGRESS**

# Dependencies #
  * Python >= 2.5
  * Numpy => 1.1.0
  * Scipy => 0.6.0
  * Matplotlib >= 0.98.1
  * ffmpeg >= svn20080206
  * Imaging >= 1.1.6 (PIL)

![http://wiki.astir.googlecode.com/hg/images/fr.gif](http://wiki.astir.googlecode.com/hg/images/fr.gif)

Astir est une console interactive qui donne un ensemble de fonctions de traitement et de rendu d'images. Les fonctions sont speciallement elaborees pour l'amelioration d'images astronomique provenant d'images ou de videos. Le but du projet est de donner de puissante fonctions a n'importe quel astronome amateur. Les perspectives d'Astir est delaborer des methodes completes de mosaicing, de super-resolution, de filtrage, analyse, etc.

# Caracteristiques #
  * Console interactive avec espace de travail et de fonction basic: ls, cp, mv, ...
  * Capable d'executer un script de commande (script astir shell .sas)
  * Lecture et ecriture d'images (32 bit bmp et png)
  * GUI pour afficher les images
  * Chargement de video (avi)
  * Decomposition de video en sequence d'images (stacking)
  * Decoupe de sequence d'images
  * Anaglyphe d'image
  * Operation entre image (add, sub, mul, div, ...)
  * Analyse d'images (moyenne, variance, puissance, spectre de puissance, spectre de puissance rotationel, histogramme...) **EN COURS**
  * Transformation de couleur (luminance, RGB, fausse couleurs)
  * Transformation d'image (colineation, flip, rotation, interpolation bilineare, bicubique) **EN COURS**
  * Method de moyennage pour augmenter le raport signal sur bruit depuis une sequence video
  * Suivie du deplacement entre les images du video automatiquement
  * Mosaicing d'image avec une procedure semi-automatique (recallage par collineation, fusion progressive, ...) **EN COURS**

# Dependences #
  * Python >= 2.5
  * Numpy => 1.1.0
  * Scipy => 0.6.0
  * Matplotlib >= 0.98.1
  * ffmpeg >= svn20080206
  * Imaging >= 1.1.6 (PIL)

# Gallery #

Astir v0.36

![http://wiki.astir.googlecode.com/hg/images/astir_v036.png](http://wiki.astir.googlecode.com/hg/images/astir_v036.png)


Example of color mapping (left to right, top to bottom: original image only in luminance, color map hsv, color map hot and color map jet).

![http://wiki.astir.googlecode.com/hg/images/soleil_map.jpg](http://wiki.astir.googlecode.com/hg/images/soleil_map.jpg)

