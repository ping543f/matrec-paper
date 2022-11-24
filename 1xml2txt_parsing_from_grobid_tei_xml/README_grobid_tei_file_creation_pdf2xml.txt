How to convert tei-xml format from any pdf:


grobid docs: https://grobid.readthedocs.io/en/latest/References/

0. Gradle build tools must be installed in the system.
1. Install GROBID in linux or WSL or in mac using the git version. Do not install in native windows as it does not support. JDK 11 or 8+ must be installed both in 
linux or mac. for mac use brew and for linux openjdk will also do the trick.

git clone https://github.com/kermitt2/grobid.git

go to gradle folder then run the following commands

./gradlew clean install   #it can also be gradle if your system does not support gradlew command

./gradlew run

2. Download the python client for this gradle server
git clone https://github.com/kermitt2/grobid-client-python

3. open the test.py file in the python client folder and provide the path where all of your pdfs are 
4. run the python file, it will convert all the pdf files to tei-xml files and store beside the original pdf files

5. then use the tei-xml-parser to parse necessary information from the xml files like title, doi, abstract and all text of the pdf files