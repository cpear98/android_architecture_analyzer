## Development: Android Architecture Analyzer
***

### Table of Contents
* [Project Summary](#project-summary)
* [Requirements](#requirements)
* [Installation](#installation)
    * [CSE Server Installation](#cse-server-installation)
    * [Local Installation](#local-installation)
* [Usage](#usage)
  * [Analyze an Android Application's Manifest](#analyze-an-android-applications-manifest)
  * [Analyze an Android Application's Architecture using Source Code](#analyze-an-android-applications-architecture-using-source-code)
  * [Run Project Test Cases](#run-project-test-cases)
* [Known Limitations, Bugs, and Issues](#known-limitations-bugs-and-issues)

***

### Project Summary
The Android Architecture Analyzer generates an xADL architecture description by analyzing the manifest file and the source code of an Android application. The tool extracts the components, interfaces, and interactions between components. The generated xADL file can be loaded into ArchStudio to visually observe and interact with the architecture of the software system.

***

### Requirements
The software requirements needed to use this project are listed below.
* **Python 3**
    * Python 3 must be installed on the host machine
* **Mandatory for CSE Server Installation:**
    * Access to the UNL CSE Server and its compute resources
* **Optional:**
    * ArchStudio
        * An optional tool that the Android Architecture Analyzer has been tested with is [ArchStudio](http://isr.uci.edu/projects/archstudio/). ArchStudio enables Users to visualize and interact with a software architecture provided through an xADL file. To install ArchStudio, refer to the [ArchStudio Installation Instructions](http://isr.uci.edu/projects/archstudio/setup-easy.html).
    * Git
        * Used to clone the Android Architecture Analyzer project

***

### Installation
The following section serves to provide information regarding the installation process for the Android Architecture Analyzer and its related requirements. Two installation instruction sets are provided. One set discusses how to install the project onto the UNL CSE Server. The second instruction set discusses how to install the project locally.

* [CSE Server Installation](#cse-server-installation)
* [Local Installation](#local-installation)

***

#### CSE Server Installation
The following instructions serve to document the steps required to install the Android Architecture Analyzer onto the UNL CSE Server. These instructions assume that a connection has been made to the server.

##### Install Android Architecture Analyzer
The Android Archicture Analyzer tool may be installed using two different methods listed below:

* **Download ZIP**
    1. Navigate to the project [Github Repository](https://github.com/cpear98/android_architecture_analyzer) in your browser of choice
    2. Select the `Code` drop-down menu
    3. Select the `Download ZIP` option
    4. Once the file download has been completed, unzip the folder into the desired location.
    5. Upon unzipping the project, upload the project to the CSE Server
        * Note that this can be done using [SFTP](https://www.digitalocean.com/community/tutorials/how-to-use-sftp-to-securely-transfer-files-with-a-remote-server#:~:text=SFTP%2C%20which%20stands%20for%20SSH,but%20over%20a%20secure%20connection.) in a terminal or using an FTP tool such as [FileZilla](https://filezilla-project.org/)

* **Clone Project Repository**
    1. Navigate to the project [Github Repository](https://github.com/cpear98/android_architecture_analyzer)
    2. Select the `Code` drop-down menu
    3. Copy the project link using `HTTPS`
    4. Execute the command `git clone [link]` in a terminal with a CSE Server connection where `[link]` is replaced with the link copied in Step 3

Upon completing installation of the Android Architecture Analyzer tool, the project contents should appear as follows:

```bash
├── android_architecture_analyzer/
│   ├── data/
│   │   ├── simple_manifest/
│   │   └──   └── AndroidManifest.xml
│   ├── src/
│   │   ├── entities.py
│   │   ├── main.py
│   │   └── manifest_parser.py
│   ├── .gitignore
└── └── README.md
```

***

#### Local Installation
The following instructions serve to document how to install the Android Architecture Analyzer onto your local machine.

##### Install Android Architecture Analyzer
The Android Archicture Analyzer tool may be installed using two different methods listed below:

* **Download ZIP**
    1. Navigate to the project [Github Repository](https://github.com/cpear98/android_architecture_analyzer)
    2. Select the `Code` drop-down menu
    3. Select the `Download ZIP` option
    4. Once the file download has been completed, extract the folder into the desired location.
* **Clone Project Repository**
    1. Navigate to the project [Github Repository](https://github.com/cpear98/android_architecture_analyzer)
    2. Select the `Code` drop-down menu
    3. Copy the project link using either `HTTPS` or `SSH`
    4. Execute the command `git clone link` in a terminal where `link` is replaced with the link copied in Step 3

Upon completing installation of the Android Architecture Analyzer tool, the project contents should appear as follows:

```bash
├── android_architecture_analyzer/
│   ├── data/
│   │   ├── simple_manifest/
│   │   └──   └── AndroidManifest.xml
│   ├── src/
│   │   ├── entities.py
│   │   ├── main.py
│   │   └── manifest_parser.py
│   ├── .gitignore
└── └── README.md
```

***

### Usage
The Android Archicture Analyzer enables Users to analyze the desired Android application in two ways: through the application's `AndroidManifest.xml` document or through source code analysis. These methods are outlined below.

#### Analyze an Android Application's Manifest
To analyze an Android application's software architecture using the application's manifest file, follow the instructions below:

* For Users that followed the [local installation process](#local-installation):
    * Open a new terminal
* For Users that followed the [CSE Server installation proces](#cse-server-installation):
    * Open a new terminal with connection to the UNL CSE Server

1. Navigate to the directory that the `android_architecture_analyzer` folder has been installed to
    * `cd /path/to/android_architecture_analyzer/`
2. Run the Android Architecture Analyzer where `path/to/AndroidManifest.xml` is replaced with the path to the manifest file for the application that should be analyzed and `name-of-arch` is replaced with the name of the desired architecture.
    * `python3 src/main.py path/to/AndroidManifest.xml name-of-arch`
    * A working example has been provided with the project. To observe the example output, execute the command
        * `python3 src/main.py data/simple_manifest/AndroidManifest.xml test`
3. Upon successful execution, a notification will be displayed. The notification will contain information regarding the location of the generated xADL file:
    * `[SUCCESS] Output written to path/to/name-of-arch.xml`
    * In the case of the project example, navigate to the directory `output/`
    * Within this directory, the output may be observed in the `test.xml` file

#### Analyze an Android Application's Architecture using Source Code
To analyze an Android application's software architecture using the application's source code, follow the instructions below:

* For Users that followed the [local installation process](#local-installation):
    * Open a new terminal
* For Users that followed the [CSE Server installation proces](#cse-server-installation):
    * Open a new terminal with connection to the UNL CSE Server

1. Navigate to the directory that the `android_architecture_analyzer` folder has been installed to
    * `cd /path/to/android_architecture_analyzer/`
2. Run the Android Architecture Analyzer where `path/to/AndroidManifest.xml` is replaced with the path to the manifest file for the application that should be analyzed, `name-of-arch` is replaced with the name of the desired architecture, and `path/to/src/` is the path to the directory containing the application source code
    * `python3 src/main.py path/to/AndroidManifest.xml name-of-arch --src path/to/src/`
    * **Note:** For Users completing this process on the UNL CSE Server, it will be necessary to upload the desired application to the server. This can be done using [SFTP](https://www.digitalocean.com/community/tutorials/how-to-use-sftp-to-securely-transfer-files-with-a-remote-server#:~:text=SFTP%2C%20which%20stands%20for%20SSH,but%20over%20a%20secure%20connection.) in a terminal, using an FTP tool such as [FileZilla](https://filezilla-project.org/), or using git.
    * A working example that utilizes the [Blockinger](https://github.com/vocollapse/Blockinger) application has been provided with this repository. To run the working example, execute the following command:
        * `python3 src/main.py data/Blockinger/AndroidManifest.xml blockinger-arch --src data/Blockinger/src/`
3. Upon successful execution, a notification will be displayed. The notification will contain information regarding the location of the generated xADL file:
    * `[SUCCESS] Output written to path/to/name-of-arch.xml`
    * In the case of the project Blockinger example, navigate to the directory `output/`
    * Within this directory, the output may be observed in the `blockinger-arch.xml` file

#### Run Project Test Cases
To run the unit tests for the Android Architecture Analyzer follow the instructions below:

* For Users that followed the [local installation process](#local-installation):
    * Open a new terminal
* For Users that followed the [CSE Server installation proces](#cse-server-installation):
    * Open a new terminal with connection to the UNL CSE Server

1. Navigate to the directory that the `android_architecture_analyzer` folder has been installed to
    * `cd /path/to/android_architecture_analyzer/`
2. Run the command
    * `python3 -m unittest tests.runtests`
3. Python will run the `unittest` module and execute all test cases included in `/tests`. Upon completion, you should see a success message which includes the number of tests ran, execution time, and an end line containing `OK`.
***

### Known Limitations, Bugs, and Issues
* The resulting xADL architecture description will not have positioning or layout information. The nodes will need to be rearranged manually to the user's needs.
