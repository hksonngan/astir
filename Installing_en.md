IN PROGRESS

# Introduction #

Astir required third part libraries:

  * Python >= 2.5
  * Numpy => 1.1.0
  * Scipy => 0.6.0
  * Matplotlib >= 0.98.1
  * ffmpeg >= svn20080206
  * Imaging >= 1.1.6 (PIL)

# Ubuntu GNU/Linux #

```
sudo apt-get install python-numpy python-scipy python-matplotlib python-imaging ffmpeg
```

Download or checkout Astir. Change to the Astir's directory, then check if every dependences are ok, by,

```
python pymir_check.py
```

# Mac OS X #

Download and install the following binaries:
  * python-2.6.2-macosx2009-04-16.dmg
  * numpy-1.3.0-py2.6-macosx10.5.dmg
  * scipy-0.7.1-py2.6-python.org.dmg
  * matplotlib-0.99.0-py2.6-macosx10.5.dmg

**Macport**

Install macport-1.8.0 for snow leopard, then install, and add the correct path,

```
export PATH=$PATH:/opt/local/bin
```

Update the port,
```
sudo port -d selfupdate
```

**ffmpeg**

Now you can install ffmpeg via macport,

```
sudo port install ffmpeg
```

In order to install Imaging you need get a couple of library before.

**freetype**

http://freetype.sourceforge.net
```
tar zxvf freetype-2.3.9.tar.gz
cd freetype-2.3.9
./configure
make
sudo make install
```

**libjpeg**

http://www.ijg.org/
```
tar zxvf jpegsrc.v7.tar.gz
cd jpegsrc.v7
./configure
make
sudo make install
```

**Imaging**

If you prefert try the binary package see the next section.

http://www.pythonware.com/products/pil/
```
tar xvf Imaging-1.1.6.tar
cd Imaging-1.1.6
sudo python setup.py build_ext -i
sudo python setup.py install
```

If every things are ok, the build summary must look likes this one:

```
--------------------------------------------------------------------
PIL 1.1.6 BUILD SUMMARY
--------------------------------------------------------------------
version       1.1.6
platform      darwin 2.6.2 (r262:71600, Apr 16 2009, 09:17:39)
              [GCC 4.0.1 (Apple Computer, Inc. build 5250)]
--------------------------------------------------------------------
--- TKINTER support ok
--- JPEG support ok
--- ZLIB (PNG/ZIP) support ok
--- FREETYPE2 support ok
--------------------------------------------------------------------
```

**Binary Imaging**

If you are on Snow Leopard you get probably this error,

```
Compiling with an SDK that doesn't seem to exist: /Developer/SDKs/MacOSX10.4u.sdk
```

It means you need to install the universal SDK 10.4, but even if you install it PIL won't works. For some reasons compile PIL to Snow Leopard is a hell. I hope soon a release of PIL will manage OS 10.6. So how to install it, just by using the binary package of the previous OS X. It works with python-2.5 and python-2.6 for OS 10.4, 10.5 and 10.6. Download this binary package:

http://pythonmac.org/packages/py25-fat/index.html

PIL-1.1.6-py2.5-macosx10.4-2007-05-18.dmg

You can not install it but from inside the dmg you can decompress the archive:

```
Contents/Packages/PIL-platlib-1.1.6-py2.5-macosx10.4.pkg/Contents/Archive.pax.gz
```

After decompression, you get a directory which contents PIL, just copy to your python site-package

```
sudo cp -R PIL* /Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/
```

I will probably drop directly the directory of PIL to the section download, it will easier, just download and move that to python.

**Astir**

Download or checkout Astir. Change to the Astir's directory, then check if every dependences are ok, by,

```
python pymir_check.py
```