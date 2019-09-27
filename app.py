# Setup/infrastructure Lifted from 10.3.10 Flask with ORM

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


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
# session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"Please note that start and end must be replaced with valid dates in the format off YYYY-MM-DD.<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary of precipitation data"""
    #   * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    all_precips = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precips.append(precip_dict)

    #   * Return the JSON representation of your dictionary.
    return jsonify(all_precips)


@app.route("/api/v1.0/stations")
def stationdata():
    """Return a list of station data"""
    #   * Return a JSON list of stations from the dataset.
    # as this should be a list, I'm just grabbing the station name
    session = Session(engine)
    results = session.query(Station.name).all()
    session.close()

    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobsdata():
    """Return a list of observed temperature data for the last year of available data"""
    #   query for the dates and temperature observations from a year from the last data point.
    # * Return a JSON list of Temperature Observations (tobs) for the previous year.
    # as this should be a list, I'm just grabbing the station name
    session = Session(engine)
    results = session.query(Measurement.tobs).filter(Measurement.date>='2016-08-23').all()
    session.close()
    tobs_list = list(np.ravel(results))

    #   * Return the JSON representation of your dictionary.
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def sstart(start):
    """Return a list of precipitation data given just a start date"""
    #   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    #   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date>=start).all()
    s_only_descriptors = list(np.ravel(results))
    session.close()
    return jsonify(s_only_descriptors)



@app.route("/api/v1.0/<start>/<end>")
def startEnd(start, end):
    """Return a list of precipitation data given a start date and an end date"""
    #   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    #   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date>=start, Measurement.date<=end).all()
    session.close()
    s_e_descriptors = list(np.ravel(results))
    
    return jsonify(s_e_descriptors)



if __name__ == '__main__':
    app.run(debug=True)
