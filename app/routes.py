from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Ticket

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return render_template('dashboard.html', tickets=tickets)

@main.route('/raise-ticket', methods=['GET', 'POST'])
def raise_ticket():
    if request.method == 'POST':
        new_ticket = Ticket(
            ticket_type=request.form.get('ticket_type'),
            user_name=request.form.get('user_name'),
            staff_id=request.form.get('staff_id'),
            official_email=request.form.get('official_email'),
            client_email=request.form.get('client_email'),
            location=request.form.get('location'),
            rm_name=request.form.get('rm_name')
        )
        db.session.add(new_ticket)
        db.session.commit()
        flash('Ticket raised successfully!')
        return redirect(url_for('main.dashboard'))
    return render_template('raise_ticket.html')

@main.route('/update-ticket/<int:ticket_id>', methods=['POST'])
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    status = request.form.get('status')
    
    ticket.status = status
    if status == 'Resolved':
        ticket.assigned_desktop = request.form.get('assigned_desktop')
        ticket.assigned_model = request.form.get('assigned_model')
        ticket.resolution_notes = request.form.get('resolution_notes')
        # Logic to send email to user can be added here
        
    db.session.commit()
    return redirect(url_for('main.dashboard'))