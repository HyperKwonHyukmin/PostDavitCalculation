"""
Mast Post Assessment Blueprint (Test Version)
"""
from flask import Blueprint, render_template, request, session, flash
import os
import subprocess
from .ProjectCodes import MastPost
import threading

blueprint = Blueprint('mastpost', __name__, url_prefix='/mastpost')
baseDirectory = r'C:\Users\HHI\KHM\HiTessCloud_Flask'

@blueprint.route('/mastpost', methods=['GET', 'POST'])
# @login_required
def mastpost_calculate():
    programDirectory = os.path.join(baseDirectory, r"main\EngineeringPrograms\MastPost")
    exe_path = os.path.join(programDirectory, "PostDavitCalculation.exe")

    if request.method == 'POST':
        # HTML form 태그의 name 속성과 동일한 키값으로 데이터를 추출합니다.
        post_height = request.form.get('postHeight', '입력값 없음')
        platform_weight = request.form.get('platformWeight', '입력값 없음')

        user_id = session['userID']
        user_name = session['userName']
        user_company = session['userCompany']
        user_dept = session['userDept']

        try:
            cmd_args = [
                exe_path,
                str(post_height),
                str(platform_weight)
            ]

            result = subprocess.run(
                cmd_args,
                capture_output=True,
                text=True,
                encoding='cp949',  # 윈도우 환경에서 파싱 에러가 계속 나면 'cp949'로 변경하세요!
                errors='replace'  # 글자가 깨져도 프로그램이 죽지 않도록 방어
            )

            thread = threading.Thread(
                target=MastPost.MastPostAssessmentRun,
                args=(programDirectory, user_id, user_name, user_company, user_dept))
            thread.start()  

        except Exception as e:
            print(f"[Python Error] {str(e)}")
            flash(f"해석 엔진 실행 실패: {str(e)}")
            return render_template('blockMastPost.html', title='Hi-TESS Mast Post', calculated=False)

    else:
        # GET 요청 시 입력 가능한 프론트엔드 페이지 표시
        return render_template('blockMastPost.html', title='Mast & Post Design')
