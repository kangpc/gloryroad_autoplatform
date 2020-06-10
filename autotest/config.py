import os

projectPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
screenRelativePath = "media/captureScreens/"



print(projectPath)
print(os.path.join(projectPath, screenRelativePath, "xxx", '.png'))