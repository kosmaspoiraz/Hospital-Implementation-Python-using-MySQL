# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import settings
import sys, os

sys.path.append(
    os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db


def connection():
    ''' User this function to create your connections '''
    con = db.connect(settings.mysql_host, settings.mysql_user,
                     settings.mysql_passwd, settings.mysql_schema)

    return con


def mostcommonsymptoms(vax_name):

    # Create a new connection
    # Create a new connection
    con = connection()
    # Create a cursor on the connection
    cur = con.cursor()

    return [("vax_name", "result")]


def buildnewblock(blockfloor):

    # Create a new connection
    con = connection()

    # Create a cursor on the connection
    cur = con.cursor()

    return [
        ("result", ),
    ]


def findnurse(x, y):

    # Create a new connection
    con = connection()

    # Create a cursor on the connection
    cur = con.cursor()

    query = "select nurse.EmployeeID, nurse.name, on_call.BlockFloor, count(distinct(vaccination.patient_SSN)) as count from nurse, on_call, vaccination where nurse.EmployeeID = on_call.Nurse and nurse.EmployeeID = vaccination.nurse_EmployeeID  and on_call.BlockFloor = '%s' group by nurse.EmployeeID having count(distinct(vaccination.patient_SSN)) > '%s' " % (
        x, y)
    cur.execute(query)

    results = cur.fetchall()

    #list of tuples to return
    ans = []

    for row in results:
        ans.append((row[1], row[0], row[2], row[3]))

    return [("Nurse", "ID", "Floor", "Number of patients"), ans[0], ans[1]]


def patientreport(name):
    # Create a new connection
    con = connection()

    # Create a cursor on the connection
    cur = con.cursor()

    query = """
    select pt.Name, p.Name, n.Name, s.StayEnd, t.Name, t.Cost, r.RoomNumber, r.BlockFloor, r.BlockCode
    from treatment t, undergoes u, physician p, nurse n, stay s, block b, patient pt, room r
    where t.Code = u.Treatment and u.Physician = p.EmployeeID 
    and u.AssistingNurse = n.EmployeeID and u.Stay = s.StayID and s.Room = r.RoomNumber and r.BlockCode = b.BlockCode 
    and pt.Name = '%s' and pt.SSN = s.Patient and s.Patient = u.Patient""" % (
        name)

    cur.execute(query)

    results = cur.fetchall()

    return [("Patient", "Physician", "Nurse", "Date of release",
             "Treatement going on", "Cost", "Room", "Floor", "Block"),
            results[0]]
