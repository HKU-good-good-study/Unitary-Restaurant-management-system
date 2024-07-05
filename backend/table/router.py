from fastapi import APIRouter, BackgroundTasks, Response, status, HTTPException
from database import Database
from datetime import datetime, timedelta
import uuid
from .schemas import Order, Table

db = Database()  # Create an instance of the Database class
router = APIRouter()

                        ############################## helper functions #################################
async def get_table(id:str):
    result = await db.fetch_one("tables", {"id":f"{id}"})
    return result
async def get_order(id:uuid):
    return db.fetch_one("orders", {"id":f"{id}"})

async def get_orders_by_table(id:str) -> list:
    # id stands for table id
    orders = await get_table(id)["order"]
    temp = []
    for orderID in orders.items():
        temp.append(get_order(orderID))
    return temp

                        ############################## table methods #################################

@router.get("/all")
async def get_tables():
    tables = await db.fetch_collection("tables")
    if tables:
        for i in range(len(tables)):
            del tables[i]["_id"] # remove defualt id given by mongodb
        return tables
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No table created")

@router.get("/{id}", response_description="Get a single table by id")
async def get_table_by_id(id:str):
    table = await get_table(id)
    if table:
        del table["_id"]
        return table
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"table not found")

@router.post("/{id}")
async def create_table(id:str, table:Table):
    result = await get_table(id)
    if result: # should not exist table having the same id
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"table exists")
    
    result = await db.execute("tables", table.model_dump(), "insert")
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"table creation failed")
    
@router.put("/{id}")
async def update_table(id: str, table:Table):
    result = await db.fetch_one("tables", {"id":f"{id}"})
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"table not found")
    
    result = await db.execute("tables", {"filter":{"id":f"{id}"}, "update":{"$set":table.model_dump()}},"update")
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"table update failed")

@router.delete("/{id}")
async def delete_table(id:str):
    table = await db.fetch_one("tables",{"id":f"{id}"})
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"table not found")
    for orderID in table["order"]: # get all orders' id
        await db.execute("orders", {"id":f"{orderID}"}, "delete") # delete all orders related to tableID
    result = await db.execute("tables", {"id":f"{id}"}, "delete") # delete table from database
    if not result: # deleteion failed
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"table deletion failed")
    
                        ############################## order methods #################################

@router.put("/order/{id}")
async def create_order(id:str, order:Order):
    table = await db.fetch_one("tables", {"id":f"{id}"})
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"table not found")
    
    # now = datetime.now().strftime("%Y-%m-%d-%H:%M:%S") # time used to label accurate creation time of an order
    now = datetime.strptime(order.time, "%Y-%m-%d-%H:%M:%S").strftime("%Y-%m-%d-%H:%M:%S")
    print(now)
    table_now = now.strftime("%Y-%m-%d") # date used to label order created in a day per table
    order.id = str(uuid.uuid4())
    order.time = now
    # udpate table
    if table_now in table["order"].keys():
        table["order"][table_now].append(order.id)
    else:
        table["order"][table_now] = [order.id]
    result = await db.execute("tables",{"filter":{"id":f"{id}"}, "update":{"$set":{"order":table["order"]}}},"update" )
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"table update failed")

    # create order
    result = await db.execute("orders",order.model_dump(), "insert")
    if result:
        return order.id # give back the unique id of order to frontend

@router.delete("/order/{id}/{date}/{orderID}")
async def delete_table_order(id:str, orderID:str, date:str): 
    table = await get_table(id)
    order =await get_order(orderID)
    formated_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")


    if not table or not order:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"tableID or orderID invalid")
    print(table["order"][formated_date])
    if orderID in table["order"][formated_date]:
        table["order"][formated_date].remove(orderID)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"invalid orderID")
    
    result = await db.execute("tables",{"filter":{"id":f"{id}"}, "update":{"$set": {"order":table["order"]}}},"update")
    result2 = await db.execute("orders", {"id":f"{orderID}"},"delete")
    if not result2 and not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"table/order deletion failed")
    
@router.get("/order/{id}")
async def get_table_orders(id:str):
    try:
        orders =await get_orders_by_table(id)
        return orders
    except Exception as e:
        print(e)
        raise Exception(e)


@router.get("/order/{id}/{day}")
async def get_table_order_by_date(id, given_date):
    date = False
    duration = None
    try:
        date = datetime.strptime(given_date, "%Y-%m-%d-%H:%M:%S")
        duration = "accurate"
    except ValueError as e:
        print("converting to accurate time failed... Trying day time...")

    try:
        date = datetime.strptime(given_date, "%Y-%m-%d")
        duration = "day"
    except ValueError as e:
        print("converting to day time failed... Trying month...")
    
    try:
        date = datetime.strptime(given_date, "%Y-%m")
        duration = "month"
    except ValueError as e:
        print("converting to month time failed... Trying year...")
    
    try:
        date = datetime.strptime(given_date, "%Y")
        duration = "year"
    except ValueError as e:
        print("converting to year time failed... Time invalid")
    
    if not date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"invalid time")

    orderIDs =await get_orders_by_table(id)
    filtered_orders = []
    for orderID in orderIDs:
        order =await get_order(orderID.id)
        if duration == "year" and date-order.time <= timedelta(days=365):
            filtered_orders.append(order)
        # a navie way to calculate monthly data 
        # TODO: convert it to calendar month (nice to have)
        elif duration == "month" and date-order.time <= timedelta(days=30): 
            filtered_orders.append(order)

        elif duration == "day" and date-order.time <= timedelta(days=1):
            filtered_orders.append(order)
        
        elif duration == "accurate" and date == order.time:
            filtered_orders.append(order)

    return filtered_orders