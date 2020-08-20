import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify



engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Flask Setup
app = Flask(__name__)




session.query(Measurement.date).order_by(Measurement.date.desc()).first()
recent_date= session.query(Measurement.date).order_by(Measurement.date.desc()).first()
recent_date
date_one_year_ago = dt.date(2017,8,23) - dt.timedelta(365)
date_one_year_ago



last_12_months = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>date_one_year_ago).all()


prcp_12_months = pd.DataFrame(last_12_months)
prcp_12_months
prcp_12_months = prcp_12_months.set_index('date')
prcp_12_months



prcp_12_months_sort = prcp_12_months.sort_values('date')
prcp_12_months_sort


# Flask Routes
@app.route("/")
def home():
    return(
        f"All Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement).all()
    prcp_12months = []
    for result in results:
        prcp_12months_dict = {}
        prcp_12months_dict["date"] = result.date
        prcp_12months_dict["prcp"] = result.prcp
        prcp_12months.append(prcp_12months_dict)
    # Returning the JSON respresentation of the dictionary    
    return jsonify(prcp_12months)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations_list = list(np.ravel(results))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    top_station_id = "USC00519281"
    top_station_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.station==top_station_id).all()
    date_one_year_ago = "2017,8,23"
    temp_obvs_prev_year = session.query(Measurement.date,Measurement.station, Measurement.tobs).filter(Measurement.date > date_one_year_ago).all()
    return jsonify(temp_obvs_prev_year)

# # @app.route("/api/v1.0/<start>")
# # @app.route("/api/v1.0/<start>/<end>")


if __name__ == '__main__':
    app.run(debug=True)

