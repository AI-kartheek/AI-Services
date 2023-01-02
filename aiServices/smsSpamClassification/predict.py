import subprocess

env_path = "F:/Python Web Projects/FLASK/AI Services/project env/smsspam_env/Scripts/python.exe"
exe_path = "F:/Python Web Projects/FLASK/AI Services/aiServices/smsSpamClassification/utils/model.py"

def getPrediction(input_data):
    batch = '0'
    args = [env_path, exe_path, '--batch', batch, '--input_data', input_data]
    output = subprocess.run(args, capture_output=True, text=True)
    if output.returncode == 0:
        ans = round(float(output.stdout), 3) 
        return ans
    else:
        print(output.stderr)
    return 0

def getBatchPrediction(input_file_path, output_file_path):
    batch = '1'
    args = [env_path, exe_path, '--batch', batch, '--input_file_path', input_file_path, '--output_file_path', output_file_path]
    output = subprocess.run(args, capture_output=True, text=True)
    if output.returncode == 0:
        return [int(x) for x in output.stdout.split(',')]
    else:
        print(output.stderr)
    return 0 

# inp = "I'm gonna be home soon and i don't want to talk about this stuff anymore tonight, k? I've cried enough today."
# print(getPrediction(inp))