import argparse
import os
import cv2
import urllib.request
import numpy as np

def make_helloween_card(drawing):
  template = cv2.imread("NFT_SPOT_Helloween.jpeg")
  t_w, t_h, _ = template.shape
  mask_template = np.ones((t_h, t_w))*255

  drawing = cv2.blur(drawing, (3,3))
  drawing_hsv = cv2.cvtColor(drawing, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange(drawing_hsv, np.array([0,50,50]), np.array([10,255,255]))

  x,y,w,h = cv2.boundingRect(mask)
  cropped_mask = mask[y:y+h, x:x+w]
  cropped_mask = cv2.bitwise_not(cropped_mask)

  template_area_x = 1700
  template_area_y = 800
  template_area_w = 2200
  template_area_h = 1500

  if w>h:
    resized_mask = cv2.resize(cropped_mask, (template_area_w, int(template_area_w/w*h)), interpolation = cv2.INTER_AREA)
    resized_mask = cv2.blur(resized_mask, (13,13))
    mask_template[template_area_y:template_area_y+int(template_area_w/w*h), template_area_x:template_area_x+template_area_w] = resized_mask[:,:]
  else:
    resized_mask = cv2.resize(cropped_mask, (int(template_area_h/h*w), template_area_h), interpolation = cv2.INTER_AREA)
    resized_mask = cv2.blur(resized_mask, (13,13))
    mask_template[template_area_y:template_area_y+template_area_h, template_area_x:template_area_x+int(template_area_h/h*w)] = resized_mask[:,:]

  mask_template = (mask_template>0)*255
  mask_template = mask_template.astype('uint8')

  return cv2.bitwise_and(template, template, mask=mask_template)

def start_record(video_url, output_path, last_im_file, last_drawing_file, helloween_drawing_file):
    stream = cv2.VideoCapture(video_url)

    width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = stream.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (width, height))
    last_frame = None
    print("Start video recording...", 'stream:', video_url, 'output:', output_path)
    try:
        while (True):
            ret, frame = stream.read()
            last_frame = frame.copy()
            if ret==True:
                out.write(frame)
            else:
                break
    except KeyboardInterrupt:
        print("Stop video recording...")
    finally:
        print("\nVideo recording stopped")
        if last_frame is not None:
            cv2.imwrite(last_im_file, last_frame)
            req = urllib.request.urlopen('http://luke.merklebot:8000//blackboard')
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            last_drawing = cv2.imdecode(arr, -1)
            cv2.imwrite(last_drawing_file, last_drawing, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            helloween_img = make_helloween_card(last_drawing)
            cv2.imwrite(helloween_drawing_file, helloween_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

        stream.release()
        out.release()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Downloads video from the video server')
    parser.add_argument("--video_url", dest='video_url', required=True, type=str, help='URL of the video')
    parser.add_argument("--output_file", dest='output_file', required=True, type=str, help='Output file')
    parser.add_argument("--last_im_file", dest='last_im_file', required=True, type=str, help='Last image file (save after process interruption)')
    parser.add_argument("--last_drawing_file", dest='last_drawing_file', required=True, type=str, help='Last drawing file (save after process interruption)')
    parser.add_argument("--helloween_drawing_file", dest='helloween_drawing_file', required=True, type=str, help='Last drawing file (save after process interruption)')

    args = parser.parse_args()
    start_record(args.video_url, args.output_file, args.last_im_file, args.last_drawing_file, args.helloween_drawing_file)
