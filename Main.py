from datetime import datetime
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp

'''--------------------'''


def add_student_info_by_txt(classes, section, file_name):
    with open(file_name, 'r') as file:
        header = file.readline().strip().split(',')
        num_columns = len(header)
        big_list = [[] for _ in range(num_columns)]
        for line in file:
            elements = line.strip().split(',')
            for i in range(num_columns):
                big_list[i].append(elements[i])
    for i in range(len(big_list[0])):
        create_table_query = f"""
                insert into {classes}_{section} (Roll_Number, Name, Phone_Number, Address, Total_Att, Total_Days, 
                Admission_Number ) VALUES (%s,%s,%s,%s,%s,%s,%s);"""
        report = [int(big_list[0][i]), big_list[1][i], big_list[2][i], big_list[3][i], int(big_list[4][i]),
                  int(big_list[5][i]),
                  int(big_list[6][i])]

        cursor.execute(create_table_query, report)
        connection.commit()
        print("TXT File Data Imported:")


def add_student_info_alpha(classes, section, rn, name, pn, add, an):
    try:
        c = classes
        s = section
        create_table_query = f"""
                        insert into {c}_{s}(Roll_Number, Name, Phone_Number, Address, Admission_Number ) 
                        VALUES (%s,%s,%s,%s,%s);"""
        report = [rn, name, pn, add, an]

        cursor.execute(create_table_query, report)
        connection.commit()
        return 'ok'
    except:
        return 'not ok'


def main_take_attendence(classes, section, rn, n, att):
    date = datetime.now().strftime('%Y%m%d')

    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {classes}_{section}_{date} (
            Roll_Number INT,
            Name VARCHAR(50),
            Attendance VARCHAR(10)
        );
        """
    cursor.execute(create_table_query)
    connection.commit()
    length = len(rn)
    for i in range(length):
        print(f"Attendance a/p: ")
        create_table_query = f"""insert into {classes}_{section}_{date} (Roll_Number, Name, Attendance) VALUES (%s, %s, %s);"""

        report = [rn[i], n[i], att[i]]

        cursor.execute(create_table_query, report)
        connection.commit()


def get_today_date():
    # Get today's date in the format 'YYYYMMDD'
    today_date = datetime.now().strftime('%Y%m%d')
    return today_date


def sql_to_name(classes, section):
    cursor.execute(f"SELECT name FROM {classes}_{section}")
    name_rows = cursor.fetchall()
    name_list = [row[0] for row in name_rows]
    return name_list


def sql_to_roll_number(classes, section):
    cursor.execute(f"SELECT Roll_Number FROM {classes}_{section}")
    rname_rows = cursor.fetchall()
    rname_list = [row[0] for row in rname_rows]
    return rname_list


def converter(classes, section):
    if classes == 'Class 1':
        classes = 1
    elif classes == 'Class 2':
        classes = 2
    elif classes == 'Class 3':
        classes = 3
    elif classes == 'Class 4':
        classes = 4
    elif classes == 'Class 5':
        classes = 5
    elif classes == 'Class 6':
        classes = 6
    elif classes == 'Class 7':
        classes = 7
    elif classes == 'Class 8':
        classes = 8
    elif classes == 'Class 9':
        classes = 9
    elif classes == 'Class 10':
        classes = 10
    elif classes == 'Class 11':
        classes = 11
    elif classes == 'Class 12':
        classes = 12
    else:
        pass
    # next
    if section == 'Section A':
        section = 'a'
    elif section == 'Section B':
        section = 'b'
    else:
        section = 'c'
    all_list = [classes, section]
    return all_list


'''--------------------'''
'''--------------------'''
import pymysql

connection = pymysql.connect(
    host='database-1.cretzsmx7wor.ap-south-1.rds.amazonaws.com',
    user='admin',
    password='ayushkumar',
    database='student_att',
    port=3306
)
cursor = connection.cursor()


def add_class(classes, section):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {classes}_{section} (
        Roll_Number INT PRIMARY KEY,
        Name VARCHAR(50),
        Phone_Number varchar(100),
        Address VARCHAR(100),
        Total_Att INT,
        Total_Days INT,
        Admission_Number INT 
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print(f"TABLE FORMED\nCLASS = {classes}\n SECTION = {section}\n ")


'''--------------------'''


class WindowManager(ScreenManager):
    pass


# Main Window:
class Main_Page(BoxLayout, Screen):
    pass


# WINDOW 2; ADD CLASS & SECTION
class Add_class_section(BoxLayout, Screen):
    pass


class add_student(StackLayout, Screen):
    classes = StringProperty()
    section = StringProperty()
    status = StringProperty()

    def classes_section(self, classes, section):
        self.classes += classes
        self.section += section
        main_list = converter(classes, section)
        add_class(main_list[0], main_list[1])


class Add_student_main(BoxLayout, Screen):
    pass


class Add_student_by_txt(StackLayout, Screen):
    classes = StringProperty()
    section = StringProperty()
    path = StringProperty()

    def select_file(self):
        from plyer import filechooser
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):
        self.path = str(selection)[2:-2]

    def all_function(self, classes, section):
        main_list = converter(classes, section)
        self.classes = str(main_list[0])
        self.section = str(main_list[1])
        add_student_info_by_txt(self.classes, self.section, self.path)


class add_student_info(StackLayout, Screen):
    def decide(self, a):
        if a == 'Add Manually ':
            return 'add_student_manually'
        if a == 'Add By Txt ':
            return 'h1'


class Add_student_manually(StackLayout, Screen):
    statuss = StringProperty()

    def do_nothing(self):
        pass

    def add_student_information(self, classes, section, rn, name, pn, add, an):
        # add_student_info(classes, section, rn, name, pn, add, an)
        alph = converter(classes, section)
        a = int(alph[0])
        b = str(alph[1])
        c = int(rn)
        d = str(name)
        e = str(pn)
        f = str(add)
        g = int(an)
        lets_see_now = add_student_info_alpha(a, b, c, d, e, f, g)
        if lets_see_now == 'ok':
            self.statuss = 'Successful'
        else:
            self.statuss = 'Error'


class Edit_student_info(StackLayout, Screen):
    def get_choice(self, ch):
        if ch == 'Edit By Name':
            return 'edit_by_name'
        if ch == 'Edit By Roll Number':
            'Edit_by_roll_number'
        if ch == 'Edit By Admission Number':
            return 'edit_by_adm'
        pass


class Edit_by_name(StackLayout, Screen):

    def edit_by_name_1(self, classes, section, nam, rn, pn, ad, adm):
        main = converter(classes, section)
        classes = main[0]
        section = main[1]
        sql = f''' UPDATE {classes}_{section} SET Roll_Number = %s, Phone_Number = %s, Address = %s, 
                Admission_Number = %s WHERE Name = %s;'''
        report = [rn, pn, ad, adm, nam]
        cursor.execute(sql, report)
        connection.commit()


class Edit_by_roll_number(StackLayout, Screen):
    def edit_by_rn(self, classes, section, nam, rn, pn, ad, adm):
        main = converter(classes, section)
        classes = main[0]
        section = main[1]

        sql = f''' UPDATE {classes}_{section} SET Name = %s, Phone_Number = %s, Address = %s, 
                            Admission_Number = %s WHERE Roll_Number = %s;'''
        report = [nam, pn, ad, adm, rn]
        cursor.execute(sql, report)
        connection.commit()


class Edit_by_admission(StackLayout, Screen):
    def edit_by_adm(self, classes, section, nam, rn, pn, ad, adm):
        main = converter(classes, section)
        classes = main[0]
        section = main[1]

        sql = f''' UPDATE {classes}_{section} SET Name = %s, Phone_Number = %s, Address = %s, 
                                     Roll_Number= %s WHERE Admission_Number = %s;'''
        report = [nam, pn, ad, rn, adm]
        cursor.execute(sql, report)
        connection.commit()


class Take_attendance_1(BoxLayout, Screen):
    pass


class Take_attendance_1_1(StackLayout, Screen):
    classes = ''
    section = ''

    def classes_section_12(self, a, b):
        # Function to handle the submission of class and section
        list12 = converter(a, b)
        c = list12[0]
        s = list12[1]

        if not c or not s:
            return  # Skip if class or section is empty

        print(f"Table name to be created: {c}_{s}")

        q = f'''TRUNCATE TABLE a_class_section;'''
        cursor.execute(q)
        connection.commit()

        query = f'''insert into a_class_section (class, section) VALUES(%s, %s);'''
        report = [c, s]
        cursor.execute(query, report)
        connection.commit()

        # Update the content of Take_attendance_2
        app = App.get_running_app()
        take_attendance_2_screen = app.root.get_screen('take_att')
        take_attendance_2_screen.update_content(c, s)

        app.root.current = 'take_att'
        app.root.transition.direction = 'left'


# Modified code for Take_attendance_2
class Take_attendance_2(BoxLayout, Screen):
    orientation = 'vertical'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spacing = 10
        self.padding = 5

        # Add class_name and section_name attributes
        self.class_name = 11
        self.section_name = 'a'

        # Initialize content
        self.update_content(self.class_name, self.section_name)

    def update_content(self, class_name, section_name):
        # Update SQL queries based on class_name and section_name
        cursor.execute(f"SELECT Roll_Number FROM {class_name}_{section_name}")
        rname_rows = cursor.fetchall()
        list_roll_number = [row[0] for row in rname_rows]

        cursor.execute(f"SELECT name FROM {class_name}_{section_name}")
        name_rows = cursor.fetchall()
        list_name = [row[0] for row in name_rows]

        # Update content based on the new data
        self.clear_widgets()  # Clear existing widgets

        btn = Button(text='Submit', background_normal='', font_name='fonts/ballo.ttf',
                     background_color=(0.45, 0.61, 1, 1))
        back_button = Button(text='Back', background_normal='', font_name='fonts/ballo.ttf',
                             background_color=(0.45, 0.61, 1, 1))
        btn.bind(
            on_press=lambda instance: self.on_submit(instance, class_name, section_name, list_name, list_roll_number),
            on_release=lambda instance: self.on_back_press(instance))

        back_button.bind(on_press=self.on_back_press)

        content_layout = GridLayout(cols=3, padding=10, size_hint_y=None)
        content_layout.add_widget(Label(text='Roll Number', color=(0, 0, 0, 1), size_hint=(None, None), size=(100, 20)))
        content_layout.add_widget(Label(text='Name', color=(0, 0, 0, 1), size_hint=(None, None), size=(100, 20)))
        content_layout.add_widget(Label(text='Present', color=(0, 0, 0, 1), size_hint=(None, None), size=(100, 20)))

        self.checkbox_states = []  # List to store checkbox states ('p' for checked, 'a' for unchecked)
        for i in range(len(list_roll_number)):
            name = list_name[i]
            name = str(name)
            content_layout.add_widget(Button(text=str(list_roll_number[i]), size_hint=(None, None), size=(100, 50)))
            content_layout.add_widget(Label(text=name, color=(0, 0, 0, 1), size_hint=(None, None), size=(100, 50)))

            c = CheckBox()
            content_layout.add_widget(c)

        content_layout.bind(minimum_height=content_layout.setter('height'))
        scroll_view = ScrollView(size_hint=(None, None), size=(340, 500), do_scroll_y=True)
        scroll_view.add_widget(content_layout)

        self.add_widget(scroll_view)
        self.add_widget(btn)
        self.add_widget(back_button)

    def on_back_press(self, instance):
        app = App.get_running_app()
        app.root.current = 'take_attendance'
        app.root.transition.direction = 'left'

    def on_submit(self, instance, class_name, section_name, n, rn):
        self.checkbox_states = ['p' if child.active else 'a' for child in self.walk() if isinstance(child, CheckBox)]
        print("Checkbox States:", self.checkbox_states)
        a = self.checkbox_states
        self.main_attendance(class_name, section_name, n, rn, a)

    def main_attendance(self, c, s, n, rn, a):
        print('it is working?', a)
        print(c, s)
        print(n, rn)
        print(len(a))
        print(len(n))
        print(len(rn))
        print('all good?')
        classes = c
        section = s
        att = a
        date = datetime.now().strftime('%Y%m%d')

        create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {classes}_{section}_{date} (
                    Roll_Number INT,
                    Name VARCHAR(50),
                    Attendance VARCHAR(10)
                );
                """
        cursor.execute(create_table_query)
        connection.commit()
        length = len(rn)
        for i in range(length):
            print(f"Attendance a/p: ")
            create_table_query = f"""insert into {classes}_{section}_{date} (Roll_Number, Name, Attendance) VALUES (%s, %s, %s);"""

            report = [rn[i], n[i], att[i]]

            cursor.execute(create_table_query, report)
            connection.commit()


class TheLabApp(MDApp, App):
    Window.size = (340, 690)
    Window.clearcolor = (205 / 255, 238 / 255, 1, 1)

    def build(self):
        return Builder.load_file('main.kv')


if __name__ == '__main__':
    TheLabApp().run()
