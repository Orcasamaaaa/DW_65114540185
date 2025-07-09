# DW_65114540185
นายณัฐจักษ์  กายชาติ  65114540185

ในส่วนหัวข้อ ที่ผมได้จะเป็น Brown University Benchmark(11)


ทำการ clone project แล้วทำการ สร้าง env

python -m venv venv #สร้าง env

.\venv\Scripts\activate #activate env

pip install -r requirements.txt

จากนั้นทำการโหลด data ตาม จาก clickhouse(Brown University Benchmark)

จากนั้นทำการสร้าง database และสร้าง table ใน clickhouse

database = mgbench, table = logs1 ,log2 ,log3 

จากนั้นทำการ lodadata ทั้ง 3 ตัวที่โหลดมาไปใส่ clickhouse
clickhouse-client --query "INSERT INTO mgbench.logs1 FORMAT CSVWithNames" < mgbench1.csv
clickhouse-client --query "INSERT INTO mgbench.logs2 FORMAT CSVWithNames" < mgbench2.csv
clickhouse-client --query "INSERT INTO mgbench.logs3 FORMAT CSVWithNames" < mgbench3.csv

จากนั้นทำการ cd เข้า project 

cd myproject 

จากนั้นทำการรันเพื่อนเปิด server

python manage.py runserver

จากนั้นไปที่ path: http://127.0.0.1:8000/hw04/
