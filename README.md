## Development: Android Architecture Analyzer
***

### Table of Contents
* [Project Summary](#project-summary)
* [Requirements](#requirements)
* [Installation](#installation)
  * [Android Architecture Analyzer Installation](#install-android-architecture-analyzer)
  * [Anaconda Installation](#install-anaconda)
  * [ArchStudio Installation](#install-archstudio)
* [Usage](#usage)
  * [Analyze an Android Application Manifest](#analyze-an-android-applications-manifest)
  * [Analyze an Android Application's Architecture using Source Code](#analyze-an-android-applications-architecture-using-source-code)
* [Known Limitations, Bugs, and Issues](#known-limitations-bugs-and-issues)

***

### Project Summary
The Android Architecture Analyzer generates a an xADL architecture description by analyzing the manifest file and the source code of an Android application. The tool extracts the components, interfaces, and interactions between components. The generated xADL file can be loaded into ArchStudio to visually observe and interact with the architecture of the software system.

***

### Requirements
The software requirements needed to use this project are listed below.
* **Mandatory**
    * Anaconda
        * Used to enable distribution of the Android Architecture Analyzer environment across operating systems
* **Optional**
    * ArchStudio
        * Used to enable visualization of the generated xADL file and interaction with the archicture
    * Git
        * Used to clone the Android Architecture Analyzer project 

***

### Installation
The following section serves to provide information regarding the installation process for the Android Architecture Analyzer and its related requirements.

#### Install Android Architecture Analyzer
The Android Archicture Analyzer tool may be installed using two different methods listed below:

* **Download ZIP**
    1. Navigate to the project [Github Repository](https://github.com/cpear98/466_project)
    2. Select the `Code` drop-down menu
    3. Select the `Download ZIP` option
    4. Once the file download has been completed, extract the folder into the desired location.
* **Clone Project Repository**
    1. Navigate to the project [Github Repository](https://github.com/cpear98/466_project)
    2. Select the `Code` drop-down menu
    3. Copy the project link using either `HTTPS` or `SSH`
    4. Execute the command `git clone link` in a terminal where `link` is replaced with the link copied in Step 3

Upon completing installation of the Android Architecture Analyzer tool, the project contents should appear as follows:

```bash
├── 466_project/
│   ├── data/
│   │   ├── simple_manifest/
│   │   └──   └── AndroidManifest.xml
│   ├── src/
│   │   ├── entities.py
│   │   ├── main.py
│   │   └── manifest_parser.py
│   ├── .gitignore
│   ├── README.md
└── └── environment.yml
```


#### Install Anaconda
[Anaconda](https://www.anaconda.com/products/individual) is used by the development team to ensure portability and usability of the Android Architecture Analyzer tool across operating systems. To install Anaconda, refer to the [Anaconda Installation Instructions](https://docs.anaconda.com/anaconda/install/) and follow the instructions for your respective operating system.

Upon successfully installing Anaconda, in a terminal, navigate into the `/path/to/466_project/` folder. In this folder, execute the command 
```conda env create -f environment.yml```

This command will create a new Anaconda environment using the `environment.yml` specifications provided.

#### Install ArchStudio
An optional tool that the Android Architecture Analyzer has been tested with is [ArchStudio](http://isr.uci.edu/projects/archstudio/). ArchStudio enables Users to visualize and interact with a software architecture provided through an xADL file. To install ArchStudio, refer to the [ArchStudio Installation Instructions](http://isr.uci.edu/projects/archstudio/setup-easy.html).

***

### Usage
The Android Archicture Analyzer enables Users to analyze the desired Android application in two ways: through the application's `AndroidManifest.xml` document or through source code analysis. The methods that these can be performed are outlined below.

#### Analyze an Android Application's Manifest
To analyze an Android application's software architecture using the application's manifest file, follow the instructions below:
1. Open a new terminal
2. Overlay the Anaconda environment
    * `conda activate soft_arch`
3. Navigate to the directory that the `466_project` folder has been installed to
    * `cd /path/to/466_project/`
4. Run the Android Architecture Analyzer where `path/to/AndroidManifest.xml` is replaced with the path to the manifest file for the application that should be analyzed and `name-of-arch` is replaced with the name of the desired architecture.
    * `python3 main.py path/to/AndroidManifest.xml name-of-arch`

#### Analyze an Android Application's Architecture using the Source Code
To analyze an Android application's software architecture using the application's source code, follow the instructions below:
1. Open a new terminal
2. Overlay the Anaconda environment
    * `conda activate soft_arch`
3. Navigate to the directory that the `466_project` folder has been installed to
    * `cd /path/to/466_project/`
4. Run the Android Architecture Analyzer where `path/to/AndroidManifest.xml` is replaced with the path to the manifest file for the application that should be analyzed, `name-of-arch` is replaced with the name of the desired architecture, and `path/to/src/dir/` is the path to the directory containing the application source code
    * `python3 main.py path/to/AndroidManifest.xml name-of-arch --src path/to/src/dir/`

***

### Known Limitations, Bugs, and Issues
**TODO**