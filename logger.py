import os
import datetime
import traceback

class MyLogger:
  DEBUG = 0
  INFO = 1
  WARNING = 2
  ERROR = 3
  EXCEPTION = 4
  FATAL = 5
  levelMsg = ['DBG', 'INF', 'WRN', 'ERR', 'EXC', 'FTL']
  def __init__(self, filename='log', output_path=None, ext='txt', inf_postfix='_inf', err_postfix='_err', mode='a', dateformat='%Y/%m/%d %H:%M:%S', sequentially=False, put_stdout=False, with_debug=False):
    self.__dateformat = dateformat
    self.__seq = sequentially
    self.__put_stdout = put_stdout
    self.__with_debug = with_debug
    self.__mode = mode
    root = output_path if output_path is not None else os.getcwd()
    if not os.path.exists(root):
      os.mkdir(root)
    self.__fp_path = os.path.join(root, filename+'.'+ext)
    self.__fp_inf_path = os.path.join(root, filename+inf_postfix+'.'+ext)
    self.__fp_err_path = os.path.join(root, filename+err_postfix+'.'+ext)
    self.__fp = None
    self.__fp_inf = None
    self.__fp_err = None
  def set_with_debug(self, with_debug):
    self.__with_debug = with_debug
  def open(self):
    if self.__fp is None:
      self.__fp = open(self.__fp_path, self.__mode)
    if self.__fp_inf is None:
      self.__fp_inf = open(self.__fp_inf_path, self.__mode)
    if self.__fp_err is None:
      self.__fp_err = open(self.__fp_err_path, self.__mode)
  def close(self):
    if self.__fp is not None:
      self.__fp.close()
      self.__fp = None
    if self.__fp_inf is not None:
      self.__fp_inf.close()
      self.__fp_inf = None
    if self.__fp_err is not None:
      self.__fp_err.close()
      self.__fp_err = None
  def __enter__(self):
    self.open()
    if self.__seq:
      self.close()
    return self
  def __exit__(self, ex_type, ex_value, trace):
    self.close()
  def __del__(self):
    self.close()
  def __output_log(self, msg, level):
    now = datetime.datetime.now().strftime(self.__dateformat)
    msg_line = '{now} [{level}]{msg}\n'.format(now=now, level=MyLogger.levelMsg[level], msg=msg)
    if self.__fp is None:
      self.__fp = open(self.__fp_path, self.__mode)
    self.__fp.write(msg_line)
    if self.__seq:
      self.__fp.close()
      self.__fp = None
    if level <= MyLogger.WARNING:
      if self.__fp_inf is None:
        self.__fp_inf = open(self.__fp_inf_path, self.__mode)
      self.__fp_inf.write(msg_line)
      if self.__seq:
        self.__fp_inf.close()
        self.__fp_inf = None
    else:
      if self.__fp_err is None:
        self.__fp_err = open(self.__fp_err_path, self.__mode)
      self.__fp_err.write(msg_line)
      if self.__seq:
        self.__fp_err.close()
        self.__fp_err = None
    if self.__put_stdout:
      print(msg_line.strip('\n'))
  # for user
  def log(self, msg, level=None):
    level = level if level is not None else MyLogger.INFO
    self.__output_log(msg, level)
  def log_inf(self, msg):
    self.__output_log(msg, MyLogger.INFO)
  def log_wrn(self, msg):
    self.__output_log(msg, MyLogger.WARNING)
  def log_dbg(self, msg, level=None):
    if self.__with_debug:
      level = level if level is not None else MyLogger.DEBUG
      self.log(msg, level)
  def log_err(self, msg):
    self.__output_log(msg, MyLogger.ERROR)
  def log_exc(self, msg, e=None):
    if e is None:
      msg += '\n' + traceback.format_exc()
    else:
      msg += '\n' + traceback.format_tb(e.__traceback__)
    self.__output_log(msg, MyLogger.EXCEPTION)
  def log_ftl(self, msg):
    self.__output_log(msg, MyLogger.FATAL)


def test():
  current_dir = os.getcwd()
  filename = 'test'
  # 逐次オープンクローズを繰り返す場合はsequentially=True
  with MyLogger(current_dir, filename, sequentially=True, put_stdout=True) as logger:
    logger.log_inf("test1")
    logger.log_wrn("test2")
    logger.log_err("test3")
    logger.log_ftl("test4")

if __name__ == '__main__':
  test()