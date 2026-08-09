from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta
from ecosphere import db
from ecosphere.models import User, WaterUsage, ElectricityUsage, WasteRecord, TreePlantation, CarbonCalculation
from ecosphere.utils import get_daily_tip, calculate_carbon_footprint

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/dashboard')
@login_required
def dashboard():
    # 1. Fetch Daily Eco Tip
    tip = get_daily_tip()
    
    # 2. Get summaries for logged-in user
    water_logs = WaterUsage.query.filter_by(user_id=current_user.id).order_by(WaterUsage.date.desc()).limit(5).all()
    electricity_logs = ElectricityUsage.query.filter_by(user_id=current_user.id).order_by(ElectricityUsage.date.desc()).limit(5).all()
    
    # Fetch aggregations
    total_water = db.session.query(db.func.sum(WaterUsage.liters)).filter_by(user_id=current_user.id).scalar() or 0
    total_electricity = db.session.query(db.func.sum(ElectricityUsage.kwh)).filter_by(user_id=current_user.id).scalar() or 0
    total_trees = db.session.query(db.func.sum(TreePlantation.quantity)).filter_by(user_id=current_user.id).scalar() or 0
    
    # Waste breakdown
    total_reduce = db.session.query(db.func.sum(WasteRecord.weight_kg)).filter_by(user_id=current_user.id, category='reduce').scalar() or 0
    total_reuse = db.session.query(db.func.sum(WasteRecord.weight_kg)).filter_by(user_id=current_user.id, category='reuse').scalar() or 0
    total_recycle = db.session.query(db.func.sum(WasteRecord.weight_kg)).filter_by(user_id=current_user.id, category='recycle').scalar() or 0
    total_waste = total_reduce + total_reuse + total_recycle
    
    # Carbon calculations
    latest_carbon = CarbonCalculation.query.filter_by(user_id=current_user.id).order_by(CarbonCalculation.date.desc()).first()
    
    # 3. Compute carbon-saving indices or ranks
    # Quick card stats
    stats = {
        'total_water': round(total_water, 1),
        'total_electricity': round(total_electricity, 1),
        'total_waste': round(total_waste, 1),
        'total_trees': int(total_trees),
        'latest_carbon': round(latest_carbon.total_emissions, 1) if latest_carbon else None
    }
    
    return render_template(
        'dashboard.html', 
        tip=tip, 
        stats=stats, 
        water_logs=water_logs, 
        electricity_logs=electricity_logs,
        latest_carbon=latest_carbon
    )

# --- Authentication Routes ---

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('main.register'))
            
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('main.register'))
            
        # Check existing user
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or Email already registered.', 'danger')
            return redirect(url_for('main.register'))
            
        # Create user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('main.login'))
            
        login_user(user, remember=remember)
        next_page = request.args.get('next')
        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

# --- Tracker Routes ---

@main.route('/trackers/water', methods=['GET', 'POST'])
@login_required
def water():
    if request.method == 'POST':
        liters = request.form.get('liters')
        date_str = request.form.get('date')
        notes = request.form.get('notes')
        
        try:
            liters = float(liters)
            log_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            new_log = WaterUsage(user_id=current_user.id, liters=liters, date=log_date, notes=notes)
            db.session.add(new_log)
            db.session.commit()
            flash('Water usage logged successfully.', 'success')
        except ValueError:
            flash('Invalid values submitted. Please try again.', 'danger')
            
        return redirect(url_for('main.water'))
        
    # Get all logs for current user
    logs = WaterUsage.query.filter_by(user_id=current_user.id).order_by(WaterUsage.date.desc()).all()
    
    # Calculate stats
    total_liters = sum(l.liters for l in logs)
    avg_liters = total_liters / len(logs) if logs else 0
    
    stats = {
        'total': round(total_liters, 1),
        'average': round(avg_liters, 1),
        'count': len(logs)
    }
    
    return render_template('water.html', logs=logs, stats=stats)

@main.route('/trackers/electricity', methods=['GET', 'POST'])
@login_required
def electricity():
    if request.method == 'POST':
        kwh = request.form.get('kwh')
        date_str = request.form.get('date')
        notes = request.form.get('notes')
        
        try:
            kwh = float(kwh)
            log_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            new_log = ElectricityUsage(user_id=current_user.id, kwh=kwh, date=log_date, notes=notes)
            db.session.add(new_log)
            db.session.commit()
            flash('Electricity usage logged successfully.', 'success')
        except ValueError:
            flash('Invalid values submitted. Please try again.', 'danger')
            
        return redirect(url_for('main.electricity'))
        
    # Get all logs for current user
    logs = ElectricityUsage.query.filter_by(user_id=current_user.id).order_by(ElectricityUsage.date.desc()).all()
    
    # Calculate stats
    total_kwh = sum(l.kwh for l in logs)
    avg_kwh = total_kwh / len(logs) if logs else 0
    
    stats = {
        'total': round(total_kwh, 1),
        'average': round(avg_kwh, 1),
        'count': len(logs)
    }
    
    return render_template('electricity.html', logs=logs, stats=stats)

@main.route('/trackers/waste', methods=['GET', 'POST'])
@login_required
def waste():
    if request.method == 'POST':
        category = request.form.get('category')
        item_name = request.form.get('item_name').strip()
        weight_kg = request.form.get('weight_kg')
        date_str = request.form.get('date')
        
        if category not in ['reduce', 'reuse', 'recycle']:
            flash('Invalid waste category.', 'danger')
            return redirect(url_for('main.waste'))
            
        try:
            weight_kg = float(weight_kg)
            log_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            new_log = WasteRecord(user_id=current_user.id, category=category, item_name=item_name, weight_kg=weight_kg, date=log_date)
            db.session.add(new_log)
            db.session.commit()
            flash('Waste activity logged successfully.', 'success')
        except ValueError:
            flash('Invalid values submitted. Please try again.', 'danger')
            
        return redirect(url_for('main.waste'))
        
    # Get all logs for current user
    logs = WasteRecord.query.filter_by(user_id=current_user.id).order_by(WasteRecord.date.desc()).all()
    
    # Calculate stats
    total_reduce = sum(l.weight_kg for l in logs if l.category == 'reduce')
    total_reuse = sum(l.weight_kg for l in logs if l.category == 'reuse')
    total_recycle = sum(l.weight_kg for l in logs if l.category == 'recycle')
    total_waste = total_reduce + total_reuse + total_recycle
    
    stats = {
        'total': round(total_waste, 2),
        'reduce': round(total_reduce, 2),
        'reuse': round(total_reuse, 2),
        'recycle': round(total_recycle, 2),
        'count': len(logs)
    }
    
    return render_template('waste.html', logs=logs, stats=stats)

@main.route('/trackers/tree', methods=['GET', 'POST'])
@login_required
def tree():
    if request.method == 'POST':
        tree_species = request.form.get('tree_species').strip()
        quantity = request.form.get('quantity')
        location = request.form.get('location').strip()
        date_str = request.form.get('date')
        
        try:
            quantity = int(quantity)
            log_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            new_log = TreePlantation(
                user_id=current_user.id, 
                tree_species=tree_species, 
                quantity=quantity, 
                location=location, 
                date=log_date
            )
            db.session.add(new_log)
            db.session.commit()
            flash('Tree plantation logged successfully.', 'success')
        except ValueError:
            flash('Invalid values submitted. Please try again.', 'danger')
            
        return redirect(url_for('main.tree'))
        
    # Get all logs
    logs = TreePlantation.query.filter_by(user_id=current_user.id).order_by(TreePlantation.date.desc()).all()
    total_trees = sum(l.quantity for l in logs)
    
    stats = {
        'total': total_trees,
        'count': len(logs)
    }
    
    return render_template('tree.html', logs=logs, stats=stats)

# --- Calculator Routes ---

@main.route('/calculator/carbon', methods=['GET', 'POST'])
@login_required
def carbon():
    latest_calc = CarbonCalculation.query.filter_by(user_id=current_user.id).order_by(CarbonCalculation.date.desc()).first()
    
    if request.method == 'POST':
        transport_km = request.form.get('transport_km', 0)
        transport_type = request.form.get('transport_type', 'walk_bike')
        electricity_kwh = request.form.get('electricity_kwh', 0)
        waste_kg = request.form.get('waste_kg', 0)
        recycling_rate = request.form.get('recycling_rate', 0)
        
        try:
            res = calculate_carbon_footprint(
                transport_km=transport_km,
                transport_type=transport_type,
                electricity_kwh=electricity_kwh,
                waste_kg=waste_kg,
                recycling_rate=recycling_rate
            )
            
            # Save results to DB
            new_calc = CarbonCalculation(
                user_id=current_user.id,
                transport_emissions=res['transport'],
                energy_emissions=res['energy'],
                waste_emissions=res['waste'],
                total_emissions=res['total'],
                date=datetime.utcnow().date()
            )
            db.session.add(new_calc)
            db.session.commit()
            flash('Carbon footprint computed and saved.', 'success')
            return redirect(url_for('main.carbon'))
        except ValueError:
            flash('Invalid form entries.', 'danger')
            
    return render_template('carbon.html', latest=latest_calc)

# --- User Profile Route ---

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not email:
            flash('Email cannot be empty.', 'danger')
            return redirect(url_for('main.profile'))
            
        # Check email uniqueness
        existing_user = User.query.filter(User.email == email, User.id != current_user.id).first()
        if existing_user:
            flash('Email is already in use by another account.', 'danger')
            return redirect(url_for('main.profile'))
            
        current_user.email = email
        
        # Optional password update
        if password:
            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return redirect(url_for('main.profile'))
            current_user.set_password(password)
            
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('main.profile'))
        
    # Compile stats summary for profile page
    total_water = db.session.query(db.func.sum(WaterUsage.liters)).filter_by(user_id=current_user.id).scalar() or 0
    total_electricity = db.session.query(db.func.sum(ElectricityUsage.kwh)).filter_by(user_id=current_user.id).scalar() or 0
    total_trees = db.session.query(db.func.sum(TreePlantation.quantity)).filter_by(user_id=current_user.id).scalar() or 0
    total_waste = db.session.query(db.func.sum(WasteRecord.weight_kg)).filter_by(user_id=current_user.id).scalar() or 0
    
    stats = {
        'water': round(total_water, 1),
        'electricity': round(total_electricity, 1),
        'trees': int(total_trees),
        'waste': round(total_waste, 1),
        'join_date': current_user.created_at.strftime('%B %d, %Y')
    }
    
    return render_template('profile.html', stats=stats)
