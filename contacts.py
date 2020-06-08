import argparse
import sqlite3

class People:
    def __init__(self,name,number):
        self.name=name
        self.number=number

    def __repr__(self):
        return "People(?,?)",(self.name,self.number)

conn=sqlite3.connect("contacts.db")
c=conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Contacts(name text unique, number integer)")

def add_contact(people):
    with conn:
        c.execute("INSERT INTO Contacts VALUES(?,?)",(people.name,people.number))


def search_contact(name):
    c.execute("SELECT * FROM Contacts WHERE (name=?)",(name,))
    return c.fetchall()

def remove_contact(people):
    with conn:
        c.execute("DELETE FROM contacts WHERE (name=? and number=?)",(people.name,people.number))

conn.commit()

if __name__=="__main__":
    parser=argparse.ArgumentParser(prog="Contacts",
                                   usage='''
                                   use -h or --help
                                   ''',
                                   description='''
                                   --------------------------------
                                   DESCRIPTION:
                                   A tool for adding, searching or
                                   deleting a contact
                                   --------------------------------
                                   ''',
                                   epilog='Copyright @ pranav',
                                   formatter_class=argparse.RawDescriptionHelpFormatter,
                                   add_help=True)

    group=parser.add_mutually_exclusive_group()
    group.add_argument("--show","-s",help="Option for searching a contact",action="store_true")
    group.add_argument("--add","-a",help="Option for adding a contact",action="store_true")
    group.add_argument("--delete", "-d", help="Option for deleting a contact", action="store_true")
    parser.add_argument("--name","-n",help="Name of the contact",action="store",type=str)
    parser.add_argument("--number","-no",help="Number of the contact",action="store",type=int)
    arg=parser.parse_args()
    if (arg.add):
        name=arg.name
        num=arg.number
        if (name and num):
            people=People(name,num)
            add_contact(people)
            print("Successfully Added")
        else:
            print("Please Provide both name and number to add the contact.")

    elif arg.show:
        name=arg.name
        contact=search_contact(name)
        if len(contact)>0:
            print("Name: {}, Number: {}".format(contact[0][0],contact[0][1]))
        else:
            print("There are no contacts with that name.")

    elif arg.delete:
        name=arg.name
        num=arg.number
        contact=search_contact(name)
        if len(contact)>0:
            if (name and num):
                people=People(name,num)
                remove_contact(people)
                print("Successfully deleted")
            else:
                print("Please Provide both name and number to delete the contact.")
        else:
            print("There are no contacts with that name.")
