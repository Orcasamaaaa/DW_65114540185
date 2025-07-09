from django.shortcuts import render
#from django_clickhouse import connection
from django.db import connection
from clickhouse_driver import Client
from datetime import datetime

# Create your views here.
def home(request):
    return render(request, 'realtime_app/home.html')

# def logs_view(request):
#     # ใช้ Django's database connection เพื่อรัน raw SQL query
#     with connection.cursor() as cursor:
#         cursor.execute('SELECT * FROM mgbench.logs1 LIMIT 10')
#         result = cursor.fetchall()
#
#     # ส่งผลลัพธ์ไปที่ template
#     return render(request, 'logs.html', {'logs': result})


# def logs_view(request):
#     # เชื่อมต่อกับ ClickHouse
#     client = Client('localhost')  # หรือ IP ของ ClickHouse server ของคุณ
#
#     # ดึงข้อมูลจากตาราง logs1
#     query = 'SELECT * FROM mgbench.logs1 LIMIT 10'
#     result = client.execute(query)
#
#     # ส่งข้อมูลไปที่ template
#     return render(request, 'logs.html', {'logs': result})

def logs_view(request):
    """
    ดึงข้อมูลจากตาราง ClickHouse ทั้งสามตาราง (mgbench.logs1, mgbench.logs2, mgbench.logs3)
    และจัดรูปแบบชื่อคอลัมน์ก่อนส่งไปยังเทมเพลต
    """
    try:
        # เชื่อมต่อกับ ClickHouse server
        client = Client('localhost')

        # ดึงข้อมูลจากตาราง mgbench.logs1 จำนวน 10 แถว
        query_logs1 = 'SELECT * FROM mgbench.logs1 LIMIT 10'
        logs1_data = client.execute(query_logs1)

        # ดึงข้อมูลจากตาราง mgbench.logs2 จำนวน 10 แถว
        query_logs2 = 'SELECT * FROM mgbench.logs2 LIMIT 10'
        logs2_data = client.execute(query_logs2)

        # ดึงข้อมูลจากตาราง mgbench.logs3 จำนวน 10 แถว
        query_logs3 = 'SELECT * FROM mgbench.logs3 LIMIT 10'
        logs3_data = client.execute(query_logs3)

        # กำหนดชื่อคอลัมน์สำหรับแต่ละตาราง
        # และจัดรูปแบบชื่อคอลัมน์โดยการแทนที่ '_' ด้วยช่องว่าง
        logs1_columns_raw = [
            'log_time', 'machine_name', 'machine_group', 'cpu_idle', 'cpu_nice',
            'cpu_system', 'cpu_user', 'cpu_wio', 'disk_free', 'disk_total',
            'part_max_used', 'load_fifteen', 'load_five', 'load_one',
            'mem_buffers', 'mem_cached', 'mem_free', 'mem_shared', 'swap_free',
            'bytes_in', 'bytes_out'
        ]
        logs2_columns_raw = [
            'log_time', 'client_ip', 'request', 'status_code', 'object_size'
        ]
        logs3_columns_raw = [
            'log_time', 'device_id', 'device_name', 'device_type', 'device_floor',
            'event_type', 'event_unit', 'event_value'
        ]

        # จัดรูปแบบชื่อคอลัมน์
        logs1_columns = [col.replace("_", " ") for col in logs1_columns_raw]
        logs2_columns = [col.replace("_", " ") for col in logs2_columns_raw]
        logs3_columns = [col.replace("_", " ") for col in logs3_columns_raw]

        # สร้าง context dictionary เพื่อส่งข้อมูลไปยัง template
        context = {
            'logs1': logs1_data,
            'logs2': logs2_data,
            'logs3': logs3_data,
            'logs1_columns': logs1_columns,
            'logs2_columns': logs2_columns,
            'logs3_columns': logs3_columns,
        }
        return render(request, 'logs.html', context)

    except Exception as e:
        # จัดการข้อผิดพลาดในการเชื่อมต่อหรือดึงข้อมูล
        return render(request, 'logs.html', {'error_message': f'เกิดข้อผิดพลาดในการเชื่อมต่อ ClickHouse หรือดึงข้อมูล: {e}'})
