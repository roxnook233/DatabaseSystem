import tkinter as tk
from tkinter import ttk, messagebox
import pymysql


def get_connection():
    # 데이터베이스에 접속하고 커넥션 객체를 반환하는 함수
    return pymysql.connect(
        host="192.168.56.4",
        user="clubmanager",
        password= "0000",
        database="software_club"
    )

# 테이블 정보 
TABLES ={
    "Student":{
        "pk": "student_id",
        "columns": ["student_id", "Sname", "gender", "Dno", "tel", "email", "club_id", "Bdate"]
    },
    "Professor":{
        "pk": "professor_id",
        "columns": ["professor_id", "Pname", "gender", "tel", "email", "office_location", "advising_club_id", "Bdate"]
    },
    "ACTIVITY":{
        "pk": "activity_id",
        "columns": ["activity_id", "Aname", "category", "period", "C_id"]
    },
    "ITEM":{
        "pk": "item_support_id",
        "columns": ["item_support_id", "item_id", "item_name", "C_id"]
    },
    "Activity_fee":{
        "pk": "fee_support_id",
        "columns": ["fee_support_id", "fee_usage", "subsidy", "C_id"]
    },
    "Club":{
        "pk": "club_id",
        "columns": ["club_id", "club_name", "club_Bdate", "location", "type"]
    }
}

def on_table_select(event):
    """ 
    콤보박스에서 테이블을 선택했을 때 호출되는 함수
    선택한 테이블에 맞는 컬럼 Entry를 생성하고 Teeview 컬럼을 재설정한 뒤 해당 테이블 레코드를 조회한다.
    """
    
    table = combo_table.get()
    cols = TABLES[table]["columns"]
    
    # 기존 컬럼 위젯 제거
    for widget in frame_columns.winfo_children():
        widget.destroy()
    
    global entries
    entries = {}
    
    # 컬럼 라벨 및 엔트리 중앙 정렬
    for col in cols:
        lbl = tk.Label(frame_columns, text=col + ":")
        lbl.pack(anchor="center", pady=2)
        
        # Entry 폭 설정
        ent = tk.Entry(frame_columns, width=30)
        ent.pack(anchor="center", pady=2)
        entries[col] = ent

    setup_tree()
    search_records()

def insert_record():
    # Entry에 입력된 값을 바탕으로 INSERT 쿼리 실행
    
    table = combo_table.get()
    cols = TABLES[table]["columns"]
    vals = [entries[c].get().strip() for c in cols]
    
    cols_str = ", ".join(cols)
    placeholders = ", ".join(["%s"] * len(cols))
    query = f"INSERT INTO {table} ({cols_str}) VALUES ({placeholders})"
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, vals)
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("성공", f"{table} 테이블에 레코드 추가 완료")
        search_records()
    except pymysql.MySQLError as e:
        messagebox.showerror("DB Error", str(e))

def update_record():
    # pk로 특정 레코드를 찾아 Update 쿼리 실행
    
    table = combo_table.get()
    pk = TABLES[table]["pk"]
    cols = TABLES[table]["columns"]
    
    pk_val = entries[pk].get().strip()
    if pk_val == "":
        messagebox.showwarning("입력 오류", f"Update하려면 {pk}를 입력해야 합니다.")
        return
    
    set_clauses = []
    vals = []
    for c in cols:
        if c == pk:
            continue
        val = entries[c].get().strip()
        set_clauses.append(f"{c}=%s")
        vals.append(val)
        
    if not set_clauses:
        messagebox.showwarning("입력 오류", "수정할 컬럼을 입력하세요.")
        return
    
    query = f"UPDATE {table} SET {', '.join(set_clauses)} WHERE {pk}=%s"
    vals.append(pk_val)
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        affected = cursor.execute(query, vals)
        conn.commit()
        cursor.close()
        conn.close()
        
        if affected == 0:
            messagebox.showinfo("결과", f"{pk_val} 레코드를 찾을 수 없습니다.")
        else:
            messagebox.showinfo("성공", f"{pk_val} 레코드 수정 완료")
            search_records()
    except pymysql.MySQLError as e:
        messagebox.showerror("DB Error", str(e))

def delete_record():
    # pk로 특정 레코드를 찾아 Delete 쿼리 실행
    
    table = combo_table.get()
    pk = TABLES[table]["pk"]
    pk_val = entries[pk].get().strip()
    if pk_val == "":
        messagebox.showwarning("입력 오류", f"삭제하려면 {pk}를 입력해야 합니다.")
        return
    
    query = f"DELETE FROM {table} WHERE {pk}=%s"
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        affected = cursor.execute(query, (pk_val,))
        conn.commit()
        cursor.close()
        conn.close()
        
        if affected == 0:
            messagebox.showinfo("결과", f"{pk_val} 레코드를 찾을 수 없습니다.")
        else:
            messagebox.showinfo("성공", f"{pk_val} 레코드 삭제 완료")
            search_records()
    except pymysql.MySQLError as e:
        messagebox.showerror("DB Error", str(e))

def search_records():
    # pk 값 유무에 따라 특정 레코드 또는 전체 레코드를 SELECT
    
    table = combo_table.get()
    pk = TABLES[table]["pk"]
    pk_val = entries[pk].get().strip()
    
    if pk_val:
        query = f"SELECT * FROM {table} WHERE {pk}=%s"
        vals = (pk_val,)
    else:
        query = f"SELECT * FROM {table}"
        vals = ()
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, vals)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # 기존 Treeview 데이터 삭제
        for i in tree.get_children():
            tree.delete(i)
        
        # 새로운 결과 추가
        for row in rows:
            tree.insert("", tk.END, values=row)
        
    except pymysql.MySQLError as e:
        messagebox.showerror("DB Error", str(e))

def setup_tree():
    # 현재 선택된 테이블에 맞추어 Treeview 컬럼 헤더를 설정
    
    table = combo_table.get()
    cols = TABLES[table]["columns"]
    tree["columns"] = cols
    tree["show"] = "headings"
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=100, anchor="center")

def on_tree_select(event):
    # Treeview에서 행 선택 시 그 값을 Entry에 반영
    
    selected = tree.selection()
    if not selected:
        return
    item = tree.item(selected[0])
    values = item["values"]
    
    table = combo_table.get()
    cols = TABLES[table]["columns"]
    
    for c, v in zip(cols, values):
        entries[c].delete(0, tk.END)
        entries[c].insert(0, str(v))

# 메인 창
root = tk.Tk()
root.title("Software Club Management")
root.geometry("900x700")

# 테이블 선택
frame_top = tk.Frame(root)
frame_top.pack(fill="x", padx=10, pady=10)

tk.Label(frame_top, text="테이블 선택:").pack(side=tk.LEFT)
combo_table = ttk.Combobox(frame_top, values=list(TABLES.keys()), state="readonly")
combo_table.current(0)
combo_table.pack(side=tk.LEFT, padx=5)
combo_table.bind("<<ComboboxSelected>>", on_table_select)

# 컬럼 입력 
frame_columns = tk.LabelFrame(root, text="컬럼 입력")
frame_columns.pack(fill="x", padx=200, pady=10)

entries = {}

# 버튼: Insert, Update, Delete, Search 
frame_buttons = tk.Frame(root)
frame_buttons.pack(fill="x", padx=10, pady=10)

insert_btn = tk.Button(frame_buttons, text="Insert", command=insert_record)
insert_btn.pack(side=tk.LEFT, padx=5)

update_btn = tk.Button(frame_buttons, text="Update", command=update_record)
update_btn.pack(side=tk.LEFT, padx=5)

delete_btn = tk.Button(frame_buttons, text="Delete", command=delete_record)
delete_btn.pack(side=tk.LEFT, padx=5)

select_btn = tk.Button(frame_buttons, text="Search", command=search_records)
select_btn.pack(side=tk.LEFT, padx=5)

# 결과 표시용 Treeview
frame_list = tk.Frame(root)
frame_list.pack(fill="both", expand=True, padx=10, pady=10)

tree = ttk.Treeview(frame_list, columns=("none",), show="headings")
tree.pack(fill="both", expand=True)

# 스크롤바 추가
scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree.bind("<<TreeviewSelect>>", on_tree_select)

# 프로그램 시작 시 초기 테이블 로드
on_table_select(None)

root.mainloop()
