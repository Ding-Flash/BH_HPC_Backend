from flask import Flask

from background.main import update_state
from common import main_init
from router.router import router

# 主程序初始化，检测日志路径及数据库等信息
main_init.main_program_init()
update_state()

app = Flask(__name__)

#  加载路由
router(app)

if __name__ == '__main__':
    # 这项导入需要在init()函数之后，否则会报错
    from config import HOST, PORT

    app.run(
        host=HOST,
        port=PORT,
        # debug=True
    )
