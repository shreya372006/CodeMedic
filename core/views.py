import json
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .models import CodeSession, BugReport, Feedback
from .ai_engine import analyse_code


def home_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return redirect('accounts:login')


@login_required
def dashboard_view(request):
    sessions = CodeSession.objects.filter(user=request.user)
    total_analyses = sessions.count()
    total_bugs = BugReport.objects.filter(session__user=request.user).count()
    languages_used = sessions.values_list('language', flat=True).distinct().count()
    recent_logs = sessions[:10]

    context = {
        'username': request.user.username,
        'total_analyses': total_analyses,
        'total_bugs': total_bugs,
        'languages_used': languages_used,
        'recent_logs': recent_logs,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def workspace_view(request):
    return render(request, 'core/workspace.html')


@login_required
def analyse_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip()
        language = data.get('language', 'python')

        if not code:
            return JsonResponse({'error': 'No code provided'}, status=400)

        lines = code.split('\n')
        if len(lines) > 100:
            return JsonResponse({'error': 'Code exceeds 100 lines'}, status=400)

        bugs, error = analyse_code(code, language)

        if error:
            return JsonResponse({'error': error}, status=500)

        error_count = len(bugs)
        risk_level = calculate_risk(error_count)

        session = CodeSession.objects.create(
            user=request.user,
            language=language,
            code=code,
            risk_level=risk_level,
            error_count=error_count,
        )

        bug_objects = []
        for bug in bugs:
            b = BugReport.objects.create(
                session=session,
                line_number=bug['line'],
                bug_type=bug['type'],
                description=bug['description'],
                fix_suggestion=bug['fix'],
            )
            bug_objects.append({
                'id': b.id,
                'line': b.line_number,
                'type': b.bug_type,
                'type_display': b.get_bug_type_display(),
                'description': b.description,
                'fix': b.fix_suggestion,
            })

        return JsonResponse({
            'success': True,
            'session_id': session.id,
            'error_count': error_count,
            'risk_level': risk_level,
            'risk_display': session.get_risk_level_display(),
            'bugs': bug_objects,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def feedback_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        bug_id = data.get('bug_id')
        verdict = data.get('verdict')

        if verdict not in ['correct', 'incorrect']:
            return JsonResponse({'error': 'Invalid verdict'}, status=400)

        bug = get_object_or_404(BugReport, id=bug_id)

        feedback, created = Feedback.objects.update_or_create(
            bug_report=bug,
            defaults={
                'user': request.user,
                'verdict': verdict,
            }
        )

        return JsonResponse({
            'success': True,
            'verdict': verdict,
            'created': created,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def export_feedback_view(request):
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=403)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="codemedic_feedback.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Feedback ID', 'User', 'Bug ID', 'Bug Type',
        'Line Number', 'Description', 'Fix Suggestion',
        'Verdict', 'Language', 'Created At'
    ])

    feedbacks = Feedback.objects.select_related(
        'bug_report', 'bug_report__session', 'user'
    ).all()

    for fb in feedbacks:
        writer.writerow([
            fb.id,
            fb.user.username,
            fb.bug_report.id,
            fb.bug_report.bug_type,
            fb.bug_report.line_number,
            fb.bug_report.description,
            fb.bug_report.fix_suggestion,
            fb.verdict,
            fb.bug_report.session.language,
            fb.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        ])

    return response


def calculate_risk(error_count):
    if error_count == 0:
        return 'safe'
    elif error_count <= 2:
        return 'low'
    elif error_count <= 5:
        return 'medium'
    elif error_count <= 8:
        return 'high'
    else:
        return 'critical'


@login_required
def session_detail_view(request, session_id):
    session = get_object_or_404(CodeSession, id=session_id, user=request.user)
    bugs = session.bugs.all()
    context = {
        'session': session,
        'bugs': bugs,
    }
    return render(request, 'core/session_detail.html', context)


@login_required
def session_delete_view(request, session_id):
    session = get_object_or_404(CodeSession, id=session_id, user=request.user)
    if request.method == 'POST':
        session.delete()
        messages.success(request, 'Analysis session deleted.')
        return redirect('core:dashboard')
    return redirect('core:dashboard')

# Handle repository dashboard requests