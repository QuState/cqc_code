## About the code in this repository

> [!NOTE]
> This repository is a work in progress--more comments and notes will be added

* The code uses minimal dependencies, in order to facilitate learning and ensure longevity
* The code behind notebooks is built incrementally in each chapter following sound dependency management principles
* The notebooks only use code dependencies in the chapter they belong to
* There will be a simulator, called Hume, that will put together all pieces, and will be usable as a standalone simulator


#### Overview of contents and structure 


<pre>
├── README.md
├── src                            # notebooks are designed to run from the src directory
│   ├── chXX
│   │   ├── chXX.ipynb             # notebook with chapter code that can be used for experimentation
│   │   ├── chXX_output.ipynb      # notebook that includes the output of chXX.ipynb after being run (can be used for comparison)
│   │   ├── chXX_exercises.ipynb   # notebook with chapter exercises and solutions
│   │   └── x.py                   # the source code introduced in each chapter
│   ├── ...
</pre>

