from datetime import datetime
from ecosphere import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships to clean up associated records upon user deletion
    water_logs = db.relationship('WaterUsage', backref='user', lazy=True, cascade="all, delete-orphan")
    electricity_logs = db.relationship('ElectricityUsage', backref='user', lazy=True, cascade="all, delete-orphan")
    waste_logs = db.relationship('WasteRecord', backref='user', lazy=True, cascade="all, delete-orphan")
    tree_logs = db.relationship('TreePlantation', backref='user', lazy=True, cascade="all, delete-orphan")
    carbon_logs = db.relationship('CarbonCalculation', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class WaterUsage(db.Model):
    __tablename__ = 'water_usage'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    liters = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<WaterUsage {self.liters}L on {self.date}>'

class ElectricityUsage(db.Model):
    __tablename__ = 'electricity_usage'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    kwh = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ElectricityUsage {self.kwh}kWh on {self.date}>'

class WasteRecord(db.Model):
    __tablename__ = 'waste_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    # categories: 'reduce', 'reuse', 'recycle'
    category = db.Column(db.String(20), nullable=False)
    item_name = db.Column(db.String(150), nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<WasteRecord {self.category} - {self.item_name} ({self.weight_kg}kg)>'

class TreePlantation(db.Model):
    __tablename__ = 'tree_plantations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    tree_species = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    location = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TreePlantation {self.tree_species} x{self.quantity}>'

class CarbonCalculation(db.Model):
    __tablename__ = 'carbon_calculations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    transport_emissions = db.Column(db.Float, nullable=False) # kg CO2e
    energy_emissions = db.Column(db.Float, nullable=False) # kg CO2e
    waste_emissions = db.Column(db.Float, nullable=False) # kg CO2e
    total_emissions = db.Column(db.Float, nullable=False) # kg CO2e
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CarbonCalculation {self.total_emissions}kg CO2e on {self.date}>'
