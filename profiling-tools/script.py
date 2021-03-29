import os
import sys
import shutil
import tempfile
from shutil import copyfile

# CONFIG
apps = ['app1', 'app2'] # réplications de l'application d'introduction (1 build  ~= 5min)
yml = '.onedev-buildspec.yml'
clients = 10 # nombre de branches associées à chaque application


def commit(branch, push=False):
    os.system('git add .')
    os.system('git commit -m ' + branch)
    if push: os.system('git push --set-upstream origin ' + branch)


if __name__ == '__main__':

    for appName in apps:

        # INIT
        os.system('npx create-react-app ' + appName)
        copyfile(yml, appName + '\\' + yml)

        # PUSH
        os.chdir(appName)
        commit('master')
        os.system('git remote add origin http://127.0.0.1:6610/' + appName)
        os.system('git push origin master:master')
        
        for x in range(1, clients+1):
            branch = 'b' + str(x)
            os.system('git checkout -b ' + branch)
            with open("touch.txt", "w") as f:
                f.write("touch")
            commit(branch, push=True)
            os.system('git checkout master')
        
        os.chdir('../')

        # CLEAN
        os.system('rmdir ' + appName + ' /s /q')
        
    os.system('cls')
    print("Finis!")
