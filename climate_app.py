import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct
import datetime as dt
from flask import Flask, jsonify



####Database Setup######
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)


@app.route("/")
def home():
    return(
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/list_start/<start><br/>"
        f"/api/v1.0/list_start_end/<start>/<end><br/>"
        f"/api/v1.0/3values_start/<start2><br/>"
        f"/api/v1.0/3values_start_end/<start2><end2>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returns in dictionary form: date as key and prcp as value"""
    # Query all passengers
    results = session.query(measurement.date, measurement.prcp, measurement.station).all()
    # Create a dictionary from the row data and append to a list of all_passengers
    all_climate = []
    for item in results:
        climate = {}
        climate["date"] = item[0]
        climate["precipitation"] = item[1]
        all_climate.append(climate)
    return jsonify(all_climate)
    #dict to list, then list to jsonify


@app.route("/api/v1.0/stations")
def stations():
    """Returns a JSON list of stations"""

     # Query all list of stations
    results2 = session.query(measurement.station).all()
    all_climate2 = []
    for station in results2:
        climate2 = {}
        climate2["station"] = station
        all_climate2.append(climate2)
    return jsonify(all_climate2)
 

@app.route("/api/v1.0/tobs")
def tobs():
# Which station had the highest number of observations?
    q =session.query(func.count(measurement.station).label("sta_ct"),measurement.station).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).all()
    hg_stat = ((q)[0][1])

#print("Station with the highest number of observations:", hg_stat)
# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram

    temp2 =session.query(measurement.tobs).\
        filter(measurement.date >= '2016-08-23').\
        filter(measurement.station == hg_stat).\
        order_by(measurement.date).all()
        
# Query all list of Temperature Observations of the past year
    all_climate3 = []
    for item in temp2:
        climate3 = {}
        climate3["Temperature"] = item[0]
        all_climate3.append(climate3)
    return jsonify(all_climate3)

@app.route("/api/v1.0/list_start/<start>")
def daterange_st(start):
# grouped by date, displayes the min avg and max of an inputed date range.
    z = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).group_by(measurement.date).all() 
 
    all_climate4 = []  
    for i in z:
        climate4 = {}
        climate4["Min Temp"] = i[0]
        climate4["Avg Temp"] = i[1]
        climate4["Max Temp"] = i[2]
        all_climate4.append(climate4)
    return jsonify(all_climate4)
 
@app.route("/api/v1.0/list_start_end/<start>/<end>")
def daterange_st_ed(start, end):
# grouped by date, displayes the min avg and max of an inputed date range.
    z = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).group_by(measurement.date).all() 
 
    all_climate4 = []  
    for i in z:
        climate4 = {}
#       climate4["Date"] = i[0]
        climate4["Min Temp"] = i[0]
        climate4["Avg Temp"] = i[1]
        climate4["Max Temp"] = i[2]
        all_climate4.append(climate4)
    return jsonify(all_climate4)
#    if end is null:
#        all()
#    else:
#        filter(measurement.date <= end).all()  

#        f"Please enter a start date and optional end date!<br/>"
#        f"date format yyyy-mm-dd"


        #for start in start_date:
        #search_term = character["superhero"].replace(" ", "").lower()

#        if search_term == canonicalized:
#            return jsonify(character)

#return jsonify({"error": "Character not found."}), 404 

@app.route("/api/v1.0/3values_start/<start2>")
def threevals_st(start2):

    y= session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start2).all()
 
 
    all_climate5 = []   
    for i in y:
        climate5 = {}
        climate5["Min Temp"] = i[0]
        climate5["Avg Temp"] = i[1]
        climate5["Max Temp"] = i[2]
        all_climate5.append(climate5)
    return jsonify(all_climate5)


@app.route("/api/v1.0/3values_start_end/<start2>/<end2>")
def threevals_st_ed(start2, end2):

    y= session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start2).filter(measurement.date <= end2).all()
 
 
    all_climate5 = []   
    for i in y:
        climate5 = {}
        climate5["Min Temp"] = i[0]
        climate5["Avg Temp"] = i[1]
        climate5["Max Temp"] = i[2]
        all_climate5.append(climate5)
    return jsonify(all_climate5)

 

if __name__ == "__main__":

    app.run(debug=True)
