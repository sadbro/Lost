from tkinter import *
import json
import random

def default(title, s):

    host= Tk()
    host.title(title)
    Label(host, text=s).pack()

class Host():

    def __init__(self, register_fp="register.json", matches_fp="matches.json", groups=4):
        self.file= register_fp
        self.match= matches_fp
        self.default_groups= int(groups)

    def divide(self, names, no_grps):

        grps= []
        n= len(names)//no_grps
        for i in range(no_grps):
            grps.append(names[n*i:(n*i)+n])

        return grps

    def start(self):

        def warning(s):
            host= Tk()
            host.title("WARNING!!")
            host.geometry("300x100")
            Label(host, text=s).pack()
            Button(host, text="Close", command=host.destroy, bd='2').pack(side='bottom')

        def CreateProfile():
            host= Tk()
            host.title('Enter your Details')

            name_str= Entry(host)
            desc_str= Entry(host)
            n= Label(host, text='Enter name:').grid(row=0, column=1)
            d= Label(host, text='Enter ID:').grid(row=1, column=1)

            def Submit():
                name= name_str.get()
                code= desc_str.get()

                with open(self.file) as f:
                    data= json.load(f)
                    dict= {"name":name, "ID":code}
                    data["players"].append(dict)

                with open(self.file, "w") as writer:
                    json.dump(data, writer)

                host.destroy()

            SubmitInput= Button(host, text='Submit', command=Submit)

            name_str.grid(row=0, column=2)
            desc_str.grid(row=1, column=2)
            SubmitInput.grid(row=3, column=2)

        def CreateGroupsOf2():
            with open(self.file) as f:
                data= json.load(f)
            names= []
            grps= self.default_groups
            for player in data["players"]:
                names.append(player["name"])
            if len(names)==0:
                warning("No participants found!!")
            elif len(names)%grps!=0:
                warning("Cannot divide players: {} in {}".format(len(names), grps))
            else:
                random.shuffle(names)
                Gs= self.divide(names, self.default_groups)

                for i, grp in enumerate(Gs):
                    c= i+1
                    list= "GROUP {}\n\n".format(c)
                    for name in grp:
                        list+= "NAME: {}\n".format(name)

                    default("G{}".format(c), list)

            with open(self.match, "w") as f:
                data= {"groups":[*Gs]}
                json.dump(data, f)

        def Display():
            host= Tk()
            host.title('Player List')
            host.geometry("200x100")

            list= "# of players: {}"
            count= 0

            with open(self.file) as f:
                data= json.load(f)
                for i, player in enumerate(data["players"]):
                    count+= 1

            Label(host, text= list.format(count)).pack()
            Button(host, text="Create Groups", command=CreateGroupsOf2).pack(side='top')
            Button(host, text="Back", command=host.destroy).pack(side='bottom')


        win= Tk()
        win.title('TestRun')
        win.geometry("200x100")

        Entree= Button(win, text='New Player', command=CreateProfile).pack()
        Display= Button(win, text='Player List', command=Display).pack()

        win.mainloop()


