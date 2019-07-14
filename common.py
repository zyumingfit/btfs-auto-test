
import logging

logging.basicConfig(filename="detail.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%d-%M-%Y %H:%M:%S", level=logging.INFO)

class TestLog():

    def __init__(self):
        self.now_msg = None
        self.component_msg = None
        self.lvl_1_serial_num = 0
        self.lvl_2_serial_num = 0

    def test_end(self):
        self.lvl_1_serial_num = 0

    def component(self):
        return self.component_msg
    def compontent_reset(self):
        self.component_msg = None
        self.lvl_2_serial_num = 0

    def test_info(self, msg, *args, **kwargs):
        """Print test info log"""
        if msg == None:
            return
        rlog.info('-------------------->%s<-------------------' % msg)

        serial = 0
        blank = ''
        if self.component_msg != None:
            blank = '    |---->'
            serial = self.lvl_2_serial_num
        else:
            serial = self.lvl_1_serial_num

        msg = '%s%d.%s' % (blank, serial, msg)
        if len(msg) > 80:
            msg = msg[:77] + "..."
        print '%-80s' % (msg),

        if self.component_msg != None:
            self.lvl_2_serial_num += 1
        else:
            self.lvl_1_serial_num += 1

        self.now_msg = msg

    def test_result(self, result, *args, **kwargs):
        """Print test result log"""
        # If test_info has no output, test_result will not output the result.
        if self.now_msg != None:
            print "          " + result
            self.now_msg = None

    def component_info(self, msg, *args, **kwargs):
        """Print component log"""
        #Compent nesting is not supported
        if self.component_msg != None:
            return

        print "%d.%s" %(self.lvl_1_serial_num, msg)
        self.lvl_1_serial_num += 1

        self.component_msg = msg

    def print_info(self, msg, *args, **kwargs):
        """Print general log"""
        print msg

    def info(self, msg, *args, **kwargs):
        """Write info logs to log files"""
        logging.info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """Write error logs to log files"""
        logging.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """Write critical logs to log files"""
        logging.critical(msg, *args, **kwargs)


rlog = TestLog()


def result(func):
    def inner(*args, **kwargs):
        if rlog.now_msg != None:
            func(*args, **kwargs)
        else:
            rlog.test_info(func.__doc__)
            try:
                func(*args, **kwargs)
            except Exception, err:
                err = "fail, Reason:%s" % err
                #Output to the terminal
                rlog.test_result(err)
                #Output to log file
                rlog.error('-------------------->%s<-------------------' % err)
            else:
                rlog.info('-------------------->%s<-------------------' % 'success')
                rlog.test_result('success')
    return inner

def component(func):
    def inner(*args, **kwargs):
        if rlog.component() == None:
            rlog.component_info(func.__doc__)
        func(*args, **kwargs)
        rlog.compontent_reset()
    return inner

class BtfsCmd():
    def __init__(self):
        self.cmd = "./btfs/bin/btfs"
    def with_args(self, arg_string):
        return self.cmd + ' ' + arg_string
    def nohup_with_args(self,arg_string):
        return "nohup " + self.cmd + ' ' + arg_string

    def cmd_name(self):
        return self.cmd

