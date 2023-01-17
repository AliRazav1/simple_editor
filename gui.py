from logging import root
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from os.path import isfile
from tkinter import messagebox
from tkinter import simpledialog
from os import listdir
from re import findall
from re import finditer
import os
from tkinter import font as fonttkinter
import keyword
import builtins
from tkinter import colorchooser
global counter , dict_tabs , current_tab
current_tab = None
dict_tabs = {}
counter = 1
alphabets = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
# here we define some keywords for each programming language
python_keywords = list(set(keyword.kwlist + dir(builtins)))
python_keywords = sorted(python_keywords,key = lambda x:len(x),reverse=True)
python_keywords = list("("+i+")" for i in python_keywords)
java_keywords = ["Scanner","System","abstract", "assert", "boolean",
                "break", "byte", "case", "catch", "char", "class", "const",
                "continue", "default", "do", "double", "else", "extends", "false",
                "final", "finally", "float", "for", "goto", "if", "implements",
                "import", "instanceof", "int", "interface", "long", "native",
                "new", "null", "package", "private", "protected", "public",
                "return", "short", "static", "strictfp", "super", "switch",
                "synchronized", "throw", "throws", "transient", "true",
                "try", "void", "volatile", "while"]
java_keywords = sorted(java_keywords,key = lambda x:len(x),reverse=True)
java_keywords = list("("+i+")" for i in java_keywords)
cpp_keywords = ["printf","scanf","cin","cout","include",'asm', 'auto', 'break', 'case', 'catch', 'char', 'class', 'const', 'continue', 'default', 'delete', 'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'friend', 'goto', 'if', 'inline', 'int', 'long', 'new', 'operator', 'private', 'protected', 'public', 'register', 'return', 'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'template', 'this', 'throw', 'try', 'typedef', 'union', 'unsigned', 'virtual', 'void', 'volatile', 'while']
cpp_keywords = sorted(cpp_keywords,key = lambda x:len(x),reverse=True)
cpp_keywords = list("("+i+")" for i in cpp_keywords)



class FindReplaceDialog(Toplevel):
    def __init__(self, master, textWidget, withdrawInsteadOfDestroy=False, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.transient(master)
        self.resizable(False, False)

        frame = FindReplaceFrame(self, textWidget)
        frame.pack(fill="both", padx=10, pady=10)

        x = master.winfo_rootx() + (master.winfo_width()/2) - (self.winfo_reqwidth()/2)
        y = master.winfo_rooty() + (master.winfo_height()/2) - (self.winfo_reqheight()/2)
        self.geometry(f'+{int(x)}+{int(y)}')
        if withdrawInsteadOfDestroy:
            self.protocol("WM_DELETE_WINDOW", self.withdraw)

# this function is for coloring texts
def coloring_texts_of_widget(text_element):
    global current_tab , dict_tabs
    indexes = []
    indexes2 = []
    lines = text_element.get(0.0, END).split("\n")[:-1]
    lang = dict_tabs[current_tab][3]
    if lang !="Plain Text":
     # here we check each programming language has been set
     if lang=="Java":
        keywords = java_keywords
     elif lang=="Python":
        keywords = python_keywords
     elif lang=="C++":
        keywords = cpp_keywords
     list(list(indexes.append([str(i+1)+'.'+str(k.span()[0]),str(i+1)+'.'+str(k.span()[1])]) for k in list(finditer("|".join(keywords),lines[i]))) for i in range(len(lines)))
     list(list(indexes2.append([str(i+1)+'.'+str(k.span()[0]),str(i+1)+'.'+str(k.span()[1])]) for k in list(finditer('".*?"',lines[i]))) for i in range(len(lines)))
     for item in indexes:
      l = lines[int(item[0].split(".")[0])-1]
      status_for_coloring1 = False
      try:
        if int(item[0].split(".")[1])>0:
         if l[int(item[0].split(".")[1])-1] in [" ","\t","\n","=","#"]:
            status_for_coloring1 = True
         else:
            status_for_coloring1 = False
        else:
            status_for_coloring1 = True
      except:
        status_for_coloring1 = True
      status_for_coloring2 = False
      try:
        if l[int(item[1].split(".")[1])] in [" ","\t","\n","(","<",">","."]:
         status_for_coloring2 = True
        else:
            status_for_coloring2 = False
      except:
        status_for_coloring2 = True
      if status_for_coloring2 and status_for_coloring1:
       text_element.tag_add("coloring_syntax", item[0],item[1])
       text_element.tag_configure("coloring_syntax", foreground= "purple")
     for item in indexes2:
       text_element.tag_add("between_cot", item[0],item[1])
       text_element.tag_configure("between_cot", foreground= "#b36200")

def onModification(event):
     event.widget.tag_delete("coloring_syntax")
     event.widget.tag_delete("between_cot")
     coloring_texts_of_widget(event.widget)


class CustomText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
    def _proxy(self, command, *args):
        global dict_tabs , current_tab
        if command == 'get' and (args[0] == 'sel.first' and args[1] == 'sel.last') and not dict_tabs[current_tab][0].tag_ranges('sel'): return
        if command == 'delete' and (args[0] == 'sel.first' and args[1] == 'sel.last') and not dict_tabs[current_tab][0].tag_ranges('sel'): return
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)
        if command in ('insert', 'delete', 'replace'):
                self.event_generate('<<TextModified>>')
        return result

class FindReplaceFrame(Frame):
    def __init__(self, master, textWidget, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.textWidget = textWidget
        self.findStartPos = 1.0

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, pad=8)
        self.rowconfigure(1, pad=8)

        Label(self, text="Find: ").grid(row=0, column=0, sticky="nw")
        self.findEntry = Entry(self)
        self.findEntry.grid(row=0, column=1, sticky="new")
        self.findEntry.focus()

        Label(self, text="Replace: ").grid(row=1, column=0, sticky="nw")
        self.replaceEntry = Entry(self)
        self.replaceEntry.grid(row=1, column=1, sticky="new")

        buttonFrame = Frame(self)
        buttonFrame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.findNextButton = Button(buttonFrame, text="Find Next", command=self.findNext)
        self.findNextButton.grid(row=0, column=0, padx=(0, 5))
        self.replaceButton = Button(buttonFrame, text="Replace", command=self.replace)
        self.replaceButton.grid(row=0, column=1, padx=(0, 5))
        self.replaceAllButton = Button(buttonFrame, text="Replace All", command=self.replaceAll)
        self.replaceAllButton.grid(row=0, column=2)

        optionsFrame = Frame(self)
        optionsFrame.grid(row=3, column=0, sticky="nsew")
        self.matchCaseVar = BooleanVar(self, True)
        self.matchCaseCheckbutton = Checkbutton(optionsFrame, text="Match Case", variable=self.matchCaseVar)
        self.matchCaseCheckbutton.grid(row=0, column=0, sticky="nw")
        

    def findNext(self):
        key = self.findEntry.get()
        pos = self.textWidget.search(key, INSERT, nocase=not self.matchCaseVar.get())
        if pos:
            endIndex = f'{pos}+{len(key)}c'
            if self.textWidget.tag_ranges(SEL): 
                self.textWidget.tag_remove(SEL, SEL_FIRST, SEL_LAST)
            self.textWidget.tag_add(SEL, pos, endIndex)
            self.textWidget.mark_set(INSERT, endIndex)
            self.textWidget.see(endIndex)

    def replace(self):
        key = self.findEntry.get()
        repl = self.replaceEntry.get()
        flags = 0
        selRange = self.textWidget.tag_ranges(SEL)
        if selRange:
            selection = self.textWidget.get(selRange[0], selRange[1])
            if not self.matchCaseVar.get():
                key = key.lower()
                selection = selection.lower()
            if key == selection:
                self.textWidget.delete(selRange[0], selRange[1])
                self.textWidget.insert(selRange[0], repl)
        self.findNext()

    def replaceAll(self):
        start = "1.0"
        key = self.findEntry.get()
        repl = self.replaceEntry.get()
        count = 0
        
        while True:
            pos = self.textWidget.search(key, start, "end")
            if pos:
                self.textWidget.delete(pos, f"{pos}+{len(key)}c")
                self.textWidget.insert(pos, repl)
                start = f"{pos}+{len(repl)}c"
                count += 1
            else:
                messagebox.showinfo("", f"Replaced {count} occurences.")
                break

def openFindReplaceDialog(e=None):
        global dict_tabs , current_tab
        if e!=None:
         FindReplaceDialog(root_window, e.widget, True)
        else:
         FindReplaceDialog(root_window,dict_tabs[current_tab][0],True)

def goto_line(e=None):
    global dict_tabs
    line = simpledialog.askinteger(title="line",prompt="Which Line? ")
    if e!=None:
        e.widget.mark_set("insert", f"{line}.0")
        e.widget.see("insert")
    else:
        dict_tabs[current_tab][0].mark_set("insert", f"{line}.0")
        dict_tabs[current_tab][0].see("insert")

def config_main_window():
 window = Tk()
 window.geometry("1000x600")
 window.title("Khu Editor")
 window.resizable(0,0)
 photo = PhotoImage(file = "notepad.png")
 window.iconphoto(False, photo)
 return window

def selectall(ev):
    ev.widget.event_generate('<<SelectAll>>')
    return 'break'

def on_tab_change(event):
  global current_tab , root_window , tabcontrol , counter , dict_tabs
  try:
   current_tab = event.widget
   current_tab = current_tab.select()
   root_window.title(dict_tabs[current_tab][1].strip().replace("  "," ").replace("  "," ")+" - Khu Editor"+f"      mode: {dict_tabs[current_tab][3]}")
  except:
    pass

def undo(e=None):
    global current_tab , dict_tabs
    dict_tabs[current_tab][0].edit_undo()

def redo(e=None):
    global current_tab , dict_tabs
    dict_tabs[current_tab][0].edit_redo()

def get_file_type(s):
    if '.' in s:
        extension = s.split('.')[-1].lower()
        if  extension == "java":
            return "Java"
        elif extension == "c" or extension == "cpp" or extension =="h" or extension == "hpp":
            return "C++"
        elif extension == "py" or extension == "pyc":
            return "Python"
        else:
            return "Plain Text"
    else:
        return "Plain Text"

def add_text_area_with_scroll(tab,tpe,t):
    global tabcontrol , dict_tabs , default_bg , default_fg , current_tab
    myscrollbarx=Scrollbar(tab, orient='horizontal')
    myscrollbarx.pack(side=BOTTOM, fill='x')
    myscrollbary=Scrollbar(tab, orient='vertical')
    myscrollbary.pack(side=RIGHT, fill='y')
    text=CustomText(tab,font=("Helvetica",13),selectforeground="gray",undo=True,width=1000,height=600  , wrap=NONE, xscrollcommand=myscrollbarx.set,yscrollcommand=myscrollbary.set)
    text.pack()
    text.bind_all('<Control-a>', selectall)
    text.bind("<<TextModified>>", onModification)
    text.config(inactiveselectbackground=text.cget("selectbackground"))
    try:
        text.config(foreground=default_fg)
        text.config(insertbackground=default_fg)
    except:
        pass
    try:
        text.config(background=default_bg)
    except:
        pass
    text.bind_all("<Control-f>", openFindReplaceDialog)
    mode_lang = get_file_type(tpe)
    tabcontrol.select(tab)
    dict_tabs[tabcontrol.select()] = [text,tpe,t,mode_lang]
    text.event_generate("<<TextModified>>")
    tabcontrol.event_generate("<<NotebookTabChanged>>")
    myscrollbarx.config(command=text.xview)
    myscrollbary.config(command=text.yview)
    return text

def reload_notebook():
    global tabcontrol
    tabcontrol.pack_forget()
    tabcontrol.pack(expand=True,fill="both")


def close_tab(e=""):
    global tabcontrol , dict_tabs , current_tab , root_window
    if len(dict_tabs)>=2:
     if isfile(dict_tabs[current_tab][1]):
        with open(dict_tabs[current_tab][1],"r",encoding="utf-8") as f:
            content = f.read()
            f.close()
     if (dict_tabs[current_tab][2] == 0 and len(dict_tabs[current_tab][0].get("1.0", "end-1c").strip()) == 0) or (dict_tabs[current_tab][2] == 1 and content == dict_tabs[current_tab][0].get("1.0", "end-1c")):
            tabcontrol.forget(current_tab)
            reload_notebook()
            del(dict_tabs[current_tab])
     else:
        result = messagebox.askyesno("Close","Are you sure you want to close this file without saving?")
        if result==False:
            result = save_as_file()
            if result==1:
             tabcontrol.forget(current_tab)
             reload_notebook()
             del(dict_tabs[current_tab])
        else:
            tabcontrol.forget(current_tab)
            reload_notebook()
            del(dict_tabs[current_tab])
    else:
      messagebox.showerror(parent = root_window , message = "You must have atleast one opened tab", title="Error")

def new_file(e=""):
    global tabcontrol , counter , dict_tabs
    if len(dict_tabs)<12:
     tab = Frame(tabcontrol)
     tabcontrol.add(tab,text="   New   "+str(counter)+"   ")
     root_window.title("New "+str(counter)+" - Khu Editor"+f"      mode: Plain Text")
     add_text_area_with_scroll(tab,"New "+str(counter),0)
     reload_notebook()
     counter+=1
    else:
     messagebox.showerror(parent = root_window , message = "You can't have more than 12 tabs", title="Error")

def next_tab(e=""):
    global tabcontrol , current_tab , dict_tabs
    try:
     if tabcontrol.index(current_tab)+1<=len(dict_tabs):
      tabcontrol.select(tabcontrol.index(current_tab)+1)
     else:
      tabcontrol.select(0)
    except:
      tabcontrol.select(0)
    current_tab = tabcontrol.select()

def previous_tab(e):
    global tabcontrol , current_tab , dict_tabs
    try:
     tabcontrol.select(tabcontrol.index(current_tab)-1)
     current_tab = tabcontrol.select()
    except:
     tabcontrol.select(len(dict_tabs)-1)

def add_tab_control():
    global tabcontrol , dict_tabs
    tabcontrol = Notebook(root_window)
    tabcontrol.pack(expand=True,fill="both")
    tabcontrol.bind('<<NotebookTabChanged>>', on_tab_change)
    if len(dict_tabs) == 0:
       new_file()

def create_text_area_and_tabs():
    global main_frame
    add_tab_control()

def save_file(e=""):
    global tabcontrol , dict_tabs , current_tab
    if dict_tabs[current_tab][2] == 0:
        save_as_file()
    else:
      try:
        text_to_save = dict_tabs[current_tab][0].get("1.0","end-1c")
        file_to_save = open(dict_tabs[current_tab][1],'w',encoding="utf-8")
        file_to_save.write(text_to_save)
        file_to_save.close()
      except:
        pass

def save_as_file(e=""):
    global tabcontrol , dict_tabs , current_tab
    text_to_save = dict_tabs[current_tab][0].get("1.0","end-1c")
    file_name = filedialog.asksaveasfilename()
    try:
     if file_name!=None and file_name!="" and file_name!=():
        if isfile(file_name):
            mode = "linux" if '/' in file_name else "windows"
            file_name = file_name.split('/') if '/' in file_name else file_name.split('\\')
            last_index = list(k for k in listdir() if (file_name[-1].split(".")[0] if '.' in file_name[-1] else file_name[-1]) in (k.split(".")[0] if '.' in k else k))
            last_index = list(0 if findall(r'\((.*?)\)',k)==[] else int(findall(r'\((.*?)\)',k)[0]) for k in last_index)
            last_index = sorted(last_index)[-1]
            if '.' in file_name[-1]:
             file_name = ('/' if mode=="linux" else "\\").join(file_name[:-1]) + ('/' if mode=="linux" else "\\") + (file_name[-1].split('.')[0]+'('+str(last_index+1)+').'+file_name[-1].split('.')[1])
            else:
             file_name = ('/' if mode=="linux" else "\\").join(file_name[:-1]) + ('/' if mode=="linux" else "\\") + file_name[-1]+'('+str(last_index+1)+')'
        file_to_save = open(file_name,'w',encoding="utf-8")
        file_to_save.write(text_to_save)
        file_to_save.close()
        dict_tabs[current_tab][1] = file_name
        dict_tabs[current_tab][2] = 1
        dict_tabs[current_tab][3] = get_file_type(file_name)
        dict_tabs[current_tab][0].event_generate("<<TextModified>>")
        tabcontrol.event_generate("<<NotebookTabChanged>>")
        root_window.title(f"{file_name} - Khu Editor"+f"      mode: {dict_tabs[current_tab][3]}")
        tabcontrol.tab(current_tab, text=file_name.split("/")[-1] if '/' in file_name else file_name.split("\\")[-1])
        return True
     else:
      messagebox.showerror(parent = root_window ,title="File Name Required", message="please select a file name!")
      return False
    except:
        pass

def quit_program(e=""):
    global root_window
    root_window.quit()

def cut_text(e=""):
    global root_window , dict_tabs , current_tab
    try:
      root_window.clipboard_clear()
      root_window.clipboard_append(dict_tabs[current_tab][0].get("sel.first", "sel.last"))
      dict_tabs[current_tab][0].delete("sel.first", "sel.last")
    except:
        pass

def copy_text(e=""):
    global root_window , dict_tabs , current_tab
    try:
      root_window.clipboard_clear()
      root_window.clipboard_append(dict_tabs[current_tab][0].get("sel.first", "sel.last"))
    except:
        pass

def paste_text(e=""):
    global root_window , dict_tabs , current_tab
    try:
     dict_tabs[current_tab][0].insert("insert", root_window.clipboard_get())
    except:
        pass

def open_command(e=""):
   global tabcontrol , dict_tabs , current_tab
   file_names = filedialog.askopenfilenames()
   d = list(dict_tabs.values())
   d = list(i[1] for i in d)
   if (type(file_names)==list or type(file_names)==tuple) and len(file_names)>0:
    for file_name in file_names:
     try:
      if file_name not in d:
       tab = Frame(tabcontrol)
       root_window.title(f"{file_name} - Khu Editor"+f"      mode: {dict_tabs[current_tab][3]}")
       tabcontrol.add(tab,text="   "+file_name.split("/")[-1]+"   " if '/' in file_name else "   "+file_name.split("\\")[-1]+"   ")
       text = add_text_area_with_scroll(tab,file_name,1)
       file_to_open = open(file_name,'r',encoding="utf-8")
       text.insert(END, file_to_open.read())
       file_to_open.close()
      else:
       messagebox.showerror(parent = root_window ,title="File Already Open", message=f"file {file_name} already open!")
     except:
       pass
    reload_notebook()
    change_lang(dict_tabs[current_tab][3])

def color_choosing_forefround(e=""):
    global root_window , dict_tabs , current_tab , default_fg
    try:
     color = colorchooser.askcolor()
     if color[1]!=None:
      for items in list(i[0] for i in list(dict_tabs.values())):
       items.config(insertbackground=color[1],fg=color[1])   
       default_fg = color[1]
    except:
        pass

def color_choosing(e=""):
   global root_window , dict_tabs , current_tab , default_bg
   try:
    color = colorchooser.askcolor()
    if color[1]!=None:
     for items in list(i[0] for i in list(dict_tabs.values())):
       items.config(bg=color[1])
       default_bg = color[1]
   except:
    pass

def change_lang(e=""):
    global dict_tabs , current_tab
    dict_tabs[current_tab][3] = e
    window_title = root_window.title()
    root_window.title(window_title.split("Khu Editor")[0]+"Khu Editor"+f"      mode: {e}")
    dict_tabs[current_tab][0].event_generate("<<TextModified>>")
    tabcontrol.event_generate("<<NotebookTabChanged>>")

def add_menu_bar():
    main_menu = Menu(root_window)
    submenufile = Menu(main_menu,tearoff=0)
    submenufile.add_command(label="    New File",accelerator="Ctrl+t",command=new_file)
    submenufile.add_command(label="    Open...",accelerator="Ctrl+o" , command=open_command)
    submenufile.add_command(label="    Close",accelerator="Ctrl+w",command=close_tab)
    submenufile.add_separator()
    submenufile.add_command(label="    Save",accelerator="Ctrl+s",command=save_file)
    submenufile.add_command(label="    Save as...",accelerator="Ctrl+S", command=save_as_file)
    submenufile.add_separator()
    submenufile.add_command(label="    Exit",accelerator="Ctrl+q",command=quit_program)
    submenuedit = Menu(main_menu,tearoff=0)
    submenuedit.add_command(label="    Undo" , accelerator="Ctrl+z" , command=undo)
    submenuedit.add_command(label="    Redo" , accelerator="Ctrl+Shift+z" , command=redo)
    submenuedit.add_separator()
    submenuedit.add_command(label="    Cut",command=cut_text,accelerator="Ctrl+x")
    submenuedit.add_command(label="    Copy",command=copy_text,accelerator="Ctrl+c")
    submenuedit.add_command(label="    Paste",command=paste_text,accelerator="Ctrl+v")
    submenuedit.add_separator()
    submenuedit.add_command(label="    Find And Replace",command=openFindReplaceDialog,accelerator="Ctrl+f")
    submenuedit.add_command(label="    Go to line" , command=goto_line,accelerator="Ctrl+g")
    subformatmenu = Menu(main_menu,tearoff=0)
    subformatmenu.add_command(label="    Color Background",command=color_choosing,accelerator="Ctrl+p")
    subformatmenu.add_command(label="    Color Foreground",command=color_choosing_forefround,accelerator="Ctrl+P")
    subhelpmenu = Menu(main_menu , tearoff=0)
    subhelpmenu.add_command(label="    About" , command=lambda:messagebox.showinfo(parent = root_window ,title="About", message="Khu Editor v1.0.0"))
    subhelpmenu.add_command(label="    License" , command=lambda:messagebox.showinfo(parent = root_window ,title="License", message="That's Free!"))
    sublangmenu = Menu(main_menu,tearoff=0)
    sublangmenu.add_command(label="    PlainText",command=lambda : change_lang("Plain Text"))
    sublangmenu.add_command(label="    Python",command=lambda : change_lang("Python"))
    sublangmenu.add_command(label="    Java",command=lambda : change_lang("Java"))
    sublangmenu.add_command(label="    CPP",command=lambda : change_lang("C++"))
    main_menu.add_cascade(label="  File", menu=submenufile)
    main_menu.add_cascade(label="  Edit",menu = submenuedit)
    main_menu.add_cascade(label="  Format",menu=subformatmenu)
    main_menu.add_cascade(label=" Language",menu=sublangmenu)
    main_menu.add_cascade(label=" Help",menu=subhelpmenu)
    root_window.config(menu=main_menu)
    root_window.bind_all("<Control-p>", color_choosing)
    root_window.bind_all("<Control-P>", color_choosing_forefround)
    root_window.bind_all("<Control-t>",new_file)
    root_window.bind_all("<Control-o>",open_command)
    root_window.bind_all("<Control-s>",save_file)
    root_window.bind_all("<Control-S>",save_as_file)
    root_window.bind_all("<Control-w>",close_tab)
    root_window.bind_all("<Control-q>",quit_program)
    root_window.bind_all("<Control-Tab>",next_tab)
    root_window.bind_all("<Control-Shift-KeyPress-Tab>",previous_tab)
    root_window.bind_all("<Control-g>",goto_line)

root_window = config_main_window()
create_text_area_and_tabs()
add_menu_bar()
available_fonts = fonttkinter.families()
root_window.mainloop()