# 1. import Flask
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

# 2. Create an app, being sure to pass __name__

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def welcome():
    return (
        f"Welcome to weather info<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date **replace start date with actual date in YYYY-MM-DD format**<br/>"
        f"/api/v1.0/start_date/end_date **replace start date and end date with actual dates in YYYY-MM-DD format**"
    )

# 4. Define what to do when a user hits the /stations route
@app.route("/api/v1.0/stations")
def stations():
    
    print("Server received request for list of stations...")
    stations = session.query(Station.name).all()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temps():
    print("Server recieved request for temps for a year")

    yearAgo = dt.date(2017, 8 ,23) - dt.timedelta(days=365)
    last12mon = session.query(Measurement.tobs,Measurement.date).filter(Measurement.date >= yearAgo).order_by(Measurement.date).all()

    return jsonify(last12mon)

@app.route("/api/v1.0/<start>")
def tempstart(start):
    print("start date query recieved")
    dateTemp = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        group_by(Measurement.date).filter(Measurement.date >= start).all()
    
    return jsonify(dateTemp)

@app.route("/api/v1.0/<start>/<end>")
def tempstartend(start, end):
    print("start and end date query received")
    dateRange = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        group_by(Measurement.date).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    return jsonify(dateRange)

if __name__ == "__main__":
    app.run(debug=True)
