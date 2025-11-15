import cv2
from ultralytics import YOLO

# # Load the YOLO11 model
# model = YOLO("yolo11m-seg.pt")
#
# # Export the model to ONNX format
# model.export(format="onnx")  # creates 'yolo11n.onnx'

# Load the exported ONNX model
onnx_model = YOLO("yolo11m-seg.onnx")

# Run inference
results = onnx_model("sp.png")
cv2.imwrite("cha_result.jpg", results[0].plot())
