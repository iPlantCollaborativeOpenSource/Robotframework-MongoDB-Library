import env
import os
import sys
from subprocess import call
import start_mongod


"""
Credits for Selenium2Library project for creating the original version
"""


ROBOT_ARGS = [
    '--outputdir', '%(outdir)s',
    '--escape', 'space:SP',
    '--report', 'none',
    '--log', 'none',
    #'--suite', 'Acceptance.Keywords.Textfields',
    '--loglevel', 'DEBUG',
    '--pythonpath', '%(pythonpath)s',
]
REBOT_ARGS = [
    '--outputdir', '%(outdir)s',
    '--name', 'AcceptanceSPTests',
    '--escape', 'space:SP',
    '--critical', 'regression',
    '--noncritical', 'inprogress',
]
ARG_VALUES = {'outdir': env.RESULTS_DIR, 'pythonpath': env.SRC_DIR}

mongo_db_name1 = 'test'
mongo_db_name2 = 'admin'
mongo_db_collection = 'test2013'
mongo_db_document = {"firstName": "John", "lastName": "Smith", "age": 25}


def acceptance_tests(interpreter, args):
    runner = {'python': 'pybot', 'jython': 'jybot', 'ipy': 'ipybot'}[interpreter]
    mongo_db = start_mongod.MongoTemporaryInstance()
    mongo_db.start_mongodb()
    mongo_db.mongo_create_db(mongo_db_name1, mongo_db_collection, mongo_db_document)
    mongo_db.mongo_create_db(mongo_db_name2, mongo_db_collection, mongo_db_document)
    if os.sep == '\\':
        runner += '.bat'
    execute_tests(runner, args)
    mongo_db.shutdown()
    return process_output()


def execute_tests(runner, args):
    if not os.path.exists(env.RESULTS_DIR):
        os.mkdir(env.RESULTS_DIR)
    command = [runner] + [arg % ARG_VALUES for arg in ROBOT_ARGS] + args + [env.ACCEPTANCE_TEST_DIR]
    print ''
    print 'Starting test execution with command:\n' + ' '.join(command)
    syslog = os.path.join(env.RESULTS_DIR, 'syslog.txt')
    call(command, shell=os.sep == '\\', env=dict(os.environ, ROBOT_SYSLOG_FILE=syslog))


def process_output():
    print
    if _has_robot_27():
        call(['python', os.path.join(env.RESOURCES_DIR, 'statuschecker.py'),
             os.path.join(env.RESULTS_DIR, 'output.xml')])
    rebot = 'rebot' if os.sep == '/' else 'rebot.bat'
    rebot_cmd = [rebot] + [arg % ARG_VALUES for arg in REBOT_ARGS] + \
                [os.path.join(ARG_VALUES['outdir'], 'output.xml')]
    rc = call(rebot_cmd, env=os.environ)
    if rc == 0:
        print 'All critical tests passed'
    else:
        print '%d critical test%s failed' % (rc, 's' if rc != 1 else '')
    return rc


def _has_robot_27():
    try:
        from robot.result import ExecutionResult
    except:
        return False
    return True


def _exit(rc):
    sys.exit(rc)


def _help():
    print 'Usage:  python run_tests.py python|jython [options]'
    print
    print 'See README.txt for details.'
    return 255


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        _exit(_help())
    interpreter = sys.argv[1]
    args = sys.argv[2:]
    _exit(acceptance_tests(interpreter, args))
