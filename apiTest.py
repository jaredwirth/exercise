import xmlrpc.client, json

# update data in json array for easy reading and looping
update_data = [
        {"id":"", "name":"Abigail Peterson", "phone":"+1 (930) 719-8403", "address":"332 Aviation Way, Los Angeles, CA 90017"},
        {"id":"", "name":"Anita Oliver", "phone":"+1 (479) 340-6265", "address":"2871 Park Avenue, Rancho Cordova, CA 95742"},
        {"id":"", "name":"Billy Kyle", "phone":"+1 (990) 741-1321", "address":"92 Holden Street, San Diego, CA 92105"},
        {"id":"", "name":"Eli Lambert", "phone":"+1 (864) 792-5015", "address":"1792 Liberty Avenue, Pomona, CA, 91766"},
        {"id":"", "name":"Marc Demo", "phone":"+1 (779) 623-8202", "address":"2999 Francis Mine, Sacramento, CA 95814"}
    ]
# new data in json array for easy reading and looping
new_data = [
        {"name":"Bruce Wayne", "phone":"+1 (555) 555-0001", "contact_address":"123 Wayne Drive, Gotham, NJ 88888"},
        {"name":"Clark Kent", "phone":"+1 (555) 555-0002", "contact_address":"321 Bugal Lane, Metropolis, NY 11111"},
        {"name":"Peter Parker", "phone":"+1 (555) 555-0003", "contact_address":"20 Ingram Street, New York, NY 11427"},
        {"name":"Bruce Banner", "phone":"+1 (555) 555-0004", "contact_address":"1682 Anywhere Avenue, San Fransico, CA, 99856"},
        {"name":"Steve Rodgers", "phone":"+1 (555) 555-0005", "contact_address":"762 Freedom Lane, Chicago, IL 12365"}
    ]

logs = open("logs.txt", "a")

# vars for connection
info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
url ="http://demo7.odoo.com"
db = "demo_saas-174_a9a946ecea29_1726715040"
username = "admin"
password = "admin"

logs.write("Program Started. Updating and Createing Data in Odoo API System\n")
logs.write("Basic information:\n")
logs.write(str(info))
logs.write("\n================================\n")

logs.write("Fetching Version Data to Test Connection...\n")
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
logs.write("Connected Version Info:\n")
versionInfo = common.version()
logs.write(str(versionInfo))
logs.write("\n================================\n")

logs.write("Fetching Unique ID#\n")
uid = common.authenticate(db, username, password, {})
logs.write("Unique Identification Number:[")
logs.write(str(uid))
logs.write("]\n================================\n")

# data object
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')


logs.write("Starting Data Updates\n")
logs.write("================================\n")

# loop through up
for data in update_data:
    #get data entry id
    logs.write("Retrieving Entry ID for: " + data["name"] + "\n")
    results = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['name', '=', data["name"]]]])
    data["id"] = results
    logs.write("ID Recieved:[" + str(results) + "]\n")

    # update pulled data
    logs.write("Sending Update Data: " + json.dumps(data))
    models.execute_kw(db, uid, password, 'res.partner', 'write', [results, {"phone": data["phone"],"contact_address":data["address"]} ])
    logs.write("================================\n")

logs.write("Adding New Data\n")
logs.write("================================\n")

# loop through and add new data
for data in new_data:
    logs.write("New Data Added: " + json.dumps(data))
    id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{"name":data["name"],"phone":data["phone"],"contact_address":data["contact_address"]} ])
    logs.write("\nNew Data ID Returned: "+ str(id))
    logs.write("\n================================\n")

logs.write("Task Completed")
logs.close()
