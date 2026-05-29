import sys
import os
import datetime
import tkinter as tk
from tkinter import messagebox

def process_task(user_input, base_dir):
    if not user_input.strip():
        return False, "请输入有效的任务指令！"
        
    constitution_path = os.path.join(base_dir, ".ai_system_prompt.md")
    registry_path = os.path.join(base_dir, "AI_Skills_Registry.md")
    output_payload_path = os.path.join(base_dir, "Latest_Task_Payload.md")

    # 读取文件
    def read_file(path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return "（未能加载相关文件）"

    constitution = read_file(constitution_path)
    registry = read_file(registry_path)

    # 截取 registry 的一部分，避免过长
    if len(registry) > 2000:
        registry = registry[:2000] + "\n... (技能库较长，已截断。详情请查阅完整注册表)"

    # 构建 Payload
    payload = f"""# 🚀 集团 CEO 下达的最新自动化任务

> **生成时间**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
> **指令来源**: CEO_一键下达指令入口

## 1. CEO 原始业务需求 (非技术大白话)
```text
{user_input}
```

## 2. 强制遵守的系统约束 (《AI 强制宪法》节选)
{constitution}

## 3. 可用的本地武器库参考 (AI_Skills_Registry 节选)
{registry}

---
**[系统派发动作]**：
你（底层AI）接到了这个任务。你**必须**基于《AI 强制宪法》为你生成的代码 and 逻辑注入 429 防护 and 重试机制，然后立即开始执行！请立刻向 CEO 汇报你的执行方案 and 结果，而不是询问技术细节！
"""

    try:
        with open(output_payload_path, "w", encoding="utf-8") as f:
            f.write(payload)
        return True, output_payload_path
    except Exception as e:
        return False, f"写入 Payload 失败: {str(e)}"

def run_gui(base_dir):
    root = tk.Tk()
    root.title("👑 CEO AI 员工任务分发中心")
    root.configure(bg="#1E1E1E")
    root.resizable(False, False)

    # Center the window
    window_width = 750
    window_height = 550
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # Header Frame
    header_frame = tk.Frame(root, bg="#1E1E1E")
    header_frame.pack(side=tk.TOP, pady=15)

    title_label = tk.Label(
        header_frame, 
        text="👑 CEO AI 员工任务分发中心", 
        font=("Microsoft YaHei", 16, "bold"), 
        fg="#00FFCC", 
        bg="#1E1E1E"
    )
    title_label.pack()

    subtitle_label = tk.Label(
        header_frame, 
        text="请输入您的业务指令 (支持多行输入与粘贴，底层将静默注入《AI强制宪法》与《技能库》)", 
        font=("Microsoft YaHei", 9), 
        fg="#888888", 
        bg="#1E1E1E"
    )
    subtitle_label.pack(pady=5)

    # Button Action
    def on_submit():
        user_input = text_area.get("1.0", tk.END).strip()
        success, message = process_task(user_input, base_dir)
        if success:
            try:
                os.startfile(message)
            except Exception:
                pass
            messagebox.showinfo("派发成功", f"任务已成功封装编译！\n\n已自动为您打开生成的目标文件：\nLatest_Task_Payload.md")
            root.destroy()
        else:
            messagebox.showerror("错误", message)

    # Submit Button (Packed to the bottom first)
    btn_frame = tk.Frame(root, bg="#1E1E1E")
    btn_frame.pack(side=tk.BOTTOM, pady=20, fill=tk.X)

    submit_btn = tk.Button(
        btn_frame, 
        text="🚀 编译并派发任务", 
        command=on_submit,
        bg="#00FFCC", 
        fg="#1E1E1E", 
        font=("Microsoft YaHei", 12, "bold"), 
        activebackground="#00D8B2", 
        activeforeground="#1E1E1E", 
        relief="flat", 
        padx=20,
        pady=10,
        cursor="hand2"
    )
    submit_btn.pack()

    # Hover effect
    def on_enter(e):
        submit_btn.config(bg="#33FFD6")
    def on_leave(e):
        submit_btn.config(bg="#00FFCC")

    submit_btn.bind("<Enter>", on_enter)
    submit_btn.bind("<Leave>", on_leave)

    # Text Area (Packed last to fill remaining space)
    text_frame = tk.Frame(root, bg="#1E1E1E")
    text_frame.pack(side=tk.TOP, padx=20, pady=5, fill=tk.BOTH, expand=True)

    text_area = tk.Text(
        text_frame, 
        bg="#2D2D2D", 
        fg="#FFFFFF", 
        insertbackground="#FFFFFF", 
        relief="flat", 
        font=("Microsoft YaHei", 11), 
        wrap=tk.WORD,
        borderwidth=8
    )
    text_area.pack(fill=tk.BOTH, expand=True)
    text_area.focus_set()

    root.mainloop()

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if len(sys.argv) >= 2:
        # CLI Mode
        user_input = sys.argv[1]
        success, message = process_task(user_input, base_dir)
        if success:
            print("[OK] 任务已成功封装编译！")
            print(f"[+] Payload 已生成并存入: {message}")
        else:
            print(f"[FAIL] {message}")
            sys.exit(1)
    else:
        # GUI Mode
        run_gui(base_dir)

if __name__ == "__main__":
    main()
