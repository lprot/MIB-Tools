import os, sys, gzip, shutil, sqlite3

try:
    with gzip.open('vip_sys_db.sql.gz', 'rb') as f_in:
        with open('vip_sys_db.sql', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
except:
    print("vip_sys_db.sql.gz not found. Will try to open the unpacked one.")

con = sqlite3.connect("vip_sys_db.sql")

cur = con.cursor()
res = cur.execute("SELECT obj_id, obj_data FROM vipDB WHERE obj_id=156")
obj_id, obj_data = res.fetchone()
print("Train: %s" % obj_data.upper())

res = cur.execute("SELECT obj_id, obj_data FROM vipDB WHERE obj_id=100")
obj_id, obj_data = res.fetchone()
print("SW ver: %s" % obj_data.upper())

res = cur.execute("SELECT obj_id, obj_data FROM vipDB WHERE obj_id=138")
obj_id, obj_data = res.fetchone()
print("MU: %s" % obj_data.upper())

res = cur.execute("SELECT obj_id, obj_data FROM vipDB WHERE obj_id=115")
obj_id, obj_data = res.fetchone()
print("PN: %s" % obj_data.upper())

res = cur.execute("SELECT obj_id, obj_data FROM vipDB WHERE obj_id=116")
obj_id, obj_data = res.fetchone()
print("HW: %s" % obj_data.upper())

res = cur.execute("SELECT obj_id, obj_data FROM vipDB WHERE obj_id=121")
obj_id, obj_data = res.fetchone()
print("Fazit: %s" % obj_data.upper())

con.text_factory = bytes
cur = con.cursor()
res = cur.execute("SELECT obj_id, obj_data FROM vipDB WHERE obj_id=139")
obj_id, obj_data = res.fetchone()
print("Coding: %s" % obj_data.hex().upper())

input("\nPress Enter to exit...")
sys.exit(1)