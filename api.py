from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from ecosphere import db
from ecosphere.models import WaterUsage, ElectricityUsage, WasteRecord, TreePlantation, CarbonCalculation

api = Blueprint('api', __name__)

@api.route('/water/trends')
@login_required
def water_trends():
    # Fetch last 7 records, then reverse to display chronologically
    logs = WaterUsage.query.filter_by(user_id=current_user.id).order_by(WaterUsage.date.desc()).limit(7).all()
    logs.reverse()
    return jsonify({
        'labels': [log.date.strftime('%b %d') for log in logs],
        'data': [log.liters for log in logs]
    })

@api.route('/electricity/trends')
@login_required
def electricity_trends():
    logs = ElectricityUsage.query.filter_by(user_id=current_user.id).order_by(ElectricityUsage.date.desc()).limit(7).all()
    logs.reverse()
    return jsonify({
        'labels': [log.date.strftime('%b %d') for log in logs],
        'data': [log.kwh for log in logs]
    })

@api.route('/waste/breakdown')
@login_required
def waste_breakdown():
    reduce_w = db.session.query(db.func.sum(WasteRecord.weight_kg)).filter_by(user_id=current_user.id, category='reduce').scalar() or 0
    reuse_w = db.session.query(db.func.sum(WasteRecord.weight_kg)).filter_by(user_id=current_user.id, category='reuse').scalar() or 0
    recycle_w = db.session.query(db.func.sum(WasteRecord.weight_kg)).filter_by(user_id=current_user.id, category='recycle').scalar() or 0
    
    return jsonify({
        'labels': ['Reduce', 'Reuse', 'Recycle'],
        'data': [round(reduce_w, 2), round(reuse_w, 2), round(recycle_w, 2)]
    })

@api.route('/tree/distribution')
@login_required
def tree_distribution():
    # Group trees by species for charting species variety
    results = db.session.query(
        TreePlantation.tree_species,
        db.func.sum(TreePlantation.quantity)
    ).filter_by(user_id=current_user.id).group_by(TreePlantation.tree_species).all()
    
    return jsonify({
        'labels': [row[0] for row in results],
        'data': [int(row[1]) for row in results]
    })

@api.route('/carbon/history')
@login_required
def carbon_history():
    logs = CarbonCalculation.query.filter_by(user_id=current_user.id).order_by(CarbonCalculation.date.desc()).limit(7).all()
    logs.reverse()
    return jsonify({
        'labels': [log.date.strftime('%b %d') for log in logs],
        'data': [log.total_emissions for log in logs]
    })
