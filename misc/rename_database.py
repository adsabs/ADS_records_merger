# Copyright (C) 2011, The SAO/NASA Astrophysics Data System
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


'''
@author: Giovanni Di Milia
'''
import MySQLdb
from time import strftime

def _move_tables(cur, from_db, to_db):
    """
    function that simply moves the tables from a db to another
    """
    #I retrieve the list of tables from the old db
    cur.execute('SHOW TABLES from %s' % from_db)
    tables = [elem[0] for elem in cur.fetchall()]
    
    #I move the tables to the new database
    print 'moving all the tables from "%s" to "%s"' % (from_db, to_db)
    for table in tables:
        cur.execute('RENAME TABLE %(old_db_name)s.%(table)s TO %(new_db_name)s.%(table)s;' % {'old_db_name':from_db, 'new_db_name':to_db, 'table':table})
    return

def _create_db_for_invenio(cur, db_name):
    """creates a database and gives the user invenio rights to it"""
    print 'Creating the database %s' % db_name
    cur.execute('CREATE DATABASE %s DEFAULT CHARACTER SET utf8;' % db_name)
    cur.execute("GRANT ALL PRIVILEGES ON %s.* TO invenio@'%%'" % db_name)
    cur.execute("GRANT ALL PRIVILEGES ON %s.* TO invenio@'localhost'" % db_name)
    return

def rename_invenio_database(host, user, passwd, from_db, to_db, backup_old_to_db=True, drop_old_to_db=False):
    """
    Function to rename the invenio database 
    It works only if the user has enough rights to execute these kind of queries 
    """
    
    #create connection to db
    try:
        db = MySQLdb.connect(host=host, user=user, passwd=passwd, db='mysql')
    except Exception, error:
        print 'Connection to database failed: %s' % error
        return
    cur = db.cursor()
    
    #retrieve list of databases
    cur.execute('SHOW DATABASES')
    databases = [elem[0] for elem in cur.fetchall()]
    
    #if the db to rename is not in the list I don't have to do anything
    if from_db not in databases:
        print '"Database to rename "%s" does not exists' % from_db
        return
    #if the destination db already exists
    if to_db in databases:
        #and I don't want to backup it
        if not backup_old_to_db:
            #and I don't want to drop it I cannot do anything
            if not drop_old_to_db:
                print 'New database "%s" already exists: you need to drop it or backup it' % to_db
                return
            else:
                print 'Dropping the database %s' % to_db
                cur.execute('DROP DATABASE %s;' % to_db)
                _create_db_for_invenio(cur, to_db)
                
        #otherwise I have to backup it 
        else:
            backup_name = to_db + '_' + strftime("%Y_%m_%d_%H_%M_%S")
            _create_db_for_invenio(cur, backup_name)
            _move_tables(cur, to_db, backup_name)        
    #otherwise I have to create it
    else:
        #I create the new database
        _create_db_for_invenio(cur, to_db)
    #finally I move the tables
    _move_tables(cur, from_db, to_db)
    
    return
    
    
    
        