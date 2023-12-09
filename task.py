import datetime
import threading
import time
from pywebio.input import input, TEXT,select
from pywebio.io_ctrl import partial
from pywebio.output import put_text, put_buttons, clear,put_code,put_html,put_image,put_table
import pywebio
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

def apscheduler_init():
    # redis的连接串
    REDIS = {
        'host': '127.0.0.1',
        'port': '6379',
        'db': 15
        # ,
        # 'password':'wind369'
    }
 
    # 设置任务的存储位置为redis
    jobstores = {
        'redis': RedisJobStore(**REDIS)
    }
 
    # 设置定时任务运行的线程和进程，可选配置
    executors = {
        'default': ThreadPoolExecutor(10),  # 默认线程数
        'processpool': ProcessPoolExecutor(4)  # 默认进程
    }
 
    # 实例定时任务对象，用于定时任务的添加，修改，删除等等操作
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors)
    return scheduler

# def script_thread(script):
#     t = threading.Thread(target=execute_script_thr, kwargs={"script_name": script})
#     pywebio.session.register_thread(t)
#     t.start()
    


def run_start_emu1(btn_name):
    if btn_name == "启动模拟器1": 
        execute_script('jobs/start_emu_1.py')

def run_stop_emu1(btn_name):
    if btn_name == "关闭模拟器1": 
        execute_script('jobs/stop_emu_1.py')

def run_start_emu2(btn_name):
    if btn_name == "启动模拟器2": 
        execute_script('jobs/start_emu_2.py')

def run_stop_emu2(btn_name):
    if btn_name == "关闭模拟器2": 
        execute_script('jobs/stop_emu_2.py')
    

def execute_script(script_name):
    process = subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        put_code("正在执行脚本，请稍候...\n")
        while True:
            output = process.stdout.readline()
            if not output:
                break
            put_code(output)
    except:
        print("!not found")
    process.wait()

# def execute_script_thr(script_name):
#     process = subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     put_text("正在执行脚本，请稍候...\n")
#     while True:
#         output = process.stdout.readline()
#         if not output:
#             break
#         put_text(output)
        
#     process.wait()

def get_next_run_time(job_id):
    job = scheduler.get_job(job_id)
    if job:
        return job.next_run_time
    return None

def schedule_script(script_name, cron_expression):

    trigger = CronTrigger.from_crontab(cron_expression)
    job_id = script_name + cron_expression
    scheduler.add_job(execute_script, args=[script_name], trigger=trigger, id=job_id,jobstore='redis',misfire_grace_time=1000)
    
    next_run_time = get_next_run_time(job_id)
    
    if next_run_time:
        put_code(f"任务 {script_name} 已根据Cron表达式设置定时执行。")
        put_code(f"下一次执行时间： {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
        put_buttons(["删除任务"], onclick=partial(delete_task, jobid=job_id))
        # put_buttons(["继续添加任务"], onclick=continue_add_task)
    else:
        put_code("无法获取下一次执行时间。")
        # put_buttons(["继续添加任务"], onclick=continue_add_task)

def delete_task(btname,jobid):
    scheduler.remove_job(jobid)
    put_code("任务已删除.")

def continue_add_task(btn_name):
    if btn_name == "添加新的任务":
        script_name_options = ["jobs/start_emu_all.py", "jobs/stop_emu_all.py","jobs/start_emu_1.py", "jobs/stop_emu_1.py","jobs/start_emu_2.py", "jobs/stop_emu_2.py", "jobs/stsrt_alas_only.py", "jobs/stop_alas_only.py"]
        script_name = select("输入要执行的脚本名称：", type=TEXT, placeholder="例如：start_emu.py", options=script_name_options)
        cron_expression = input("输入Cron表达式：", type=TEXT, placeholder="例如：0 0 * * *")
        schedule_script(script_name, cron_expression)


def list_jobs(btname):
    if btname == "更新定时列表": 
        clear()  # 清除之前的文本内容
        put_image("https://patchwiki.biligame.com/images/blhx/8/8d/p5apduxz3icbyurg04zd7suo9b44j9m.png") 
        put_buttons(["启动模拟器1"], onclick=run_start_emu1).style('margin-top: 20px;width: 50%; display: inline-block')
        put_buttons(["启动模拟器2"], onclick=run_start_emu2).style('width: 50%; display: inline-block')
        put_buttons(["关闭模拟器2"], onclick=run_stop_emu2).style('width: 50%; display: inline-block;')
        put_buttons(["关闭模拟器1"], onclick=run_stop_emu1).style('width: 50%; display: inline-block;')
        put_buttons(["添加新的任务"], onclick=continue_add_task).style('width: 50%; display: inline-block')
        put_buttons(["更新定时列表"], onclick=list_jobs).style('width: 50%; display: inline-block')
    jobs = scheduler.get_jobs()
    if jobs:
        # #put_code("所有定时任务:")
        # for job in jobs:
        #     # job_info = f"{job.id} - 下一次执行时间： {job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')}"
        #     #put_code(job_info)
        #     # 为每个任务添加删除按钮
        #     #put_buttons(["删除任务"], onclick=partial(delete_task, jobid=job.id))
        #     # delete_button.style = "margin-left: 10px;"
        #     job_info = f"{job.id} - 下一次执行时间： {job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')}"
        #     put_table([
        #     [put_code(job.id),put_code(job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')),put_buttons(["删除任务"], onclick=partial(delete_task, jobid=job.id))]
        #     ])
        # 创建一个空的表格
        table_content = [['任务名称','执行时间','操作']]

        for job in jobs:
            # 将每个任务的信息添加到二维列表中
            row = [
                put_text(job.id),
                put_text(job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')),
                put_buttons(["删除任务"], onclick=partial(delete_task, jobid=job.id))
            ]
            table_content.append(row)

        # 一次性将整个表格添加到页面
        put_table(table_content)
    else:
        put_code("没有定时任务.")





def main():
    put_image("https://patchwiki.biligame.com/images/blhx/8/8d/p5apduxz3icbyurg04zd7suo9b44j9m.png") 
    put_buttons(["启动模拟器1"], onclick=run_start_emu1).style('margin-top: 20px;width: 50%; display: inline-block')
    put_buttons(["关闭模拟器1"], onclick=run_stop_emu1).style('width: 50%; display: inline-block;')
    put_buttons(["启动模拟器2"], onclick=run_start_emu2).style('width: 50%; display: inline-block')
    put_buttons(["关闭模拟器2"], onclick=run_stop_emu2).style('width: 50%; display: inline-block;')
    put_buttons(["添加新的任务"], onclick=continue_add_task).style('width: 50%; display: inline-block')
    put_buttons(["更新定时列表"], onclick=list_jobs).style('width: 50%; display: inline-block')
    list_jobs("首次更新")
# 创建后台调度器
scheduler = apscheduler_init()
scheduler.start()

if __name__ == '__main__':
    pywebio.start_server(main, port=8780, debug=False, cdn=False, auto_open_webbrowser=False)