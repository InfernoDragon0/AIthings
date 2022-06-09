from yolov5 import custom
import cv2


class Process:
    def __init__(self,device="cpu",weights="./atasv3.pt"):
        self.model = custom(path=weights,device=device)
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        print(self.names)

    def draw_box_xyxy(self, img, result):
        for i in result:
            label = i["class"]
            RED = (0,0,255)
            BLUE = (255,0,0)
            color = BLUE

            box = i["box"]
            left = int(box[0])
            top = int(box[1])
            right = int(box[2])
            bottom = int(box[3])

            cv2.rectangle(img, (left, top), (right, bottom), color, 2)
            cv2.putText(img, label,
                        (left + 20, top + 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,  # font scale
                        color,
                        2)  # line type
        return img


    def inference_json_result(self,imgs):
        result = self.model(imgs)
        result.print()
        result = result.xyxy[0].tolist()

        result_array = []
        for i in result:

            result_dict = {}
            result_dict['box'] = [i[0], i[1], i[2], i[3]]
            result_dict['score'] = i[4]
            result_dict['class'] = self.names[int(i[5])]

            if result_dict['class'] == "face":
                result_array.append(result_dict)
            #result_array.append(result_dict)

        return result_array

    def inference_image_result(self, source):
        #img = cv2.imread(source)
        result = self.inference_json_result(source)
        img = self.draw_box_xyxy(source, result)
        
        im_bytes =  cv2.imencode('.jpg',img)[1].tobytes()

        return im_bytes
