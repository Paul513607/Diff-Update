# diff-update
Project realised for the Python Laboratory, 
by Samson Ioan-Paul, group 3A6 (project type A, id 6). <br> <br>

# The problem
Create an application that produces an update through differences between two binary files.
The application receives as input the current version of a binary file, as well as more
its previous version and creates a list of commands (of the type insert / delete /
change) through which one can reach from one of the previous files to the current file. List in
cause is encoded in a binary file. With that binary starting from one of the files
with older version, the newest file can be obtained. <br/> <br/>
INPUT: difupdate.py create abc.latest abc.ver1 abc.ver2 abc.ver3 <br/>
(in the case above, it is assumed that the last version is 4)
The result is a file named "abc.diff" that contains the necessary information to do so
go from version 1, 2 or 3 respectively to version 4 (latest) <br/> <br/>
INPUT: difupdate.py update abc.ver2 abc.diff <br/>
The result is that an abc.latest file obtained by applying operations of the type (insert,
delete or change bytes) on the abc.ver2 file. These operations are described in abc.diff (as
those necessary to move from version 2 to version 4 (latest). <br/> <br/>

# Usage
diff-update [options] <main_file> [other_files] <br> <br>

# Options
create <latest_file> [other_files]  Create a diff file <br>
update <version_file> <diff_file>  Update a version file <br> <br>

# Example
diff-update create abc.latest abc.ver1 abc.ver2 abc.ver3 <br>
diff-update update abc.ver1 abc.diff <br> <br>

# What does it do?
* __create__: <br>
diff-update creates a diff file by comparing the latest version with the other versions.
For each of these comparisons, it creates a diff using the Longest Common Subsequence algorithm,
and appends the diff to the diff file.<br>
* __update__: <br>
diff-update updates a version file by searching for the diff of the version file in the diff file,
and applying the diff to the version file.<br> <br>

# How does it work?
To compute the diff, diff-update uses the Longest Common Subsequence algorithm, along with a path reconstruction
algorithm to find the path of the LCS. The Longest Common Subsequence algorithm is a dynamic programming algorithm
that user a table to store the length of the LCS of two strings. The path reconstruction algorithm starts at the last
position of the table, and moves up, left or diagonally up-left, depending on the value of the current position.
If the current position is associated with a match between the two strings, the algorithm moves diagonally up-left.
If the current position is associated with a mismatch between the two strings, the algorithm moves up or left, depending
on the value of the position above or to the left (it needs to be equal to the current position's value). If both values
are the same, the algorithm choses to move left first. The path reconstruction algorithm stops when it reaches the first
position of the table. The diff is then computed by adding an 'insert' for each move up, a 'delete' for each move left, 
and a 'equal' for each move diagonally up-left. <br>
For an update, diff-update searches for the diff of the version file in the diff file, and applies the diff to the version file
by checking if the current line in the diff file starts with a '+' (insert), a '-' (delete) or a ' ' (equal). If the current
line starts with a '+', the line from the diff file is added to the final file. If the current line starts with a '-', no operation is
done for the version file and if the current line starts with a ' ', the line from the version file is added to the final file. <br> <br>

# Example of diff file
diff ./data/a2.ver1 ./data/a2.latest:
-A
 B
+D
 C
+A
 B
-D
 A
-B

The first line of the sequence in the diff file tells us on which file the diff was applies.
The next lines are the diff. The first character of each line tells us if the line is an 'insert', a 'delete' or an 'equal'.
The rest of the line is the line itself. <br> <br>

# How to install
Make sure you have a python3 interpreter installed. Then, run the script as specified above. <br> <br>

# Author
* __Name__: Samson Ioan-Paul

# References
* [diff]
  * (https://en.wikipedia.org/wiki/Diff)
* [Myers diff algorithm] 
  * (https://www.nathaniel.ai/myers-diff/)
* [Longest Common Subsequence]
  * (https://en.wikipedia.org/wiki/Longest_common_subsequence_problem)
  * (https://www.youtube.com/watch?v=sSno9rV8Rhg)
* [Python's difflib]
  * (https://docs.python.org/3/library/difflib.html)


