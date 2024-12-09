import tkinter as tk
from tkinter import messagebox
import pymysql

# db 접속
def fetch_students():
    try:
        connection = pymysql.connect(
            host="192.168.56.4",
            user="clubmanager",
            password="0000",
            database="software_club"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Student")
        result = cursor.fetchall()

        # Text 위젯 초기화
        text_area.delete("1.0", tk.END)
        for row in result:
            text_area.insert(tk.END, f"{row}\n")

        cursor.close()
        connection.close()
    except pymysql.MySQLError as e:
        messagebox.showerror("DB Error", f"데이터베이스 접근 중 오류 발생: {e}")
#학생 추가
def add_student():
    sname = entry_name.get().strip()
    if not sname:
        messagebox.showwarning("입력 오류", "이름을 입력하세요.")
        return
    
    try:
        connection = pymysql.connect(
            host="192.168.56.4",
            user="clubmanager",
            password="0000",
            database="software_club"
        )
        cursor = connection.cursor()
        query = "INSERT INTO Student (Sname) VALUES (%s)"
        cursor.execute(query, (sname,))
        connection.commit()
        cursor.close()
        connection.close()

        messagebox.showinfo("성공", f"학생 '{sname}' 추가 완료!")
        fetch_students()  # 새로고침
    except pymysql.MySQLError as e:
        messagebox.showerror("DB Error", f"추가 중 오류 발생: {e}")

# 메인 창
root = tk.Tk()
root.title("Software Club Management")
root.geometry("800x600")

# 학생 조회 버튼
btn_fetch = tk.Button(root, text="학생 조회", command=fetch_students)
btn_fetch.pack(pady=10)

# 학생 추가 섹션
frame_add = tk.Frame(root)
frame_add.pack(pady=5)

tk.Label(frame_add, text="이름:").pack(side=tk.LEFT, padx=5)
entry_name = tk.Entry(frame_add)
entry_name.pack(side=tk.LEFT, padx=5)
btn_add = tk.Button(frame_add, text="학생 추가", command=add_student)
btn_add.pack(side=tk.LEFT, padx=5)

# 결과 표시용 Text 위젯
text_area = tk.Text(root, wrap="none")
text_area.pack(expand=True, fill="both", padx=10, pady=10)

root.mainloop()
