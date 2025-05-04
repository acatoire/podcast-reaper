import torch

# Check if CUDA is available and print the number of GPUs
avaliable = torch.cuda.is_available()
if avaliable:
    print("!!!  CUDA is available   !!!")
print("CUDA available:", )
print("Number of GPUs:", torch.cuda.device_count())
print("Current device index:", torch.cuda.current_device())
print("Device object for index 0:", torch.cuda.device(0))
print("Device name for index 0:", torch.cuda.get_device_name(0))
