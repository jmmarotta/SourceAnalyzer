# SourceAnalyzer 

[GitHub Repo Link](https://github.com/dcaust1n/SourceAnalyzer.git)

- A locally run application that demonstrates different matching algorithms 
- Current release compares files as a one to one connection
- Outputs given percentage of similarity and highlighted visualization of the matching sections of input documents
- Supports, raw text files and python files currently, with C++ and java planned in the future releases

## Getting Started

#### STEP 1 

it is recommended to create and navigate to virtual environemnt using python to run script

    python3 -m venv <dir> 
    source <dir>/bin/activate

#### STEP 2

run command

    pip install source_analyzer


###### OR

Download the latest built compressed file release from [source_analyzer-X.X.X.tar.gz](https://github.com/dcaust1n/SourceAnalyzer/tree/master/dist)



then run command

    pip3 install /<path_to_file>/source_analyzer-0.1.18.tar.gz


#### STEP 3

run command

    source_analyzer

## Known Errors/Issues
Errors- 
Multiple of the same substring found in file B will return only the first instance of that substring. 

Issues- 
Python files featuring a heavy amount of print statements may cause skewed data. 


## Project Group: Codalyzers
- Djoni Austin | @dcaust1n
- Jared Dawson | @lukinator1
- Shane Eising | @seising99
- Julian Marott | @jmmoratta

## References: 
https://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf


