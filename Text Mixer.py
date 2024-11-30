# 类库
import tkinter as tk
import markdown
import random
import ctypes # hidpi
import re
from tkinter import ttk, filedialog, messagebox, simpledialog, font
from ttkbootstrap import Style # theme

# 功能
## 新建文本文档
def new_file():
    text_area_md.delete(1.0, tk.END)
## 读取markdown文件
def load_markdown():
    file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md *.markdown")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            markdown_text = file.read()
        text_area_md.delete(1.0, tk.END)
        text_area_md.insert(tk.END, markdown_text)
## 保存功能
def save_file():
    if notebook.index(notebook.select()) == 0:  # tab_md
        content = text_area_md.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md *.markdown")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)

    elif notebook.index(notebook.select()) == 1:  # tab_generate
        content = text_area_generate.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
## 查找功能
def find_text():
    if notebook.index(notebook.select()) == 0:  # tab_md
        def search_next():
            try:
                start_index = next_idx.get()
                end_index = f"{start_index}+{len(find_entry.get())}c"
                match_start = text_area_md.search(find_entry.get(), start_index, stopindex=tk.END, nocase=True)
                if match_start:
                    match_end = f"{match_start}+{len(find_entry.get())}c"
                    text_area_md.tag_remove("found", "1.0", tk.END)
                    text_area_md.tag_add("found", match_start, match_end)
                    text_area_md.tag_config("found", background="grey")
                    text_area_md.see(match_start)
                    next_idx.set(match_end)
                else:
                    messagebox.showinfo("查找", "找不到更多匹配项！")
            except Exception as e:
                print(e)
    elif notebook.index(notebook.select()) == 1:  # tab_generate  
        def search_next():
            try:
                start_index = next_idx.get()
                end_index = f"{start_index}+{len(find_entry.get())}c"
                match_start = text_area_generate.search(find_entry.get(), start_index, stopindex=tk.END, nocase=True)
                if match_start:
                    match_end = f"{match_start}+{len(find_entry.get())}c"
                    text_area_generate.tag_remove("found", "1.0", tk.END)
                    text_area_generate.tag_add("found", match_start, match_end)
                    text_area_generate.tag_config("found", background="grey")
                    text_area_generate.see(match_start)
                    next_idx.set(match_end)
                else:
                    messagebox.showinfo("查找", "找不到更多匹配项！")
            except Exception as e:
                print(e)
    # 创建查找对话框
    find_dialog = tk.Toplevel(root)
    find_dialog.title("查找")

    # 创建标签和输入框
    tk.Label(find_dialog, text="查找内容:").grid(row=0, column=0, padx=10, pady=5)
    find_entry = tk.Entry(find_dialog)
    find_entry.grid(row=0, column=1, padx=10, pady=5)

    # 创建查找下一个按钮
    next_button = tk.Button(find_dialog, text="查找下一个", command=search_next)
    next_button.grid(row=1, column=0, columnspan=2, pady=10)

    # 初始化查找索引
    next_idx = tk.StringVar()
    next_idx.set("1.0")
## 替换功能
def replace_text():
    if notebook.index(notebook.select()) == 0:  # tab_md
        def find_next_replace():
            try:
                text_area_md.mark_set(tk.INSERT, "1.0")
                start_index = next_idx.get()
                end_index = f"{start_index}+{len(find_entry.get())}c"
                match_start = text_area_md.search(find_entry.get(), start_index, stopindex=tk.END, nocase=True)
                if match_start:
                    match_end = f"{match_start}+{len(find_entry.get())}c"
                    text_area_md.tag_remove("found", "1.0", tk.END)
                    text_area_md.tag_add("found", match_start, match_end)
                    text_area_md.tag_config("found", background="grey")
                    text_area_md.see(match_start)
                    next_idx.set(match_end)
                else:
                    messagebox.showinfo("查找", "找不到更多匹配项！")
            except Exception as e:
                print(e)

        def replace_once():
            start = text_area_md.search(find_entry.get(), "insert", stopindex=tk.END)
            if start == "":
                messagebox.showinfo("替换", "未找到匹配项")
            else:
                end = f"{start}+{len(find_entry.get())}c"
                text_area_md.delete(start, end)
                text_area_md.insert(start, replace_entry.get())
    
        def replace_all():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
    
            if not find_text:
                messagebox.showinfo("查找内容为空", "请输入要查找的内容。")
                return

            text_content = text_area_md.get(1.0, tk.END)
            if find_text in text_content:
                num_replacements = text_content.count(find_text)
                confirm = messagebox.askyesno("确认替换", f"找到 {num_replacements} 处匹配项，是否全部替换？")
                if confirm:
                    new_content = text_content.replace(find_text, replace_text)
                    text_area_md.delete(1.0, tk.END)
                    text_area_md.insert(tk.END, new_content)
            else:
                messagebox.showinfo("未找到匹配项", "文档中没有找到匹配的文本。")
    elif notebook.index(notebook.select()) == 1:  # tab_generate  
        def find_next_replace():
            try:
                text_area_generate.mark_set(tk.INSERT, "1.0")
                start_index = next_idx.get()
                end_index = f"{start_index}+{len(find_entry.get())}c"
                match_start = text_area_generate.search(find_entry.get(), start_index, stopindex=tk.END, nocase=True)
                if match_start:
                    match_end = f"{match_start}+{len(find_entry.get())}c"
                    text_area_generate.tag_remove("found", "1.0", tk.END)
                    text_area_generate.tag_add("found", match_start, match_end)
                    text_area_generate.tag_config("found", background="grey")
                    text_area_generate.see(match_start)
                    next_idx.set(match_end)
                else:
                    messagebox.showinfo("查找", "找不到更多匹配项！")
            except Exception as e:
                print(e)

        def replace_once():
            start = text_area_generate.search(find_entry.get(), "insert", stopindex=tk.END)
            if start == "":
                messagebox.showinfo("替换", "未找到匹配项")
            else:
                end = f"{start}+{len(find_entry.get())}c"
                text_area_generate.delete(start, end)
                text_area_generate.insert(start, replace_entry.get())
    
        def replace_all():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
    
            if not find_text:
                messagebox.showinfo("查找内容为空", "请输入要查找的内容。")
                return

            text_content = text_area_generate.get(1.0, tk.END)
            if find_text in text_content:
                num_replacements = text_content.count(find_text)
                confirm = messagebox.askyesno("确认替换", f"找到 {num_replacements} 处匹配项，是否全部替换？")
                if confirm:
                    new_content = text_content.replace(find_text, replace_text)
                    text_area_generate.delete(1.0, tk.END)
                    text_area_generate.insert(tk.END, new_content)
            else:
                messagebox.showinfo("未找到匹配项", "文档中没有找到匹配的文本。")

    replace_dialog = tk.Toplevel(root)
    replace_dialog.title("查找和替换")
    
    tk.Label(replace_dialog, text="查找内容:").grid(row=0, column=0, padx=5, pady=5)
    find_entry = tk.Entry(replace_dialog, width=40)
    find_entry.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(replace_dialog, text="替换为:").grid(row=1, column=0, padx=5, pady=5)
    replace_entry = tk.Entry(replace_dialog, width=40)
    replace_entry.grid(row=1, column=1, padx=5, pady=5)
    
    find_button = tk.Button(replace_dialog, text="查找下一个", command=find_next_replace)
    find_button.grid(row=2, column=0, padx=5, pady=5)

    replace_once_button = tk.Button(replace_dialog, text="替换一次", command=replace_once)
    replace_once_button.grid(row=2, column=1, padx=5, pady=5)

    replace_all_button = tk.Button(replace_dialog, text="全部替换", command=replace_all)
    replace_all_button.grid(row=2, column=2, padx=5, pady=5)

    # 设置高亮样式
    text_area_md.tag_configure("highlight", background="grey")
    next_idx = tk.StringVar()
    next_idx.set("1.0")
## 设置字体





















## 关于作者

def about_program():
    messagebox.showinfo("关于", "本软件是由Pizza开发的的开源软件。")

## Generate功能
def generate_content():
    markdown_text = text_area_md.get(1.0, tk.END)
    html = markdown.markdown(markdown_text)
    headings = re.findall(r'<h2>(.*?)</h2>', html)
    lists = re.findall(r'<ul>(.*?)</ul>', html, re.DOTALL)

    if not headings or not lists:
        messagebox.showwarning("错误","哎哟，请先读入Markdown文档！")
        return

    combined_content = []
    for i, heading in enumerate(headings):
        list_items = re.findall(r'<li>(.*?)</li>', lists[i])
        if list_items:
            random_item = random.choice(list_items) 
            combined_content.append(f"{random_item}")

    result = "".join(combined_content)
    text_area_generate.delete(1.0, tk.END)
    text_area_generate.insert(tk.END, result)




# 窗体
root = tk.Tk()
## 窗体主题
style = Style(theme='cosmo')
## hidpi
try:  # >= win 8.1
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:  # win 8.0 or less
    ctypes.windll.user32.SetProcessDPIAware()
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
root.tk.call('tk', 'scaling', ScaleFactor/75)
## 程序标题
root.title("Text Mixer 0.1")

## 顶部菜单栏
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="新建Markdown文件", command=new_file)
file_menu.add_command(label="载入Markdown文件", command=load_markdown)
file_menu.add_command(label="保存文件", command=save_file)
file_menu.add_command(label="退出", command=root.quit)
menu_bar.add_cascade(label="文件", menu=file_menu)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="查找", command=find_text)
file_menu.add_command(label="替换", command=replace_text)
# file_menu.add_command(label="字体", command=change_font)
menu_bar.add_cascade(label="编辑", menu=file_menu)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="关于...", command=about_program)
menu_bar.add_cascade(label="帮助", menu=file_menu)
root.config(menu=menu_bar)

## 滚动条
scrollbar_0 = tk.Scrollbar(root)
scrollbar_0.pack(side=tk.RIGHT, fill=tk.Y)

## 标签页
notebook = ttk.Notebook(root)
tab_md = ttk.Frame(notebook)
tab_generate = ttk.Frame(notebook)
notebook.add(tab_md, text="Markdown")
notebook.add(tab_generate, text="Mixer")

### markdown标签
text_area_md = tk.Text(tab_md, undo=True, yscrollcommand=scrollbar_0.set)
text_area_md.pack(fill=tk.BOTH, expand=True)

scrollbar_0.config(command=text_area_md.yview)

#### 创建右键菜单
def cut_text_md():
   text_area_md.event_generate("<<Cut>>")
def copy_text_md():
   text_area_md.event_generate("<<Copy>>")
def paste_text_md():
   text_area_md.event_generate("<<Paste>>")

right_click_menu_md = tk.Menu(root, tearoff=0)
right_click_menu_md.add_command(label="剪切", command=cut_text_md)
right_click_menu_md.add_command(label="复制", command=copy_text_md)
right_click_menu_md.add_command(label="粘贴", command=paste_text_md)
def show_right_click_menu_md(event):
    right_click_menu_md.post(event.x_root, event.y_root)
text_area_md.bind("<Button-3>", show_right_click_menu_md)  # 绑定右键点击事件

### generate标签
text_area_generate = tk.Text(tab_generate, undo=True, yscrollcommand=scrollbar_0.set)
text_area_generate.pack(fill=tk.BOTH, expand=True)

generate_button = tk.Button(tab_generate, text="随机组合", command=generate_content)
generate_button.pack(pady=5)
scrollbar_0.config(command=text_area_generate.yview)


#### 创建右键菜单
def cut_text_ge():
   text_area_generate.event_generate("<<Cut>>")
def copy_text_ge():
   text_area_generate.event_generate("<<Copy>>")
def paste_text_ge():
   text_area_generate.event_generate("<<Paste>>")

right_click_menu_ge = tk.Menu(root, tearoff=0)
right_click_menu_ge.add_command(label="剪切", command=cut_text_ge)
right_click_menu_ge.add_command(label="复制", command=copy_text_ge)
right_click_menu_ge.add_command(label="粘贴", command=paste_text_ge)
def show_right_click_menu_ge(event):
    right_click_menu_ge.post(event.x_root, event.y_root)
text_area_generate.bind("<Button-3>", show_right_click_menu_ge)  # 绑定右键点击事件




notebook.pack(expand=True, fill=tk.BOTH)
root.mainloop()