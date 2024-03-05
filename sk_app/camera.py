import cv2
import mediapipe as mp
import time
import numpy as np
import finger
import csv
import mmap
import os

#メモリマップファイルで送る関係のクラス
class Send_data:
    def create(self,filename):
        file_exists = os.path.exists(filename)
        if not file_exists:
            with open(filename,'w',newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=ConnectCamera.fieldnames)
                writer.writeheader()
        
    def send_csv_data(self,data):
        with open(ConnectCamera.filename, 'r+b') as file:
            mmapped_file = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_WRITE)
            mmapped_file[:len(data)] = data
            mmapped_file.flush()
            
    def connect_memory(self):
            
        try:
            with open(ConnectCamera.filename, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=ConnectCamera.fieldnames)
                writer.writerow({
                    'command': ConnectCamera.send_command
                })
            with open(ConnectCamera.filename, 'r') as csvfile:
                csvfile.seek(ConnectCamera.last_position)  # 前回の終了位置から読み取り
                csv_data = csvfile.read()
                # CSVデータが変更された場合のみ送信
                if csv_data:
                    # CSVデータをメモリマップファイルに送信
                    self.send_csv_data(csv_data.encode())
                    # 今回の終了位置を記録
                    ConnectCamera.last_position = csvfile.tell()
        except Exception as e:
            print("Error during CSV writing:", str(e))
    
#変数を初期化するクラス
class Reset:
    
    def clear_file(self):
        with open(ConnectCamera.filename, 'r') as file:
            lines = file.readlines()
        with open(ConnectCamera.filename, 'w') as file:
            file.write(lines[0])
            
    def reset_finger_array(self):
        ConnectCamera.before_swipe_array = np.array([0,0])
        ConnectCamera.before_zoom_thumb_array = np.array([0,0])
        ConnectCamera.before_zoom_index_array = np.array([0,0])
        
    def reset_pose_value(self):
        ConnectCamera.set_pose = False
        ConnectCamera.check_swipe = False
        ConnectCamera.check_zoomup = False
        ConnectCamera.check_zoomout = False
    
    def reset_timer(self):
        ConnectCamera.start_time = time.time()
        
    def reset_template(self):
        self.reset_finger_array()
        self.reset_pose_value()
        self.reset_timer()

#メインの処理をまとめる関数
class ConnectCamera:
    
    #スワイプ指ポーズ判定時の人差し指先端の座標を保存
    before_swipe_array = np.array([0,0])
    #ズーム指ポーズ判定時の親指先端の座標を保存
    before_zoom_thumb_array = np.array([0,0])
    #ズーム指ポーズ判定時の人差し指先端の座標を保存
    before_zoom_index_array = np.array([0,0])
    #タイマーの初期値
    start_time = -1
    #mediapipeで起動したカメラの表示画面に表示する文字用
    display_message = ""
    #各ポーズをしているかの判定用
    set_pose = False
    check_swipe = False
    check_zoom = False
    check_zoomup = False
    check_zoomput = False
    #blenderに送るコマンドの保存用
    send_command = "none"
    #前に読み込んだCSVの最後の位置の保存用
    last_position = 0
    #共有するファイルの保存場所
    filename = "./share.csv"
    #CSVファイルのヘッダーに使用する値
    fieldnames = ['command']
    #指の距離（ズーム用）
    before_distance = 0
    
    reset = Reset()
        
    #def get_finger_position(self,fingerData,finger_name):
    #    finger_coords = getattr(fingerData, finger_name)
    #    position_data = np.array([finger_coords.x,finger_coords.y])
    #    return position_data
    
    def get_finger_position(self,fingerData,finger_num):
        finger_coords = fingerData.get_finger_for_hew(finger_num)
        position_data = np.array([finger_coords.x,finger_coords.y])
        return position_data
    
        
    def set_value(self,message,command):
        ConnectCamera.display_message = message
        ConnectCamera.send_command = command
        ConnectCamera.reset.reset_template()
        
    def swipe(self,fingerData):
        index_finger = self.get_finger_position(fingerData,8)
        if np.linalg.norm(index_finger-ConnectCamera.before_swipe_array) > 0.2:
            self.set_value("check_swipe","swipe")
            
    def zoom(self,fingerData):
        zoom_thumb_array = self.get_finger_position(fingerData,4)
        zoom_index_array = self.get_finger_position(fingerData,8)
        distance = np.linalg.norm(zoom_thumb_array-zoom_index_array)
        if ConnectCamera.check_zoomup:
            #if distance-ConnectCamera.before_distance > 0.1:
                self.set_value("check_zoomup","zoomup")
        elif ConnectCamera.check_zoomout:
            #if ConnectCamera.before_distance-distance > 0.1:
                self.set_value("check_zoomout","zoomout")
                
    def set_swipe_pose(self,fingerData):
        ConnectCamera.before_swipe_array = self.get_finger_position(fingerData,8)
        ConnectCamera.display_message =  "check_swipe_finger"
        ConnectCamera.set_pose = True
        
    def get_distance(self,from_finger,to_finger):
            from_array = self.get_finger_position(fingerData,from_finger)
            to_array = self.get_finger_position(fingerData,to_finger)
            distance = np.linalg.norm(from_array-to_array)
            return distance
        
    def set_zoom_pose(self,fingerData):
        ConnectCamera.check_zoom = fingerData.check_zoom_for_hew()
        ConnectCamera.check_zoomup = ConnectCamera.check_zoom[0]
        ConnectCamera.check_zoomout = ConnectCamera.check_zoom[1]
        if ConnectCamera.check_zoomup or ConnectCamera.check_zoomout:
            #ConnectCamera.before_distance = self.get_distance('thumb_finger_tip','index_finger_tip')
            if ConnectCamera.check_zoomup:
                ConnectCamera.display_message =  "check_zoomup_finger"
            elif ConnectCamera.check_zoomout:
                ConnectCamera.display_message =  "check_zoomout_finger"
            ConnectCamera.set_pose = True
            #continue
    
    def clear(self):   
        ConnectCamera.reset.reset_pose_value()
        ConnectCamera.display_message =  "clear"
        ConnectCamera.send_command = "none"
        
if __name__ == '__main__':
    
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands
    
    # Webカメラから入力
    camera = ConnectCamera()
    send_data = Send_data()
    send_data.create(camera.filename)
    cap = cv2.VideoCapture(0)
    reset = Reset()
    
    reset.clear_file()
    # MediaPipeの手の検出モデルを初期化
    with mp_hands.Hands(
        model_complexity=0,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            # 検出された手の骨格をカメラ画像に重ねて描画
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
                    # スワイプ検出
                    fingerData = finger.Finger(hand_landmarks)
                    fingerData.detectFingerPose()
                    #fingerData.get_finger()
                    clear = fingerData.clear_for_hew()
                    if clear:
                        camera.clear()
                    if camera.set_pose:
                        if camera.check_swipe:
                            camera.swipe(fingerData)
                        elif camera.check_zoom:
                            camera.zoom(fingerData)
                        else:
                            continue
                    else:
                        elapsed_time = time.time() - camera.start_time
                        if elapsed_time > 1:
                            send_command = "none"
                            camera.check_swipe = fingerData.check_swipe_for_hew()
                            if camera.check_swipe:
                                camera.set_swipe_pose(fingerData)
                            else:
                                camera.set_zoom_pose(fingerData)
            else:
                reset.reset_pose_value()
            send_data.connect_memory()
            cv2.putText(image, camera.display_message, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()
    cv2.destroyAllWindows()
    


# from mediapipe.python.solutions import hands     
# solution = hands.Hands()
# solution.close()