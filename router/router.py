import datetime
import logging

from flask import jsonify, request

import state
from router.get_data import get_node_data, get_queue_data, get_job_wait_top, get_job_run_top, get_job_list, \
    get_node_list

date_format = '%Y-%m-%d'


def router(app):
    """
    该函数用来定义后端所有路由
        url:'/stat/<cluster>/all',从路径传入<cluster>参数,显示集群整体统计信息,节点，核心状态
        url:'/stat/<cluster>/job_wait',从路径传入<cluster>参数,get请求传入top参数，返回等待时间的topk任务
        url:'/stat/<cluster>/job_run',从路径传入<cluster>参数,get请求传入top参数，返回运行时间的topk任务
        url:'/stat/<cluster>/node_data',从路径传入<cluster>参数,get请求传入from及to参数，若to未传入，则默认当前时间，from使用"2020-12-23"格式传入
                                        返回时间范围内的节点、核心使用率
        url:'/stat/<cluster>/node_data',从路径传入<cluster>参数,get请求传入from及to参数，若to未传入，则默认当前时间，from使用"2020-12-23"格式传入
                                        返回时间范围内的用户、作业数量
        url:'/stat/<cluster>/job_list',从路径传入<cluster>参数，返回当前队列中的任务
        url:'/stat/<cluster>/node_list',从路径传入<cluster>参数，返回当前节点状态
    :param app: 传入flask实例
    :return:
    """

    @app.route('/stat/<cluster>/all')
    def handle_state_queue(cluster):
        return jsonify({
            **state.entire_cluster_state.to_dict(),
            **state.entire_queue_state.to_dict(),
            "state": {
                **state.all_cluster_state['cpu_cluster_state'].to_dict(),
                **state.all_cluster_state['gpu_cluster_state'].to_dict(),
            },
            "queue": {
                **state.all_queue_state['cpu_queue_state'].to_dict(),
                **state.all_queue_state['gpu_queue_state'].to_dict(),
            }
        })

    @app.route('/stat/<cluster>/job_wait')
    def handle_queue_wait(cluster):
        try:
            top_num = request.args.get('top')
            job_wait_list = get_job_wait_top(int(top_num))
            return jsonify(job_wait_list), 200
        except Exception as e:
            logging.exception(e)
            return jsonify({'msg': '数据获取错误'}), 400

    @app.route('/stat/<cluster>/job_run')
    def handle_queue_run(cluster):
        try:
            top_num = request.args.get('top')
            job_run_list = get_job_run_top(int(top_num))
            return jsonify(job_run_list), 200
        except Exception as e:
            logging.exception(e)
            return jsonify({'msg': '数据获取错误'}), 400

    @app.route('/stat/<cluster>/node_data', methods=['GET'])
    def handle_node_data(cluster):
        date_from = request.args.get("from")
        if date_from is None:
            return jsonify({'response': '未指定起始日期'}), 400
        now_time = datetime.datetime.now().strftime(date_format)
        date_to = request.args.get("to", default=now_time)

        data_list = get_node_data(date_from, date_to)

        if len(data_list['info']) != 0:
            return jsonify(data_list), 200
        else:
            return jsonify({'msg': '数据获取错误'}), 400

    @app.route('/stat/<cluster>/queue_data', methods=['GET'])
    def handle_queue_data(cluster):
        date_from = request.args.get("from")
        if date_from is None:
            return jsonify({'response': '未指定起始日期'}), 400
        now_time = datetime.datetime.now().strftime(date_format)
        date_to = request.args.get("to", default=now_time)

        data_list = get_queue_data(date_from, date_to)

        if len(data_list['info']) != 0:
            return jsonify(data_list), 200
        else:
            return jsonify({'msg': '数据获取错误'}), 400

    @app.route('/stat/<cluster>/job_list', methods=['GET'])
    def handle_job_list(cluster):
        try:
            job_list = get_job_list()
            return jsonify(job_list), 200
        except Exception as e:
            logging.exception(e)
            return jsonify({'msg': '数据获取错误'}), 400

    @app.route('/stat/<cluster>/node_list', methods=['GET'])
    def handle_node_list(cluster):
        try:
            node_list = get_node_list()
            return jsonify(node_list), 200
        except Exception as e:
            logging.exception(e)
            return jsonify({'msg': '数据获取错误'}), 400
