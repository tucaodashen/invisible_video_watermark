import onnxruntime as rt
import cv2
import numpy as np
from image_resizer import image_preprocess_resizing, image_postprocess_resizing

model_path = "./data/models/RealESRGAN_ANIME_6B_512x512.onnx"
sess = rt.InferenceSession(model_path, providers=['CPUExecutionProvider'])
input_name = sess.get_inputs()[0].name

def up_scale(input_image, output_path):
    """
    written by @muhammad-ahmed-ghani
    :param input_image:
    :param output_path:
    :return:
    """
    img = cv2.imread(input_image, cv2.IMREAD_UNCHANGED)
    img, padding, old_dims = image_preprocess_resizing(img,
                                                       square_size=512)  # 512 is the size of the image you want to resize to (512x512)

    h_input, w_input = img.shape[0:2]

    img = img.astype(np.float32)

    if np.max(img) > 256:  # 16-bit image
        max_range = 65535
        print('Input is a 16-bit image')
    else:
        print('Input is not a 16-bit image resetting to 8-bit...')
        max_range = 255

    # Normalize the image
    img = img / max_range
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.transpose(img, (2, 0, 1)).astype(np.float16)

    # inference
    pred = sess.run(None, {input_name: img[None, ...]})[0]

    # Convert back to 8-bit image
    outscale = 4
    output_img = pred[0].transpose(1, 2, 0)

    # Denormalize the image
    if max_range == 65535:  # 16-bit image
        output = (output_img * 65535.0).round().astype(np.uint16)
    else:
        output = (output_img * 255.0).round().astype(np.uint8)

    output = cv2.resize(
        output, (
            int(w_input * outscale),
            int(h_input * outscale),
        ), interpolation=cv2.INTER_LANCZOS4)

    # Save the output image
    output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
    output = image_postprocess_resizing(output, padding, old_dims,
                                        outscale)  # Here you can change the upscale factor default:1

    cv2.imwrite(output_path, output)
