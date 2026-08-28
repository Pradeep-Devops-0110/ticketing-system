from app import db
from datetime import datetime

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_type = db.Column(db.String(50), nullable=False) # Issue / Allocation / Deallocation
    user_name = db.Column(db.String(100), nullable=False)
    staff_id = db.Column(db.String(50), nullable=False)
    official_email = db.Column(db.String(120), nullable=False)
    client_email = db.Column(db.String(120), nullable=True)
    location = db.Column(db.String(100), nullable=False)
    rm_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Pending') # Pending, In-Progress, Resolved
    
    # IT Team Resolution Fields
    assigned_desktop = db.Column(db.String(100), nullable=True)
    assigned_model = db.Column(db.String(100), nullable=True)
    resolution_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)