from jenkinsapi.jenkins import Jenkins
from datetime import datetime
from time import strftime, localtime
import sqlite3


def get_datetime():
    time = datetime.now()
    print(time)
    return time


def get_server_instance():
    my_url = 'http://localhost:8080'
    #my_url = "https://github.com/profmcdan/SeedstarPythonJenkins"
    server = Jenkins(my_url, username ='profmcdan', password ='dan9291@futa')
    return server

if __name__ == '__main__':
    print(get_server_instance().version)


def get_job_details():
    """Get job details of each job that is running on the Jenkins instance"""
    server = get_server_instance()
    for j in server.get_jobs():
        job_instance = server.get_job(j[0])
        job_name = job_instance.name
        job_description = job_instance.get_description()
        job_is_running = job_instance.is_running()
        job_is_enabled = job_instance.is_enabled()

        if job_is_running:
            job_status_running = 'Running'
        else:
            job_status_running = 'Not running'
        if job_is_enabled:
            job_status_enabled = 'Enabled'
        else:
            job_status_enabled = 'Disabled'

        # Update DB
        d = update_db(job_name, job_description, job_status_enabled, job_status_running)
        print(d)


def update_db(name, desc, enable_status, running_status):
    try:
        print('{0}, {3}, {1}, {2}'.format(name, enable_status, running_status, desc))
        time = strftime("%I:%M:%S %p", localtime())
        date = strftime("%a, %d %b %Y", localtime())
        print('job queried at {0} on {1}'.format(time, date))
        data = [name, desc, enable_status, running_status, date, time]
        conn = sqlite3.connect('Jobs.db')
        c = conn.cursor()
        c.execute("INSERT INTO jobs VALUES (?,?,?,?,?,?)", data)
        conn.commit()
        conn.close()
    except:
        return 'Database Error'
    return 'Success'


def get_records():
    conn = sqlite3.connect('Jobs.db')
    c = conn.cursor()
    for row in c.execute("SELECT * FROM jobs ORDER BY date "):
        print(row)
    conn.close()


def create_db():
    conn = sqlite3.connect('Jobs.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE jobs
                 (name text, description text, enable_status text, running_status text, date text, time text)''')

    conn.commit()
    conn.close()
