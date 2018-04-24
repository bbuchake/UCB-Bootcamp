import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

from datetime import datetime, timedelta

#Function for calculating min, max, avg temps based on input dates
def calc_temps(start_dt, end_dt):
    min_temp = session.query(func.min(Measurement.tobs)).filter((Measurement.date >= start_dt) & (Measurement.date < end_dt)).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter((Measurement.date >= start_dt) & (Measurement.date < end_dt)).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter((Measurement.date >= start_dt) & (Measurement.date < end_dt)).all()
    return [min_temp[0][0], max_temp[0][0], avg_temp[0][0]]

#DB Setup
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
#Save reference to tables
Station = Base.classes.station
Measurement = Base.classes.measurement
# Create our session (link) from Python to the DB
session = Session(engine)

#Flask setup
app = Flask(__name__)

#Routes
@app.route("/")
def welcome():    
    """List all available api routes."""    
    return (        
        f"Available Routes:<br/>"        
        f"/api/v1.0/precipitation<br/>"        
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
        )

@app.route("/api/v1.0/stations")
def stations():    
    """Return a json list of stations from the dataset."""    
    # Query all stations    
    results = session.query(Station).all()    
    # Create a dictionary from the row data and append to a list 
    all_stations = []
    for station in results:
        station_dict = {}
        station_dict["station"] = station.station        
        station_dict["name"] = station.name      
        station_dict["latitude"] = station.latitude    
        station_dict["longitude"] = station.longitude    
        station_dict["elevation"] = station.elevation    
        all_stations.append(station_dict) 
   
    return jsonify(all_stations)

@app.route("/api/v1.0/precipitation")
def precipitation():    
    """Query for the dates and precipitation observations from the last year."""    
    #Query 
    year_ago = datetime.today() - timedelta(days=365) 
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_ago).all()  
    all_precipitation = []
    # Create a dictionary from the row data and append to a list of all_passengers    
    precipitation_dict = {}    
    for p in precipitation: 
        sdate = p.date.strftime('%Y-%m-%d')
        precipitation_dict[sdate] = p.prcp
        all_precipitation.append(precipitation_dict)
        
    return jsonify(all_precipitation)

@app.route("/api/v1.0/tobs")
def temp_obs():    
    """Return a json list of Temperature Observations (tobs) for the previous year"""    
    #Query 
    year_ago = datetime.today() - timedelta(days=365) 
    temperature = session.query(Measurement.date, Measurement.tobs).filter((Measurement.date > year_ago)).all()
    all_temp = []
    # Create a dictionary from the row data and append to a list of all_passengers    
    temperature_dict = {}    
    for t in temperature:
        sdate = t.date.strftime('%Y-%m-%d')
        temperature_dict[sdate] = t.tobs        
        all_temp.append(temperature_dict)
        
    return jsonify(all_temp)

@app.route("/api/v1.0/<start>")
def temperatures_s(start):    
    """Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.""" 
    end = datetime.today()
    #Call function
    temp_list = calc_temps(start, end)      
   
    return jsonify(temp_list)


@app.route("/api/v1.0/<start>/<end>")
def temperatures(start, end):    
    """Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.""" 
    if not end:
        end = date.today()
    #Call function
    temp_list = calc_temps(start, end)      
   
    return jsonify(temp_list)


if __name__ == '__main__':    
    app.run(debug=True)
