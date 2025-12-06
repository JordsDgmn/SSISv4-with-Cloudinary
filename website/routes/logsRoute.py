from flask import Blueprint, render_template, send_file
import os

logsRoute = Blueprint('logs', __name__)

@logsRoute.route("/logs", methods=["GET"])
def view_logs():
    """View activity logs"""
    log_file = 'logs/activity.log'
    logs = []
    
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = f.readlines()
                logs.reverse()  # Show newest first
        except Exception as e:
            logs = [f"Error reading logs: {e}"]
    else:
        logs = ["No activity logs found"]
    
    return render_template('logs.html', logs=logs)

@logsRoute.route("/logs/download", methods=["GET"])
def download_logs():
    """Download activity logs"""
    log_file = 'logs/activity.log'
    
    if os.path.exists(log_file):
        return send_file(log_file, as_attachment=True, download_name='activity_log.txt')
    else:
        return "No logs available", 404
