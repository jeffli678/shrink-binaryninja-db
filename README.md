# shrink-binaryninja-db
A Python script to shrink the size of binary ninja database while keeping the last snapshot intact. 

If you use Binary Ninja on one project intensively, you probably observe that the database size grows quickly. I have some as large as 500MB. The original file is ~50MB and I do not think my named variables and functions, as well as notes, can end up that large. So I had a look at the .bndb file itself and find a way to shrink its size while keeping the current status intact. 

Disclaimer: Although my script also makes a backup, to be 100% sure you do not lose your progress, you may want to manually create a backup! The author should not be responsible for any data loss. 

usage:

python shrink.py your_db.bndb

You should find a new file named your_db_bk1.bndb, which is (hopefully) smaller than the original file. 

How did I arrive at this script:

I run the file command against the .bndb and find it is a sqlite database. Then I open it with the sqlite DB browser. I find there is a table called snapshot. Each row contains a timestamp that corresponds to the time I saved the database. So, if there are no weird things, the binary ninja actually keeps a copy of the data every time you save the database. 

Now that it is trivial to shrink the database -- just delete all but the last one! Remember to keep the last one, otherwise, the DB no longer works. However, to actually delete any rows in this table, you need to unleash the parent foreign key constraint. If you are not familiar with this, you can search "sqlite foreign key". In the end, you need to vacuum the database to actually shrink the size. 

Discussion:

This script obviously deletes all the snapshots in your database. So it is ideal for archival purpose or when you are sure you do not need to revert back to an earlier status. 

Interestingly, although the DB contains such snapshot information, I do not find a way to revert to earlier snapshots in the GUI. I am not sure if it is possible using the API, or this functionality is under development. 

I know this is not the smallest possible database size -- the only snapshot still has some overlap with the file_data table. However, I do not find a safe way to further shrink it. Now that you should be fine with the new database size because it is already n times smaller than the original one, where n is the number of times you save the database. 

The current API does not provide a way to directly manipulate the database, so I have to create a dedicated script for it. 

I also find the database saves the full path of the input binary in the table named global. This is probably not a big deal, but be careful when you share your database with others, e.g., on the Internet. It can accidentally leak information about your local file system, e.g., your user name, pretty much in the same way as sometimes the PDB information can reveal information about the developer. 

Again, this is an undocumented way to manipulate the database, you would better be careful with it!

