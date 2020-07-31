import sys
sys.path.append('../')
from tkinter import filedialog as fd
from backend.interface import *
from backend.analyzer import remove_comments
import os
import tkinter as tk




def remove_spaces(str_remove):
    before = len(str_remove)
    str_remove = str_remove.replace(' ', '')
    str_remove = str_remove.replace('\t', '')
    str_remove = str_remove.replace('\n', '')
    after = len(str_remove)

    spaces_removed = before - after

    return str_remove, spaces_removed


class SourceAnalyzer:

    def open_file1(self):
        if self.language_var.get() == "Python":
            files = fd.askopenfilenames(initialdir=os.getcwd(), title="Open File", filetypes=(("Python Files", "*.py"),("Text Files", "*.txt"),("Java Files", "*.java")))
        elif self.language_var.get() == "Java":
            files = fd.askopenfilenames(initialdir=os.getcwd(), title="Open File", filetypes=(("Java Files", "*.java"),("Python Files", "*.py"),("Text Files", "*.txt")))
        else:
            files = fd.askopenfilenames(initialdir=os.getcwd(), title="Open File", filetypes=(("Text Files", "*.txt"),("Python Files", "*.py"),("Java Files", "*.java")))
        # print(files)
        self.files1 = files
        for file in files:
            self.file_name1.insert(tk.END, file)

    def clear_file1(self):
        self.file1 = []
        self.file_name1.delete(0, tk.END)

    def open_file2(self):
        if self.language_var.get() == "Python":
            files = fd.askopenfilenames(initialdir=os.getcwd(), title="Open File", filetypes=(("Python Files", "*.py"),("Text Files", "*.txt"),("Java Files", "*.java")))
        elif self.language_var.get() == "Java":
            files = fd.askopenfilenames(initialdir=os.getcwd(), title="Open File", filetypes=(("Java Files", "*.java"),("Python Files", "*.py"),("Text Files", "*.txt")))
        else:
            files = fd.askopenfilenames(initialdir=os.getcwd(), title="Open File", filetypes=(("Text Files", "*.txt"),("Python Files", "*.py"),("Java Files", "*.java")))
        # print(files)
        self.files2 = files
        for file in files:
            self.file_name2.insert(tk.END, file)

    def clear_file2(self):
        self.file2 = []
        self.file_name2.delete(0, tk.END)

    def export_files(self):
        #if self.file_name1.curselection() and self.file_name2.curselection():

        self.clear_output()

        file1 = self.file_name1.get(0, tk.END) #student
        file2 = self.file_name2.get(0, tk.END) #boilerplate
        print(file2)

        k = int(self.k_input.get())
        w = int(self.windowSizeInput.get())

        self.fileList=file1
        index1 = 0
        index2 = 1

        if (not (len(file1)<=1)): #student files 1 or empty
            #print("CLEARED: more than one student file")

            diff = True
            for x in file1:
                for y in file2:
                    if x == y:
                        diff = False
            if diff:
                #print("CLEARED: all files differ between bp and student")

                self.file1out = open(file1[index1], 'r').read()
#                try: #boilerplate allowed to be empty
                self.file2out = open(file1[index2], 'r').read()
#                except IndexError as e:
#                    print("no boilerplate files recognized")

                #ADDED for boilerplate

                #
                # Takes in a list of multiple filenames, performs the comparison function and
                # returns an array of filetofingerprint objects
                # the boilerplate argument takes in a list of boilerplate filenames, which is something the files
                # will be allowed to be similar to/copy from
                # ignorecount does nothing right now
                #
                # get_similarity(file1,file2) output s similarities between files
                # switch between the files a output the get_similarity on a pool of student files.
                #

                ignorecount = 0
                #filenames = file1 + file2
                blocksize = 10 ##MAKE USER INPUT
                offset = 3 ##MAKE USER INPUT

                #Python
                if self.language_var.get() == "Python":
                    #res, num_common_fps = compare_files_py(file1, file2, k, w)
                    file2fp_objs = compare_multiple_files_py(file1, k, w, file2, ignorecount)
                    #mimatches = get_most_important_matches_py(file1, file2, blocksize, offset)
                    #fp = get_fps_py(file1, file2, k, w, num_common_fps, int(self.ignore_input.get()))
                #Text
                elif self.language_var.get() == "Java":
                    file2fp_objs = compare_multiple_files_py(file1, k, w, file2, ignorecount)
                else:
                    #res, num_common_fps = compare_files_txt(file1, file2, k, w)
                    file2fp_objs = compare_multiple_files_txt(file1, k, w, file2, ignorecount)
                    #mimatches = get_most_important_matches_txt(file1, file2, blocksize, offset)
                    #fp = get_fps_txt(file1, file2, k, w, num_common_fps, int(self.ignore_input.get()))

                self.f2fp = file2fp_objs

                index1 = 0
                index2 = 1
                self.curr_index1 = index1
                self.curr_index2 = index2

                self.get_output()

            else:
                print("there exists a same file between boilerplate and student files")

        else:
            print("Please include more student files to compare!")
            self.out_result.configure(state='normal')
            self.out_result.delete('1.0', tk.END)
            self.out_result.insert(tk.END, "Please include more student files to compare!")
            self.out_result.configure(state='disabled')

    def get_output(self):

        self.out_result.configure(state='normal')

        percentage = "{:.2%}".format(get_similarity(self.f2fp[self.curr_index1], self.f2fp[self.curr_index2]))
        f2fpstring = str("Files Compared: " + self.f2fp[self.curr_index1].filename + " and " + self.f2fp[self.curr_index2].filename + "\nPercentage Similarity: " + str(percentage) + "\nCommon Fingerprints: " + str(len(self.f2fp[self.curr_index1].similarto[self.f2fp[self.curr_index2]])))
        print(f2fpstring)

        self.out_result.delete('1.0', tk.END)
        self.out_result.insert(tk.END, f2fpstring)

        if self.language_var.get() == "Python":
            if self.f2fp[self.curr_index1].filename[(len(self.f2fp[self.curr_index1].filename) - 3):] != '.py' or self.f2fp[self.curr_index2].filename[(len(self.f2fp[self.curr_index2].filename) - 3):] != '.py':
                self.out_result.insert(tk.END, " WARNING: Used improper analyzer for file type. Results will be inaccurate!")

        if self.language_var.get() == "Java":
            if self.f2fp[self.curr_index1].filename[(len(self.f2fp[self.curr_index1].filename) - 5):] != '.java' or self.f2fp[self.curr_index2].filename[(len(self.f2fp[self.curr_index2].filename) - 5):] != '.java':
                self.out_result.insert(tk.END, " WARNING: Used improper analyzer for file type. Results will be inaccurate!")

        self.out_result.configure(state='disabled')

        print(self.fp_type.get())
        if self.fp_type.get() == 0:
            self.gather_reg_fingerprints()
        else:
            self.gather_most_fingerprints()

    def gather_reg_fingerprints(self):

        self.out_text1.configure(state='normal')
        self.out_text2.configure(state='normal')

        k = int(self.k_input.get())
        w = int(self.windowSizeInput.get())

        file1 = self.f2fp[self.curr_index1].filename
        file2 = self.f2fp[self.curr_index2].filename

        file1out = open(file1, 'r').read()
        file2out = open(file2, 'r').read()

        if self.language_var.get() == "Java":
            file1out = remove_comments(file1out)
            file2out = remove_comments(file2out)

        self.out_text1.tag_config("match", background='yellow')
        self.out_text2.tag_config("match", background='yellow')
        self.out_text1.tag_config("found")
        self.out_text2.tag_config("found")
        self.out_text1.delete('1.0', tk.END)
        self.out_text2.delete('1.0', tk.END)
        self.out_text1.insert(tk.END, self.file1out)
        self.out_text2.insert(tk.END, self.file2out)

        index_track1 = '1.0'

        #Python
        if self.language_var.get() == "Python":
            res, num_common_fps = compare_files_py(file1, file2, k, w, self.file_name2.get(0, tk.END))
            fp = get_fps_py(file1, file2, k, w, num_common_fps, int(self.ignore_input.get()), self.file_name2.get(0, tk.END))

        #Java
        elif self.language_var.get() == "Java":
            res, num_common_fps = compare_files_java(file1, file2, k, w, self.file_name2.get(0, tk.END))
            fp = get_fps_java(file1, file2, k, w, num_common_fps, int(self.ignore_input.get()), self.file_name2.get(0, tk.END))

        #Text
        else:
            res, num_common_fps = compare_files_txt(file1, file2, k, w, self.file_name2.get(0, tk.END))
            fp = get_fps_txt(file1, file2, k, w, num_common_fps, int(self.ignore_input.get()), self.file_name2.get(0, tk.END))


        #fp = self.f2fp[self.curr_index1].similarto[self.f2fp[self.curr_index2]]


        for i in range(len(fp)):
            self.out_text1.tag_config("match" + str(i), background='white')
            self.out_text2.tag_config("match" + str(i), background='white')
        self.out_text1.delete('1.0', tk.END)
        self.out_text2.delete('1.0', tk.END)
        self.out_text1.insert(tk.END, file1out)
        self.out_text2.insert(tk.END, file2out)

        index_track1 = '1.0'
        fp_track = 0

        for fingerprint in fp:

            index1 = []
            index2 = []

            len1 = []
            len2 = []

            index_track2 = '1.0'

            for i in range(len(fingerprint[0])):
                index1.append(self.out_text1.search(fingerprint[0][i].substring, index_track1, tk.END))
                print("1 - " + str(fp_track + 1) + ": " + fingerprint[0][i].substring)
                if index1[-1] != '':
                    self.out_text1.tag_add("match" + str(fp_track), index1[-1], str(index1[-1]) + "+" + str(len(fingerprint[0][i].substring)) + "c")
                    len1.append(len(fingerprint[0][i].substring))
                else:
                    index1.pop(-1)
                    print("COULD NOT FIND")

            for i in range(len(fingerprint[1])):
                index2.append(self.out_text2.search(fingerprint[1][i].substring, '1.0', tk.END))
                print("2 - " + str(fp_track + 1) + ": " + fingerprint[1][i].substring)
                if index2[-1] != '':
                    self.out_text2.tag_add("match" + str(fp_track), index2[-1], str(index2[-1]) + "+" + str(len(fingerprint[1][i].substring)) + "c")
                    len2.append(len(fingerprint[1][i].substring))
                    index_track2 = index2[-1]
                else:
                    index2.pop(-1)          
                    print("COULD NOT FIND")    

            if len(index1) > 0:
                index_track1 = index1[0]

            fp_track += 1

        self.out_text1.configure(state='disabled')
        self.out_text2.configure(state='disabled')

        self.fp = fp

        self.max_fp = len(self.fp)
        self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)

        self.show_fp()

    def gather_most_fingerprints(self):
        self.out_text1.configure(state='normal')
        self.out_text2.configure(state='normal')

        k = int(self.k_input.get())
        w = int(self.windowSizeInput.get())

        file1 = self.f2fp[self.curr_index1].filename
        file2 = self.f2fp[self.curr_index2].filename

        file1out = open(file1, 'r').read()
        file2out = open(file2, 'r').read()

        if self.language_var.get() == "Java":
            file1out = remove_comments(file1out)
            file2out = remove_comments(file2out)

        self.out_text1.tag_config("most", background='green')
        self.out_text2.tag_config("most", background='green')
        self.out_text1.delete('1.0', tk.END)
        self.out_text2.delete('1.0', tk.END)
        self.out_text1.insert(tk.END, self.file1out)
        self.out_text2.insert(tk.END, self.file2out)

        index_track1 = '1.0'

        #Python
        if self.language_var.get() == "Python":
            get_most_important_matches_javpy(self.f2fp[self.curr_index1], self.f2fp[self.curr_index2], k, 3, 6)

        #Java
        elif self.language_var.get() == "Java":
            get_most_important_matches_javpy(self.f2fp[self.curr_index1], self.f2fp[self.curr_index2], k, 3, 6)

        #Text
        else:
            get_most_important_matches_txt(self.f2fp[self.curr_index1], self.f2fp[self.curr_index2], k, 3, 6)

        fp = self.f2fp[self.curr_index1].mostimportantmatches[self.f2fp[self.curr_index2]]
        #print(fp)


        for i in range(len(fp)):
            self.out_text1.tag_config("match" + str(i), background='white')
            self.out_text2.tag_config("match" + str(i), background='white')
        self.out_text1.delete('1.0', tk.END)
        self.out_text2.delete('1.0', tk.END)
        self.out_text1.insert(tk.END, file1out)
        self.out_text2.insert(tk.END, file2out)

        index_track1 = '1.0'
        fp_track = 0

        for fingerprint in fp:

            index1 = []
            index2 = []

            len1 = []
            len2 = []

            index_track2 = '1.0'

            for i in range(len(fingerprint[0])):
                index1.append(self.out_text1.search(fingerprint[0], '1.0', tk.END))
                #print("1 - " + str(fp_track + 1) + ": " + fingerprint[0])
                if index1[-1] != '':
                    self.out_text1.tag_add("most" + str(fp_track), index1[-1], str(index1[-1]) + "+" + str(len(fingerprint[0])) + "c")
                    len1.append(len(fingerprint[0][i]))
                else:
                    index1.pop(-1)
                    print("COULD NOT FIND")

            print(str(len(fingerprint[0])))
            print(str(len(fingerprint[1])))
            for i in range(len(fingerprint[1])):
                index2.append(self.out_text2.search(fingerprint[1][i], '1.0', tk.END))
                #print("2 - " + str(fp_track + 1) + ": " + fingerprint[1][i])
                if index2[-1] != '':
                    self.out_text2.tag_add("most" + str(fp_track), index2[-1], str(index2[-1]) + "+" + str(len(fingerprint[1][i])) + "c")
                    len2.append(len(fingerprint[1][i]))
                    index_track2 = index2[-1]
                else:
                    index2.pop(-1)          
                    print("COULD NOT FIND")    

            if len(index1) > 0:
                index_track1 = index1[0]

            fp_track += 1

        self.out_text1.configure(state='disabled')
        self.out_text2.configure(state='disabled')

        self.fp = fp

        self.max_fp = len(self.fp)
        self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)

        self.show_most_fp()

    def next_file1(self):
        self.out_result.configure(state='normal')
        #print("REACHED next_file1. curr_index1=" + str(self.curr_index1) + ". curr_index2=" + str(self.curr_index2))

        if (self.curr_index1+1) == self.curr_index2:
            self.curr_index1 = self.curr_index1 + 2
        else:
            self.curr_index1 = self.curr_index1 + 1

        if self.curr_index1 >= len(self.f2fp):
            if self.curr_index2 != 0:
                self.curr_index1 = 0
            else:
                self.curr_index1 = 1

        self.out_result.configure(state='disabled')
        self.get_output()

    def next_file2(self):
        self.out_result.configure(state='normal')
        #print("REACHED next_file2. curr_index1=" + str(self.curr_index1) + ". curr_index2=" + str(self.curr_index2))


        if (self.curr_index2+1) == self.curr_index1:
            self.curr_index2 = self.curr_index2 + 2
        else:
            self.curr_index2 = self.curr_index2 + 1

        if self.curr_index2 >= len(self.f2fp):
            if self.curr_index1 != 0:
                self.curr_index2 = 0
            else:
                self.curr_index2 = 1

        self.out_result.configure(state='disabled')
        self.get_output()

    def prev_file1(self):
        self.out_result.configure(state='normal')
        #print("REACHED prev_file1. curr_index1=" + str(self.curr_index1) + ". curr_index2=" + str(self.curr_index2))


        if (self.curr_index1-1) == self.curr_index2:
            self.curr_index1 = self.curr_index1 - 2
        else:
            self.curr_index1 = self.curr_index1 - 1

        if self.curr_index1 < 0:
            if self.curr_index2 != len(self.f2fp) - 1:
                self.curr_index1 = len(self.f2fp) - 1
            else:
                self.curr_index1 = len(self.f2fp) - 2

        self.out_result.configure(state='disabled')
        self.get_output()

    def prev_file2(self):
        self.out_result.configure(state='normal')
        #print("REACHED prev_file2. curr_index1=" + str(self.curr_index1) + ". curr_index2=" + str(self.curr_index2))

        if (self.curr_index2-1) == self.curr_index1:
            self.curr_index2 = self.curr_index2 - 2
        else:
            self.curr_index2 = self.curr_index2 - 1

        if self.curr_index2 < 0:
            if self.curr_index1 != len(self.f2fp) - 1:
                self.curr_index2 = len(self.f2fp) - 1
            else:
                self.curr_index2 = len(self.f2fp) - 2

        self.out_result.configure(state='disabled')
        self.get_output()

    def show_fp(self):
        if self.fp_type.get() == 0:
            self.show_reg_fp()
        else:
            self.show_most_fp()

    def show_reg_fp(self):

        self.out_text1.configure(state='normal')
        self.out_text2.configure(state='normal')

        if self.view_var.get() == 1:
            if self.max_fp > 0:
                self.cur_fp = 1
            else:
                self.cur_fp = 0
            for i in range(self.max_fp):
                self.out_text1.tag_config("match" + str(i), background='yellow')
                self.out_text2.tag_config("match" + str(i), background='yellow')

        else:
            if self.max_fp > 0:
                self.cur_fp = 1
                
                for i in range(self.max_fp):
                    self.out_text1.tag_config("match" + str(i), background='white')
                    self.out_text2.tag_config("match" + str(i), background='white')

                self.out_text1.tag_config("match0", background='yellow')
                self.out_text2.tag_config("match0", background='yellow')

                self.out_text1.tag_raise("match0")
                self.out_text2.tag_raise("match0")

                self.out_text1.see(self.out_text1.tag_ranges("match0")[0])
                self.out_text2.see(self.out_text2.tag_ranges("match0")[0])
                
            else:
                self.cur_fp = 0
            self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)

        self.out_text1.configure(state='disabled')
        self.out_text2.configure(state='disabled')

    def show_most_fp(self):

        self.out_text1.configure(state='normal')
        self.out_text2.configure(state='normal')

        if self.view_var.get() == 1:
            if self.max_fp > 0:
                self.cur_fp = 1
            else:
                self.cur_fp = 0
            for i in range(self.max_fp):
                self.out_text1.tag_config("most" + str(i), background='green')
                self.out_text2.tag_config("most" + str(i), background='green')

        else:
            if self.max_fp > 0:
                self.cur_fp = 1
                
                for i in range(self.max_fp):
                    self.out_text1.tag_config("most" + str(i), background='white')
                    self.out_text2.tag_config("most" + str(i), background='white')

                self.out_text1.tag_config("most0", background='green')
                self.out_text2.tag_config("most0", background='green')

                self.out_text1.tag_raise("most0")
                self.out_text2.tag_raise("most0")

                self.out_text1.see(self.out_text1.tag_ranges("most0")[0])
                self.out_text2.see(self.out_text2.tag_ranges("most0")[0])
                
            else:
                self.cur_fp = 0
            self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)

        self.out_text1.configure(state='disabled')
        self.out_text2.configure(state='disabled')

    def next_fp(self):
        if self.fp_type.get() == 0:
            if self.view_var.get() == 0:
                if self.cur_fp < self.max_fp:

                    for i in range(self.max_fp):
                        self.out_text1.tag_config("match" + str(i), background='white')
                        self.out_text2.tag_config("match" + str(i), background='white')

                    self.out_text1.tag_lower("match" + str(self.cur_fp - 1))
                    self.out_text2.tag_lower("match" + str(self.cur_fp - 1))

                    self.out_text1.tag_config("match" + str(self.cur_fp), background='yellow')
                    self.out_text2.tag_config("match" + str(self.cur_fp), background='yellow')

                    self.out_text1.tag_raise("match" + str(self.cur_fp))
                    self.out_text2.tag_raise("match" + str(self.cur_fp))

                    self.out_text1.see(self.out_text1.tag_ranges("match" + str(self.cur_fp))[1])
                    self.out_text2.see(self.out_text2.tag_ranges("match" + str(self.cur_fp))[1])

                    
                    self.cur_fp = self.cur_fp + 1
                    self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)
        else:
            if self.view_var.get() == 0:
                if self.cur_fp < self.max_fp:

                    for i in range(self.max_fp):
                        self.out_text1.tag_config("most" + str(i), background='white')
                        self.out_text2.tag_config("most" + str(i), background='white')

                    self.out_text1.tag_lower("most" + str(self.cur_fp - 1))
                    self.out_text2.tag_lower("most" + str(self.cur_fp - 1))

                    self.out_text1.tag_config("most" + str(self.cur_fp), background='green')
                    self.out_text2.tag_config("most" + str(self.cur_fp), background='green')

                    self.out_text1.tag_raise("most" + str(self.cur_fp))
                    self.out_text2.tag_raise("most" + str(self.cur_fp))

                    self.out_text1.see(self.out_text1.tag_ranges("most" + str(self.cur_fp))[1])
                    self.out_text2.see(self.out_text2.tag_ranges("most" + str(self.cur_fp))[1])

                    
                    self.cur_fp = self.cur_fp + 1
                    self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)

    def last_fp(self):
        if self.fp_type.get() == 0:
            if self.view_var.get() == 0:
                if self.cur_fp > 1:

                    for i in range(self.max_fp):
                        self.out_text1.tag_config("match" + str(i), background='white')
                        self.out_text2.tag_config("match" + str(i), background='white')

                    self.out_text1.tag_lower("match" + str(self.cur_fp - 1))
                    self.out_text2.tag_lower("match" + str(self.cur_fp - 1))

                    self.out_text1.tag_config("match" + str(self.cur_fp - 2), background='yellow')
                    self.out_text2.tag_config("match" + str(self.cur_fp - 2), background='yellow')

                    self.out_text1.tag_raise("match" + str(self.cur_fp - 2))
                    self.out_text2.tag_raise("match" + str(self.cur_fp - 2))

                    self.out_text1.see(self.out_text1.tag_ranges("match" + str(self.cur_fp - 2))[0])
                    self.out_text2.see(self.out_text2.tag_ranges("match" + str(self.cur_fp - 2))[0])
                    
                    self.cur_fp = self.cur_fp - 1
                    self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)
        else:
            if self.view_var.get() == 0:
                if self.cur_fp > 1:

                    for i in range(self.max_fp):
                        self.out_text1.tag_config("most" + str(i), background='white')
                        self.out_text2.tag_config("most" + str(i), background='white')

                    self.out_text1.tag_lower("most" + str(self.cur_fp - 1))
                    self.out_text2.tag_lower("most" + str(self.cur_fp - 1))

                    self.out_text1.tag_config("most" + str(self.cur_fp - 2), background='green')
                    self.out_text2.tag_config("most" + str(self.cur_fp - 2), background='green')

                    self.out_text1.tag_raise("most" + str(self.cur_fp - 2))
                    self.out_text2.tag_raise("most" + str(self.cur_fp - 2))

                    self.out_text1.see(self.out_text1.tag_ranges("most" + str(self.cur_fp - 2))[0])
                    self.out_text2.see(self.out_text2.tag_ranges("most" + str(self.cur_fp - 2))[0])
                    
                    self.cur_fp = self.cur_fp - 1
                    self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)

    def clear_output(self):

        self.out_result.configure(state='normal')
        self.out_text1.configure(state='normal')
        self.out_text2.configure(state='normal')

        self.out_result.delete('1.0', tk.END)
        self.out_text1.delete('1.0', tk.END)
        self.out_text2.delete('1.0', tk.END)

        for i in range(len(self.fp)):
            self.out_text1.tag_delete('match' + str(i))
            self.out_text2.tag_delete('match' + str(i))

        self.out_result.configure(state='disabled')
        self.out_text1.configure(state='disabled')
        self.out_text2.configure(state='disabled')

        self.fp = []
        self.f2fp = []
        self.curr_index1 = 0
        self.curr_index2 = 1
        self.cur_fp = 0
        self.max_fp = 0

    def mult_yview(self, *args):
        self.out_text1.yview(*args)
        self.out_text2.yview(*args)

    def donothing(self):
        x = 0

    def openHelp(self):
        helpSect = tk.Toplevel()
        helpSect.title("SCAM Help Manual")
        inputMessage = "Welcome to the SCAM Help Manual! Our tool, the Source Code Analyzing Machine, is used to \n\nK (noise threshold) impacts sensitivity. Fingerprints size < k will be ignored.\n" \
                       "Window Size is the winnow size used by the algorithm.\n" \
                       "Ignore Count determines fingerprint threshold for commonality.\n" \
                       "Python files should be able to be compiled for the best results.\n\n"
        tk.Label(helpSect, text=inputMessage).pack()
        tk.Button(helpSect, text="DONE", command=helpSect.destroy).pack()

    def __init__(self, master):
        self.master = master
        self.create_widgets()

    def create_widgets(self):

    #Store Filenames
        self.files1 = []
        self.files2 = []

    #Tracking Fingerprints
        self.cur_fp = 0
        self.max_fp = 0
        self.fp = []
        self.most_fp = []

    #Tracking Multiple Files
        self.curr_index1 = 0
        self.curr_index2 = 1
        self.f2fp = []

        self.menubar = tk.Menu(self.master)
        
        self.upper = tk.Frame(self.master)
        self.upper.pack(side = "top", fill='both', pady=5, padx=5)

        self.top_frame = tk.Frame(self.upper)
        self.top_frame.pack(expand=True, side = "left", fill='both', pady=5)

        self.button_panel = tk.Frame(self.upper)
        self.button_panel.pack(side="right", fill='x', padx=10, pady=5)

        self.output_frame = tk.Frame(self.master)
        self.output_frame.pack(expand=True, fill='both', pady=5, side='bottom')

        self.bottom_frame = tk.Frame(self.output_frame)
        self.bottom_frame.pack(expand=True, fill='both', pady=5)

        self.index_btns = tk.Frame(self.bottom_frame)
        self.index_btns.pack(expand=False, fill='x', pady=5, side='bottom')

        self.index_btns1 = tk.Frame(self.index_btns)
        self.index_btns1.pack(expand=True, fill='x', side='left')

        self.index_btns2 = tk.Frame(self.index_btns)
        self.index_btns2.pack(expand=True, fill='x', side='right')

        self.very_bottom = tk.Frame(self.output_frame, width=0, height=5)
        self.very_bottom.pack(expand=False, fill='none', pady=5, side="bottom")

    #Menubar

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        #self.filemenu.add_command(label="New Window", command=self.master.open) #newWindow
        ##self.filemenu.add_command(label="Save Settings", command=self.donothing)
        #self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.master.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        #self.toolsmenu = tk.Menu(self.menubar, tearoff=0)
        #self.toolsmenu.add_command(label="Check Matches", command=self.donothing)
        #self.toolsmenu.add_command(label="Fingerprint Offest", command=self.donothing)
        #self.menubar.add_cascade(label="Tools", menu=self.toolsmenu)

        #self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        #self.helpmenu.add_command(label="Manual", command= self.openHelp)
        #self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.master.config(menu=self.menubar)
          
    #Filename Display

        self.file1_frame = tk.Frame(self.top_frame)
        self.file1_frame.pack(side='top', expand=True, fill='both')

        self.file2_frame = tk.Frame(self.top_frame)
        self.file2_frame.pack(side='bottom', expand=True, fill='both')

        #ADDED for bp
        self.bpfile_frame = tk.Frame(self.top_frame)
        self.bpfile_frame.pack(side='bottom', expand=True, fill='both')

        #Filebox 1

        self.cur_file_label1 = tk.Label(self.file1_frame, text = "Student Files: ")
        self.cur_file_label1.pack(anchor='w')
        self.cur_file_label1.config(font=(None, 9))

        self.file_name1 = tk.Listbox(self.file1_frame, height=5, exportselection=False)

        self.file_scroll1 = tk.Scrollbar(self.file1_frame, command=self.file_name1.yview)
        self.file_name1['yscrollcommand'] = self.file_scroll1.set
        self.file_scroll1.pack(expand=False, fill="y", side='right')

        self.file_name1.pack(expand=True, pady=(0, 10), fill='both')

        #Filebox 2

        self.cur_file_label2 = tk.Label(self.file2_frame, text = "Boilerplate Files: ")
        self.cur_file_label2.pack(anchor='w')
        self.cur_file_label2.config(font=(None, 9))

        self.file_name2 = tk.Listbox(self.file2_frame, height=5, exportselection=False)

        self.file_scroll2 = tk.Scrollbar(self.file2_frame, command=self.file_name2.yview)
        self.file_name2['yscrollcommand'] = self.file_scroll2.set
        self.file_scroll2.pack(expand=False, fill="y", side='right')

        self.file_name2.pack(expand=True, fill='both')

    #Button Panel

        #File Selection

        #self.filter_label = tk.Label(self.button_panel, text = "Added File Filter: ")
        #self.filter_label.grid(row=0, column=0)
        #self.filter_label.config(font=(None, 9))

        #self.file_filter = tk.Text(self.button_panel, height=1, width=30, state='disabled')
        #self.file_filter.grid(row=0, column=1, columnspan=4)

        photo1 = tk.PhotoImage(file="source/SCAM.png")
        smallerphoto1 = photo1.subsample(6,6)
        imglabel = tk.Label(self.button_panel, image=smallerphoto1)
        imglabel.image = smallerphoto1
        imglabel.grid(row=0, column=0, columnspan=4, padx=100)

        """
        photo = Image.open("source/SCAM.png")
        smallerphoto = photo.resize((round(photo.size[0] * .1), round(photo.size[1] * .1)));
        render = ImageTk.PhotoImage(smallerphoto)
        img = tk.Label(self.button_panel, image=render)
        img.image = render
        img.grid(row=0, column=0, columnspan=4)
        """

        #self.k_desc_label = tk.Label(self.button_panel, text = "K (noise threshold) impacts sensitivity. Fingerprints size < k will be ignored.\nWindow Size is the winnow size used by the algorithm.\nIgnore Count determines fingerprint threshold for commonality.\nPython files should be able to be compiled for the best results.")
        #self.k_desc_label.grid(row=1, column=0, columnspan=4)
        #self.k_desc_label.config(font=(None, 8))

        self.w_desc_label = tk.Label(self.button_panel, text = "Default values set for optimal machine output. \n View Help Manual for more information.")
        self.w_desc_label.grid(row=1, column=0, columnspan=4)
        self.w_desc_label.config(font=(None, 8))


        #self.ignore_label = tk.Label(self.button_panel, text = "Ignore Files: ")
        #self.ignore_label.grid(row=1, column=0)
        #self.ignore_label.config(font=(None, 9))

        #self.file_ignore = tk.Text(self.button_panel, height=1, width=30, state='disabled')
        #self.file_ignore.grid(row=1, column=1, columnspan=4)

        self.button1 = tk.Button(self.button_panel, text="Add Student Files", command=self.open_file1, bg="gray75", width=15)
        self.button1.grid(row = 2, column = 0, padx = 1, pady = 5, columnspan=2)

        self.button1a = tk.Button(self.button_panel, text="Clear Student File(s)", command=self.clear_file1, bg="gray80", width=15)
        self.button1a.grid(row = 2, column = 2, padx = 1, pady = 5, columnspan=2)

        self.button2 = tk.Button(self.button_panel, text="Add Boilerplate Files", command=self.open_file2, bg="gray75", width=15)
        self.button2.grid(row = 3, column = 0, padx =1, pady = 2, columnspan=2)

        self.button2a = tk.Button(self.button_panel, text="Clear Boilerplate File(s)", command=self.clear_file2, bg="gray80", width=15)
        self.button2a.grid(row = 3, column = 2, padx = 1, pady = 2, columnspan=2)

        #Commands

        self.lang_label = tk.Label(self.button_panel, text = "Language: ")
        self.lang_label.grid(row = 5, column = 0, pady = 10)
        self.lang_label.config(font=(None, 9))

        self.language_var = tk.StringVar(self.button_panel)
        self.language_var.set("Python")
        self.languageMenu = tk.OptionMenu(self.button_panel, self.language_var, "Text", "Python", "Java")
        self.languageMenu.grid(row=5, column=1, pady=10, sticky='w', columnspan=2)

        self.ignore_count_label = tk.Label(self.button_panel, text = "Ignore Count: ")
        self.ignore_count_label.grid(row = 5, column = 2, pady = 10)
        self.ignore_count_label.config(font=(None, 9))

        self.ignore_input = tk.Spinbox(self.button_panel, from_=0, to=255, width=5)
        self.ignore_input.grid(row=5, column=3, pady=10)
        self.ignore_input.delete(0, tk.END)
        self.ignore_input.insert(0, '5')

        #Advanced

        self.k_label = tk.Label(self.button_panel, text = "K-grams: ")
        self.k_label.grid(row = 7, column = 0, padx = 1, pady = (10,0))
        self.k_label.config(font=(None, 9))

        self.k_input = tk.Spinbox(self.button_panel, from_=1, to=255, width=5)
        self.k_input.grid(row=7, column=1, padx=5, pady = (10,0))

        self.k_input.delete(0, tk.END)
        self.k_input.insert(0, '10')

        self.w_label = tk.Label(self.button_panel, text = "Window Size: ")
        self.w_label.grid(row = 7, column = 2, padx = 1, pady = (10,0))
        self.w_label.config(font=(None, 9))

        self.windowSizeInput = tk.Spinbox(self.button_panel, from_=1, to=255, width=5)
        self.windowSizeInput.grid(row=7, column=3, padx=5, pady = (10,0))

        self.windowSizeInput.delete(0, tk.END)
        self.windowSizeInput.insert(0, '5')

        self.fp_count_lbl = tk.Label(self.button_panel, text = "Block Size: ")
        self.fp_count_lbl.grid(row = 7, column = 0, padx = 5, pady = 5)
        self.fp_count_lbl.config(font=(None, 9))

        self.fp_count_in = tk.Spinbox(self.button_panel, from_=1, to=255, width=5)
        self.fp_count_in.grid(row=7, column=1, padx=5, pady = 5)
        self.fp_count_in.delete(0, tk.END)
        self.fp_count_in.insert(0, '3')

        self.offset_lbl = tk.Label(self.button_panel, text = "Offset: ")
        self.offset_lbl.grid(row = 7, column = 2, padx = 1, pady = 5, columnspan=1)
        self.offset_lbl.config(font=(None, 9))

        self.offset_in = tk.Spinbox(self.button_panel, from_=1, to=255, width=5)
        self.offset_in.grid(row=7, column=3, padx=5, pady = 5, columnspan=2)
        self.offset_in.delete(0, tk.END)
        self.offset_in.insert(0, '6')

        #Compare

        self.run_label = tk.Button(self.button_panel, text="Compare", height = 1, width = 40, command=self.export_files, bg="gray75", bd=3)
        self.run_label.grid(row=9, column=0, pady=(20, 0), columnspan=4)

        self.clear_label = tk.Button(self.button_panel, text="Clear Output", height = 1, width = 40, command=self.clear_output, bg="gray80", bd=3)
        self.clear_label.grid(row=10, column=0, pady=2.5, columnspan=4)

    #Bottom Frame

        self.output_lbl = tk.Label(self.bottom_frame, text = "Output")
        self.output_lbl.pack()

        self.out_result = tk.Text(self.bottom_frame, width=1, height=4)
        self.out_result.pack(fill="x", side='top', padx=10, pady=5)
        self.out_result.configure(state='disabled')

        self.out_text1 = tk.Text(self.bottom_frame, width=1, height=1, )
        self.out_text1.configure(state='disabled')

        self.txt_scroll1 = tk.Scrollbar(self.bottom_frame, command=self.mult_yview)
        self.out_text1['yscrollcommand'] = self.txt_scroll1.set

        self.out_text1.pack(expand=True, fill="both", padx=(10,0),pady=10, side='left')
        self.txt_scroll1.pack(side='left', padx=(0,10), fill='y', pady=10)

        self.out_text2 = tk.Text(self.bottom_frame, width=1, height=1, )
        self.out_text2.configure(state='disabled')

        self.txt_scroll2 = tk.Scrollbar(self.bottom_frame, command=self.mult_yview)
        self.out_text2['yscrollcommand'] = self.txt_scroll2.set

        self.out_text2.pack(expand=True, fill="both", padx=(10,0),pady=10, side='left')
        self.txt_scroll2.pack(side='left', padx=(0,10), fill='y', pady=10)

    #Another Bottom Frame
        self.next_filebtn1 = tk.Button(self.index_btns1, text="Compare Next File", command=self.next_file1, bg="gray75", width=15)
        self.next_filebtn1.pack(expand=True, side='right', padx=(5,25), fill='x')

        self.prev_filebtn1 = tk.Button(self.index_btns1, text="Compare Previous File", command=self.prev_file1, bg="gray80", width=15)
        self.prev_filebtn1.pack(expand=True, side='left', padx=(25,5), fill='x')

        self.next_filebtn2 = tk.Button(self.index_btns2, text="Compare Next File", command=self.next_file2, bg="gray75", width=15)
        self.next_filebtn2.pack(expand=True, side='right', padx=(5,25), fill='x')

        self.prev_filebtn2 = tk.Button(self.index_btns2, text="Compare Previous File", command=self.prev_file2, bg="gray80", width=15)
        self.prev_filebtn2.pack(expand=True, side='left', padx=(25,5), fill='x')

    #Very Bottom

        self.display_label = tk.Label(self.very_bottom, text = "Output Type: ")
        self.display_label.grid(row = 0, column = 0, padx = (10,0), pady = 10)
        self.display_label.config(font=(None, 9))

        self.fp_type = tk.IntVar(self.very_bottom)
        self.fp_type.set(0)
        self.fp_menu1 = tk.Radiobutton(self.very_bottom, text="All Fingerprints", variable=self.fp_type, value=0)
        self.fp_menu1.grid(row=0, column=1, padx=(0,15), pady=(20,0), sticky='w', columnspan=2)
        self.fp_menu2 = tk.Radiobutton(self.very_bottom, text="Most Important", variable=self.fp_type, value=1)
        self.fp_menu2.grid(row=0, column=1, padx=(0,15), pady=(0,20), sticky='w', columnspan=2)
        
        self.view_label = tk.Label(self.very_bottom, text="View All?")
        self.view_label.grid(row=0, column=3, padx=(10,0), pady=5)

        self.view_var = tk.IntVar()

        self.view_all = tk.Checkbutton(self.very_bottom, command=self.show_fp, variable=self.view_var)
        self.view_all.grid(row=0, column=4, padx=5, pady=5)

        self.last_fp = tk.Button(self.very_bottom, text="Last Fingerprint", command=self.last_fp)
        self.last_fp.grid(row=0, column=5, padx=5, pady=5)

        self.current_fp = tk.Label(self.very_bottom, text="Current: " + str(self.cur_fp) + "/" + str(self.max_fp))
        self.current_fp.grid(row=0, column=6, padx=5, pady=5)

        self.next_fp = tk.Button(self.very_bottom, text="Next Fingerprint", command=self.next_fp)
        self.next_fp.grid(row=0, column=7, padx=(5, 350), pady=5)


def main():
    root = tk.Tk()
    root.geometry("1080x720")
    root.title("Source Code Analyzer Machine")
    gui = SourceAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()

