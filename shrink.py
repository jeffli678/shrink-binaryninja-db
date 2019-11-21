import sqlite3
import sys
import shutil
import os

def backup(db_path):
    
    # e.g. program.bndb == > program-bk1.bndb
    full_path = os.path.abspath(db_path)
    folder, name = os.path.split(full_path)
    root, ext = os.path.splitext(name)

    bk_done = False

    for i in range(100):
        new_root = '%s-bk%d' % (root, i)
        new_name = new_root + ext
        bk_path = os.path.join(folder, new_name)
        if os.path.exists(bk_path):
            continue

        try:
            shutil.copyfile(full_path, bk_path)
        except:
            continue
        else:
            bk_done = True
            print('created backup at %s' % bk_path)
            break


    return bk_done, bk_path

def process_one_file(db_path):

    if not os.path.exists(db_path) or not os.path.isfile(db_path):
        print('DB file %s does not exist. \
            You need to practice your typing ^_^' % db_path)
        return

    # create a backup; I do not want to accidentally corrupt your db
    bk_done, bk_path = backup(db_path)
    if not bk_done:
        print('unable to backup your database, exiting...')
        return

    conn = sqlite3.connect(bk_path)
    c = conn.cursor()
    # unleash the parent foreign keys
    c.execute('update snapshot set parent=null;')
    
    # delete all but the last snapshots
    c.execute('delete from snapshot where id not in \
	         (select max(id) from snapshot);')

    # vaccum the database; otherwise the database size 
    # will not change
    c.execute('VACUUM;')

    # commit changes
    conn.commit()
    conn.close()
    
    print('replaing the original database')
    shutil.move(bk_path, db_path)

    print('Done! Please check if your work are still there. ')

def main():

    if len(sys.argv) > 1:
        for db_path in sys.argv[1 : ]:
            process_one_file(db_path)
    else:
        print('usage: python shrink.py your_db.bndb')

if __name__ == '__main__':
    main()