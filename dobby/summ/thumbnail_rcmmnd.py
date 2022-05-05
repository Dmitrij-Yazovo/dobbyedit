import glob
import cv2
import re



def rcmd_th(representative_points,img_pth):
    img_files = [cv2.imread(file) for file in sorted(glob.glob(img_pth), key=stringSplitByNumbers)]
    for i in representative_points :
        img = img_files[i]
        
        if img is None :
            print("Image load failed")
            break
        cv2.imshow('img',img)
        cv2.waitKey()
        cv2.imwrite('{}.jpg'.format(i), img) # 이미지 저장

def stringSplitByNumbers(x):
    r = re.compile('(\d+)')
    l = r.split(x)
    return [int(y) if y.isdigit() else y for y in l]





# img_pth = ".//img//*.jpg" # 썸네일 이미지가 저장된 위치
# representative_points =  [ 37, 104, 311, 321] # demo.py 파일 돌렸을 때 출력되는 선택된 shot

# rcmd_th(representative_points,img_pth)