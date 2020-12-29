from config import DB_CONFIG

node_history_table_sql = '''
create table node_history
(
    id                   int(10) auto_increment primary key,
    record_time          timestamp default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP,

    cpu_running_node     int(10)   default 0                 not null,
    cpu_unavailable_node int(10)   default 0                 not null,
    cpu_total_node       int(10)   default 0                 not null,

    cpu_running_core     int(10)   default 0                 not null,
    cpu_unavailable_core int(10)   default 0                 not null,
    cpu_total_core       int(10)   default 0                 not null,

    gpu_running_node     int(10)   default 0                 not null,
    gpu_unavailable_node int(10)   default 0                 not null,
    gpu_total_node       int(10)   default 0                 not null,

    gpu_running_core     int(10)   default 0                 not null,
    gpu_unavailable_core int(10)   default 0                 not null,
    gpu_total_core       int(10)   default 0                 not null,

    unavailable_node     int(10)   default 0                 not null,
    running_node         int(10)   default 0                 not null,
    total_node           int(10)   default 0                 not null,

    unavailable_core     int(10)   default 0                 not null,
    running_core         int(10)   default 0                 not null,
    total_core           int(10)   default 0                 not null
)
    charset = utf8;
'''

job_history_table_sql = '''
create table job_history
(
    id                 int(10) auto_increment primary key,
    record_time        timestamp default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP,

    all_waiting_user int(10)   default 0                 not null,
    all_running_user int(10)   default 0                 not null,
    all_total_user         int(10)   default 0                 not null,

    cpu_waiting_user   int(10)   default 0                 not null,
    cpu_running_user   int(10)   default 0                 not null,
    cpu_total_user           int(10)   default 0                 not null,

    gpu_waiting_user   int(10)   default 0                 not null,
    gpu_running_user   int(10)   default 0                 not null,
    gpu_total_user           int(10)   default 0                 not null,

    cpu_running_job    int(10)   default 0                 not null,
    cpu_waiting_job    int(10)   default 0                 not null,
    cpu_total_job            int(10)   default 0                 not null,

    gpu_running_job    int(10)   default 0                 not null,
    gpu_waiting_job    int(10)   default 0                 not null,
    gpu_total_job            int(10)   default 0                 not null,

    all_running_job        int(10)   default 0                 not null,
    all_waiting_job        int(10)   default 0                 not null,
    all_total_job          int(10)   default 0                 not null
)
    charset = utf8;
'''


def node_history_sql_gen(cpu_running_node, cpu_unavailable_node, cpu_total_node,
                         cpu_running_core, cpu_unavailable_core, cpu_total_core,
                         gpu_running_node, gpu_unavailable_node, gpu_total_node,
                         gpu_running_core, gpu_unavailable_core, gpu_total_core,
                         running_node, unavailable_node, total_node,
                         running_core, unavailable_core, total_core):
    return f'''
                insert into {DB_CONFIG['history_node_table']} (
                cpu_running_node, cpu_unavailable_node, cpu_total_node, 
                cpu_running_core,cpu_unavailable_core, cpu_total_core, 
                gpu_running_node, gpu_unavailable_node, gpu_total_node,
                gpu_running_core, gpu_unavailable_core, gpu_total_core, 
                running_node, unavailable_node, total_node, 
                running_core, unavailable_core, total_core)
                VALUES (
                {cpu_running_node}, {cpu_unavailable_node}, {cpu_total_node},
                {cpu_running_core}, {cpu_unavailable_core}, {cpu_total_core},
                {gpu_running_node}, {gpu_unavailable_node}, {gpu_total_node},
                {gpu_running_core}, {gpu_unavailable_core}, {gpu_total_core},
                {running_node}, {unavailable_node}, {total_node},
                {running_core}, {unavailable_core}, {total_core});
    '''


def job_history_sql_gen(all_waiting_user, all_running_user, all_total_user,
                        all_running_job, all_waiting_job, all_total_job,
                        cpu_waiting_user, cpu_running_user, cpu_total_user,
                        cpu_running_job, cpu_waiting_job, cpu_total_job,
                        gpu_waiting_user, gpu_running_user, gpu_total_user,
                        gpu_running_job, gpu_waiting_job, gpu_total_job):
    return f'''
                insert into {DB_CONFIG['history_queue_table']} (
                all_waiting_user, all_running_user, all_total_user,
                all_running_job, all_waiting_job, all_total_job,
                cpu_waiting_user, cpu_running_user, cpu_total_user,
                cpu_running_job, cpu_waiting_job, cpu_total_job,
                gpu_waiting_user, gpu_running_user, gpu_total_user,
                gpu_running_job, gpu_waiting_job, gpu_total_job)
                VALUES (
                {all_waiting_user}, {all_running_user}, {all_total_user},
                {all_running_job}, {all_waiting_job}, {all_total_job},
                {cpu_waiting_user}, {cpu_running_user}, {cpu_total_user},
                {cpu_running_job}, {cpu_waiting_job}, {cpu_total_job},
                {gpu_waiting_user}, {gpu_running_user}, {gpu_total_user},
                {gpu_running_job}, {gpu_waiting_job}, {gpu_total_job})

    '''
