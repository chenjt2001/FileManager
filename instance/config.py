'''The config of app'''

ENV = 'development'
DEBUG = True
SECRET_KEY = 'dev'#import os; print(os.urandom(16))
DATABASE = 'instance/database.db'
SEND_FILE_MAX_AGE_DEFAULT = 0# Default: datetime.timedelta(hours=12)

################################################################################
TEMP_PATH = 'temp'# 临时文件夹
################################################################################
#file
DATA_DIR = r'C:\Users\珒陶\OneDrive\HONOR Magic-link'#'D:/OneDrive/' # 要浏览的数据文件夹，需要绝对路径
################################################################################
#gallery
PHOTO_DIR = r'C:\Users\珒陶\OneDrive\HONOR Magic-link\Backup\Photos'
