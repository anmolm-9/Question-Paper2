from flask import Blueprint, render_template, send_from_directory, flash, redirect, url_for
from flask_login import login_required, current_user
import os
from models import Course, QuestionPaper

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    courses = Course.query.all()
    return render_template('home.html', courses=courses)

@main_bp.route('/courses/<course_code>')
@login_required
def course_papers(course_code):
    if not current_user.is_authenticated:
        flash('Please log in to access course papers.', 'error')
        return redirect(url_for('auth.login'))
    
    course = Course.query.filter_by(code=course_code).first_or_404()
    papers = QuestionPaper.query.filter_by(course_id=course.id).order_by(QuestionPaper.year.desc(), QuestionPaper.semester).all()
    
    years = {}
    for paper in papers:
        if paper.year not in years:
            years[paper.year] = {}
        if paper.semester not in years[paper.year]:
            years[paper.year][paper.semester] = []
        years[paper.year][paper.semester].append(paper)
    
    return render_template('course_papers.html', course=course, years=years)

@main_bp.route('/year-papers')
@login_required
def year_papers():
    if not current_user.is_authenticated:
        flash('Please log in to access year papers.', 'error')
        return redirect(url_for('auth.login'))
    
    courses = Course.query.all()
    papers = QuestionPaper.query.order_by(QuestionPaper.year.desc()).all()
    
    years = {}
    for paper in papers:
        if paper.year not in years:
            years[paper.year] = {}
        if paper.course.code not in years[paper.year]:
            years[paper.year][paper.course.code] = {}
        if paper.semester not in years[paper.year][paper.course.code]:
            years[paper.year][paper.course.code][paper.semester] = []
        years[paper.year][paper.course.code][paper.semester].append(paper)
    
    return render_template('year_papers.html', years=years, courses=courses)

@main_bp.route('/download/<int:paper_id>')
@login_required
def download_paper(paper_id):
    if not current_user.is_authenticated:
        flash('Please log in to download papers.', 'error')
        return redirect(url_for('auth.login'))
    
    paper = QuestionPaper.query.get_or_404(paper_id)
    return send_from_directory(
        directory=os.path.dirname(paper.file_path),
        path=os.path.basename(paper.file_path),
        as_attachment=True,
        download_name=paper.filename
    )