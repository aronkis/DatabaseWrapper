from flask_paginate import Pagination, get_page_args
from flask import Flask, request, render_template, redirect, url_for
from includes.Database import Database

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

def getData(rows, page, offset=0, per_page=5):
    offset = (page - 1) * per_page
    return rows[offset: offset + per_page: 1]

@app.route("/", methods=["GET", "POST"])
def homepage():
    options = ["Persoana", "Deviz", "Piesa", "Piesa_Deviz"]
    selected_option = None
    if request.method == "POST":
        selected_option = request.form.get("dropdown")
        button_pressed = request.form.get("action")
        if button_pressed == "List":
            return redirect(url_for("listTable", 
                                    table_name=selected_option, 
                                    page=1)
                            )
        elif button_pressed == "Update":
             return redirect(url_for("selectUpdate", table_name=selected_option))
        elif button_pressed == "Alter":
             return redirect(url_for("selectAlter", table_name=selected_option))
        elif button_pressed == "Problems":
             return redirect(url_for("selectProblem"))

    return render_template("homepage.html", options=options, 
                           selected_option=selected_option)

@app.route("/list/<table_name>", methods=["GET", "POST"])
def listTable(table_name):
    db = Database("localhost", "root", "asdasdasd1", "Atelier")
    db.connect()
    rows = db.getAllFromTable(table_name)
    db.disconnect()
    
    page, per_page, offset = get_page_args(page="page",
                                           per_page_parameter="per_page")
    per_page = 5
    total = len(rows)
    column_names = rows[0].keys() if rows else []
    
    paginationData = getData(rows, page, offset, per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, 
                            css_framework="bootstrap4")
    return render_template("list.html", paginationData=paginationData, 
                           page=page, per_page=per_page, pagination=pagination,
                           column_names=column_names, table_name=table_name)

@app.route("/listselectedproblem/<selected_problem>", methods=["GET", "POST"])
def listProblemResults(selected_problem):
    db = Database("localhost", "root", "asdasdasd1", "Atelier")
    db.connect()
    data = db.callProcedure(selected_problem.replace(" ", ""))
    db.disconnect()
    
    page, per_page, offset = get_page_args(page="page",
                                           per_page_parameter="per_page")
    per_page = 5
    total = len(data)
    column_names = data[0].keys() if data else []
    
    paginationData = getData(data, page, offset, per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, 
                            css_framework="bootstrap4")
    return render_template("listselectedproblem.html", paginationData=paginationData, 
                           page=page, per_page=per_page, pagination=pagination,
                           column_names=column_names, selected_problem=selected_problem)

@app.route("/selectupdate/<table_name>", methods=["GET", "POST"])
def selectUpdate(table_name):
    options = ["Add", "Delete by value", "Delete by condition", 
               "Update by value", "Update by condition"]
    selected_option = None

    if request.method == "POST":
        selected_option = request.form.get("dropdown")
        if selected_option == "Add":
            switch = {
                'Persoana': "addPerson",
                'Deviz': "addDevice",
                'Piesa': "addComponent",
                'Piesa Deviz': "addDeviceComponent" 
            }
            return redirect(url_for(switch[table_name], table_name=table_name))
        else:
            switch = {
                'Delete by value': "deleteByValue",
                'Delete by condition': "deleteByCondition",
                'Update by value': "updateByValue",
                'Update by condition': "updateByCondition" 
            }
            return redirect(url_for(switch[selected_option], table_name=table_name))

    return render_template("selectupdate.html", options=options, 
                           selected_option=selected_option)

@app.route("/selectalter/<table_name>", methods=["GET", "POST"])
def selectAlter(table_name):
    options = ["Add column", "Delete column", "Modify column"]
    selected_option = None

    if request.method == "POST":
        selected_option = request.form.get("dropdown")
        switch = {
            'Add column': "addColumn",
            'Delete column': "deleteColumn",
            'Modify column': "modifyColumn",
        }
        return redirect(url_for(switch[selected_option], table_name=table_name))

    return render_template("selectalter.html", options=options, 
                           selected_option=selected_option)

@app.route("/selectproblem", methods=["GET", "POST"])
def selectProblem():
    options = ["Problema 3A", "Problema 3B", "Problema 4A",
               "Problema 4B", "Problema 5A", "Problema 5B",
               "Problema 6A", "Problema 6B"]
    selected_option = None

    if request.method == "POST":
        selected_option = request.form.get("dropdown")
        return redirect(url_for("listProblemResults", 
                                selected_problem=selected_option))

    return render_template("selectproblem.html", options=options, 
                           selected_option=selected_option)

@app.route("/addperson/<table_name>", methods=["GET", "POST"])
def addPerson(table_name):
    if request.method == 'POST':
        person_id = request.form['person_id']
        person_name = request.form['person_name']
        person_email = request.form['person_email']
        person_address = request.form['person_address']
        
        db = Database("localhost", "root", "asdasdasd1", "Atelier")
        db.connect()
        db.addPerson(person_id, person_name, person_email, person_address)
        db.disconnect()
 
    return render_template("addperson.html", table_name=table_name)

@app.route("/adddevice/<table_name>", methods=["GET", "POST"])
def addDevice(table_name):                 
    if request.method == 'POST':
        device_id = request.form['device_id']
        device_client_id = request.form['device_client_id']
        device_operator_id = request.form['device_operator_id']
        device_name = request.form['device_name']
        device_entry_date = request.form['device_entry_date']
        device_confirmation_date = request.form['device_confirmation_date']
        device_finalization_date = request.form['device_finalization_date']
        device_symptoms = request.form['device_symptoms']
        device_defect= request.form['device_defect']
        device_repair_time = request.form['device_repair_time']
        device_repair_hours = request.form['device_repair_hours']
        device_total = request.form['device_total']

        db = Database("localhost", "root", "asdasdasd1", "Atelier")
        db.connect()
        db.addDevice(
            device_id, device_client_id, device_operator_id, device_name, 
            device_entry_date, device_confirmation_date, 
            device_finalization_date, device_symptoms, device_defect, 
            device_repair_time, device_repair_hours, device_total
        )
        db.disconnect()
 
    return render_template("adddevice.html", table_name=table_name)

@app.route("/addcomponent/<table_name>", methods=["GET", "POST"])
def addComponent(table_name):
    if request.method == 'POST':
        id_p = request.form['id_p']
        description = request.form['description']
        manufacturer = request.form['manufacturer']
        stock_cantity = request.form['stock_cantity']
        price_catalog = request.form['price_catalog']
        
        db = Database("localhost", "root", "asdasdasd1", "Atelier")
        db.connect()
        db.addComponent(id_p, description, manufacturer, 
                        stock_cantity, price_catalog)
        db.disconnect()
 
    return render_template("addcomponent.html", table_name=table_name)

@app.route("/adddevicecomponent/<table_name>", methods=["GET", "POST"])
def addDeviceComponent(table_name):
    if request.method == 'POST':
        id_d = request.form['id_d']
        id_p = request.form['id_p']
        quantity = request.form['quantity']
        retail_price = request.form['retail_price']
        db = Database("localhost", "root", "asdasdasd1", "Atelier")
        db.connect()
        db.addDeviceComponent(id_d, id_p, quantity, retail_price)
        db.disconnect()
 
    return render_template("adddevicecomponent.html", table_name=table_name)

@app.route("/deletebyvalue/<table_name>", methods=["GET", "POST"])
def deleteByValue(table_name):
    if request.method == 'POST':
        column_name = request.form['column_name']
        row_value = request.form['row_value']

        db = Database("localhost", "root", "asdasdasd1", "Atelier")
        db.connect()
        db.deleteFromTableByValue(table_name, column_name, row_value)
        db.disconnect()
 
    return render_template("deletebyvalue.html", table_name=table_name)

@app.route("/deletebycondition/<table_name>", methods=["GET", "POST"])
def deleteByCondition(table_name):
    if request.method == 'POST':
        condition = request.form['condition']

        db = Database("localhost", "root", "asdasdasd1", "Atelier")
        db.connect()
        db.deleteFromTableByCondition(table_name, condition)
        db.disconnect()
 
    return render_template("deletebycondition.html", table_name=table_name)

@app.route("/updatebyvalue/<table_name>", methods=["GET", "POST"])
def updateByValue(table_name):
    if request.method == 'POST':
        column_name = request.form['column_name']
        row_value = request.form['row_value']
        update_values = request.form['update_values']
        update_list = update_values.replace(", ", "").split(",")
        db = Database("localhost", "root", "asdasdasd1", "Atelier")
        db.connect()
        db.updateTableByValue(table_name, column_name, row_value, update_list)
        db.disconnect()
 
    return render_template("updatebyvalue.html", table_name=table_name)

@app.route("/updatebycondition/<table_name>", methods=["GET", "POST"])
def updateByCondition(table_name):
    if request.method == 'POST':
        condition = request.form['condition']
        update_values = request.form['update_values']
        update_list = update_values.replace(", ", "").split(",")
        db = Database("localhost", "root", "asdasdasd1", "Atelier")
        db.connect()
        db.updateTableByCondition(table_name, condition, update_list)
        db.disconnect()
 
    return render_template("updatebycondition.html", table_name=table_name)

@app.route("/addcolumn/<table_name>", methods=["GET", "POST"])
def addColumn(table_name):
    if request.method == 'POST':
        column_name = request.form['column_name']
        data_type = request.form['data_type']
        db = Database("localhost", "root", "asdasdasd1", "Atelier")
        db.connect()
        db.addColumn(table_name, column_name, data_type)
        db.disconnect()
 
    return render_template("addcolumn.html", table_name=table_name)

@app.route("/deletecolumn/<table_name>", methods=["GET", "POST"])
def deleteColumn(table_name):
    if request.method == 'POST':
        column_name = request.form['column_name']
        db = Database("localhost", "root", "asdasdasd1", "Atelier")
        db.connect()
        db.deleteColumn(table_name, column_name)
        db.disconnect()
 
    return render_template("deletecolumn.html", table_name=table_name)

@app.route("/modifycolumn/<table_name>", methods=["GET", "POST"])
def modifyColumn(table_name):
    if request.method == 'POST':
        column_name = request.form['column_name']
        data_type = request.form['data_type']
        db = Database("localhost", "root", "asdasdasd1", "Atelier")
        db.connect()
        db.modifyColumn(table_name, column_name, data_type)
        db.disconnect()
 
    return render_template("modifycolumn.html", table_name=table_name)

if __name__ == "__main__":
    app.run()