from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)
import json

#####---------------------------
##### cu-paperinfinty.js variables

current_id = 4 
 
sales = [ 
    { 
        "id": 1,  
        "salesperson": "James D. Halpert", 
        "client": "Shake Shack", 
        "reams": 1000 
    }, 
    { 
        "id": 2,  
        "salesperson": "Stanley Hudson", 
        "client": "Toast", 
        "reams": 4000 
    }, 
    { 
        "id": 3,  
        "salesperson": "Michael G. Scott", 
        "client": "Computer Science Department", 
        "reams": 10000 
    }, 
] 
 
clients = [     
    "Shake Shack", 
    "Toast", 
    "Computer Science Department", 
    "Teacher's College", 
    "Starbucks", 
    "Subsconsious", 
    "Flat Top", 
    "Joe's Coffee", 
    "Max Caffe", 
    "Nussbaum & Wu", 
    "Taco Bell", 
];  

#####---------------------------
##### PPC.js variables
 
non_ppc_people = [ 
"Phyllis", 
"Dwight", 
"Oscar", "Creed", 
"Pam", 
"Jim", 
"Stanley", 
"Michael", 
"Kevin", 
"Kelly" 
] 
 
ppc_people = [ "Angela" ]

#####---------------------------



#Simple Homepage incase we open to the base url
@app.route('/')
def hello_world():
   return render_template('homepage.html')


#------------------------------------------------------------------------------------
# PART 2
@app.route('/infinity')
def infinity():
    return render_template('cu-paperinfinity.html', sales = sales, clients = clients)



@app.route('/save_sale', methods=['GET', 'POST'])
def save_sale():
    global sales
    global clients
    global current_id

    json_data = request.get_json()   
    salesperson = json_data["salesperson"] 
    client = json_data["client"] 
    reams = json_data["reams"] 
    
    # add new entry to array with 
    # a new id and the values the user sent in JSON
    current_id += 1
    new_sale_entry = {
        "id":  current_id,
        "salesperson": salesperson,
        "client": client,
        "reams": reams
    }
    sales.append(new_sale_entry)

    #append to clients in order to update the autocomplete
    if (client not in clients):
        clients.append(client)

    #send back the WHOLE array of data, so the view can redisplay it
    return jsonify(sales = sales, clients = clients)

@app.route('/delete_sale', methods=['GET', 'POST'])
def delete_sale():
    global sales
    global current_id

    json_data = request.get_json()   
    id_string = json_data["id"] 
    id_num = int(id_string)

    # Delete an entry with a matching Id as that in the JSON
    deleted = False
    s= 0
    while (not deleted and s<len(sales) ):
        if (sales[s]['id']== id_num):
            del sales[s]
        s+=1
    #send back the WHOLE array of data, so the view can redisplay it
    return jsonify(sales = sales)




#----------------------------------------------------------------------------------------
## PART 3
@app.route('/ppc')
def ppc():
    return render_template('ppc.html', nPPC_data = non_ppc_people, PPC_data = ppc_people)


@app.route('/add_PPC_name', methods=['GET', 'POST'])
def add_PPC_name():
    global ppc_people
    global non_ppc_people

    json_data = request.get_json()   
    name = json_data["name"] 
    
    # add new entry to array with 
    # a new id and the name the user sent in JSON
    new_name_entry = name
    ppc_people.append(new_name_entry)
    non_ppc_people.remove(new_name_entry)

    #send back the WHOLE array of data, so the client can redisplay it
    return jsonify(nPPC_data = non_ppc_people, PPC_data = ppc_people)


@app.route('/add_nPPC_name', methods=['GET', 'POST'])
def add_nPPC_name():
    global ppc_people
    global non_ppc_people

    json_data = request.get_json()   
    name = json_data["name"] 
    
    # add new entry to array with 
    # a new id and the name the user sent in JSON
    new_name_entry = name
    non_ppc_people.append(new_name_entry)
    ppc_people.remove(new_name_entry)

    #send back the WHOLE array of data, so the client can redisplay it
    return jsonify(nPPC_data = non_ppc_people, PPC_data = ppc_people)


if __name__ == '__main__':
   app.run(debug = True)




