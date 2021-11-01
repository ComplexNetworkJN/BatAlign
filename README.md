This README describes the usage of the graphical user interface of BatAlign.


1、source network and target network.
Both networks are specified as LEDA (.gw) graphs. A typical .gw file might look like:

====== BEGIN ======
LEDA.GRAPH
void
void
-2
3
|{A}|
|{B}|
|{C}|
3
1 2 0 |{}|
1 3 0 |{}|
2 3 0 |{}|
======= END =======


2、sequence file
similarity file that includes the sequence information of proteins. Here, we used Blast bitscores. 
The similarity file is a tab-separated file with three columns where each line is in form:
====== BEGIN ======
A	D	19.5
B	E	50.6
C	F	43.8
======= END =======


3、output file
This parameter specifies the prefix each output alignment should have. 


4、population size
This parameter specifies the size of the population used by BatAlign. Generally, a larger population
size means better alignments.


5、number of iterations
This parameter specifies the number of iterations for which to run BatAlign. Generally, running BatAlign
for more generations yields higher quality alignments.


6、alpha value
This value, which is between 0 and 1 inclusive, accounts for the the weighting between the sequence similarity and 
the topological information.
If alpha = 1, which means it only uses sequence similarity.
If alpha = 0, then it uses topological information.
