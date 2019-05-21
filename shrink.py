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


def main():

    try:
        db_path = sys.argv[1]
    except:
        print('usage: python shrink.py your_db.bndb')
        return
    
    if not os.path.exists(db_path) or not os.path.isfile(db_path):
        print('DB file does not exist. You need to practice your typing ^_^')
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
 
    print('Done! Please check if your work are still there. ')

if __name__ == '__main__':
    main()