"""Optional adapter; dependencies/model must be supplied and approved."""
import argparse,json
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('model');p.add_argument('output');p.add_argument('--every',type=int,default=1);a=p.parse_args()
    if a.every<1:p.error('every must be >=1')
    if Path(a.output).exists():raise FileExistsError('Refusing overwrite')
    import cv2,mediapipe as mp
    cap=cv2.VideoCapture(a.video)
    if not cap.isOpened():raise RuntimeError('Cannot open video')
    fps=cap.get(cv2.CAP_PROP_FPS)
    if fps<=0:raise RuntimeError('Validated CFR fps required')
    opts=mp.tasks.vision.FaceDetectorOptions(base_options=mp.tasks.BaseOptions(model_asset_path=a.model),running_mode=mp.tasks.vision.RunningMode.VIDEO,min_detection_confidence=.6)
    records=[];index=0
    try:
        with mp.tasks.vision.FaceDetector.create_from_options(opts) as detector:
            while True:
                ok,bgr=cap.read()
                if not ok:break
                if index%a.every==0:
                    image=mp.Image(image_format=mp.ImageFormat.SRGB,data=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB));result=detector.detect_for_video(image,round(index/fps*1000));boxes=[]
                    for d in result.detections:
                        b=d.bounding_box;boxes.append({'x':b.origin_x,'y':b.origin_y,'w':b.width,'h':b.height})
                    records.append({'frame':index,'sourceSeconds':index/fps,'status':'detector_observation' if boxes else 'no_face_detected','sourceBoxes':boxes})
                index+=1
    finally:cap.release()
    if index==0:raise RuntimeError('No frames decoded')
    with open(a.output,'x') as f:json.dump({'inputAssumption':'validated CFR only','coordinateSpace':'source_pixels','fps':fps,'every':a.every,'frames':records,'requiresTransformAndReview':True},f,indent=2)
if __name__=='__main__':main()
