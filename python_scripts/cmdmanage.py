from subprocess import PIPE, Popen

def cmdline(command):
    """
    This function attempts to execute the passed linux command as a string.
    Example Usage:
        cmdline('ps -ae | grep webkit_server')

    Parameters
    ----------
    command : str
        A string that represents the command to execute, followed by
        its arguments. See Example Usage above.

    Returns
    -------
    str
        The output from stdout that resulted from executing the passed
        command.
    """
    process = Popen(args=command, stdout=PIPE, shell=True)
    return process.communicate()[0].decode("utf-8")

def killWebkitServers():
    """
    This function sends kill signals to all webkit_server processes
    currently running. The webkit_server process is used for dryscrape,
    although the process is still running after the scraper script ends.
    Here we remove the webkit_server processes to free up memory.
    """
    webkitOutput = cmdline('ps -ae | grep webkit_server')
    webkitList = webkitOutput.split('\n')
    for webkitProc in webkitList:
        pid = webkitProc.split(' ')[0].strip()
        if len(pid) == 0:
            continue
        killCommand = 'kill -9 ' + pid
        cmdline(killCommand)

