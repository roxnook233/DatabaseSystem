# 데이터 삽입, 삭제, 검색
import pymysql

# MySQL 연결
dbMadang = pymysql.connect(
    host='192.168.56.4',
    port=4567,
    user='tyxo0',
    password='0000',
    database='madang',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
print("MySQL 연결 성공")

# table Book 출력
print("초기 Book table")
with dbMadang.cursor() as cursor:
    sql = "SELECT * FROM Book"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(row)
    print("")

# 데이터 삽입
print("bookid 11에 스포츠의학을 추가한 Book table")
with dbMadang.cursor() as cursor:
    sql = "INSERT INTO Book(bookid, bookname, publisher, price) VALUES (11, '스포츠 의학', '한솔의학서적', 90000)"
    cursor.execute(sql)

    sql = "SELECT * FROM Book"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(row)
    print("")

# 데이터 삭제
print("bookid 11, 스포츠의학을 제거한 Book tables")
with dbMadang.cursor() as cursor:
    sql = "DELETE FROM Book WHERE bookid = '11'"
    cursor.execute(sql)

    sql = "SELECT * FROM Book"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(row)
    print("")

# 데이터 검색(출판사)
print("Book의 publisher 검색")
with dbMadang.cursor() as cursor:
    sql = "SELECT publisher FROM Book;"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(row)
    print("")
    
if dbMadang:
    dbMadang.close()
    print("MySQL 연결 종료")

